"""
Question 4: PSO for Hyperparameter Optimization
- Use Particle Swarm Optimization to optimize neural network hyperparameters
- Optimize: Number of hidden neurons (50-300), Learning rate (0.0001-0.01),
  Batch size (32-256), Dropout rate (0-0.5)
- Compare default hyperparameters vs PSO-optimized hyperparameters
"""

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models
import numpy as np
import matplotlib.pyplot as plt
import time
import os

# Create output directory
output_dir = "output/q4"
os.makedirs(output_dir, exist_ok=True)

print("=" * 70)
print("QUESTION 4: PSO FOR HYPERPARAMETER OPTIMIZATION")
print("=" * 70)

# ============================================================================
# 1. LOAD AND PREPARE DATA
# ============================================================================
print("\n1. LOADING DATA")
print("-" * 70)

# Load MNIST dataset
mnist = keras.datasets.mnist
(train_images, train_labels), (test_images, test_labels) = mnist.load_data()

# Normalize and flatten
train_images_flat = train_images.reshape(-1, 784) / 255.0
test_images_flat = test_images.reshape(-1, 784) / 255.0

print(f"Training samples: {len(train_images)}")
print(f"Test samples: {len(test_images)}")

# ============================================================================
# 2. DEFINE HYPERPARAMETER SPACE
# ============================================================================
print("\n2. HYPERPARAMETER SEARCH SPACE")
print("-" * 70)

# Hyperparameter bounds
NEURONS_MIN, NEURONS_MAX = 50, 300
LR_MIN, LR_MAX = 0.0001, 0.01
BATCH_MIN, BATCH_MAX = 32, 256
DROPOUT_MIN, DROPOUT_MAX = 0.0, 0.5

print(f"Number of neurons: [{NEURONS_MIN}, {NEURONS_MAX}]")
print(f"Learning rate: [{LR_MIN}, {LR_MAX}]")
print(f"Batch size: [{BATCH_MIN}, {BATCH_MAX}]")
print(f"Dropout rate: [{DROPOUT_MIN}, {DROPOUT_MAX}]")

# ============================================================================
# 3. FITNESS FUNCTION (EVALUATE HYPERPARAMETERS)
# ============================================================================

def evaluate_hyperparameters(params, X_train, y_train, epochs=5):
    """
    Evaluate a set of hyperparameters
    params: [neurons, learning_rate, batch_size, dropout_rate]
    Returns: validation accuracy (fitness)
    """
    neurons = int(params[0])
    learning_rate = params[1]
    batch_size = int(params[2])
    dropout_rate = params[3]
    
    # Ensure valid ranges
    neurons = np.clip(neurons, NEURONS_MIN, NEURONS_MAX)
    learning_rate = np.clip(learning_rate, LR_MIN, LR_MAX)
    batch_size = np.clip(batch_size, BATCH_MIN, BATCH_MAX)
    dropout_rate = np.clip(dropout_rate, DROPOUT_MIN, DROPOUT_MAX)
    
    # Build model with these hyperparameters
    # Ensure neurons is a proper integer
    neurons = int(round(neurons))
    model = models.Sequential([
        layers.Input(shape=(784,)),
        layers.Dense(neurons, activation='relu'),
        layers.Dropout(dropout_rate),
        layers.Dense(10, activation='softmax')
    ])
    
    optimizer = keras.optimizers.Adam(learning_rate=learning_rate)
    model.compile(
        optimizer=optimizer,
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    
    # Train with validation split
    history = model.fit(
        X_train, y_train,
        epochs=epochs,
        batch_size=batch_size,
        validation_split=0.2,
        verbose=0
    )
    
    # Return final validation accuracy
    val_accuracy = history.history['val_accuracy'][-1]
    return val_accuracy

# ============================================================================
# 4. PSO IMPLEMENTATION FOR HYPERPARAMETER OPTIMIZATION
# ============================================================================

class HyperparameterPSO:
    def __init__(self, n_particles=10, n_dimensions=4, bounds=None, max_iter=20):
        self.n_particles = n_particles
        self.n_dimensions = n_dimensions
        self.bounds = bounds  # [(min1, max1), (min2, max2), ...]
        self.max_iter = max_iter
        
        # PSO hyperparameters
        self.w = 0.7  # Inertia weight
        self.c1 = 1.5  # Cognitive parameter
        self.c2 = 1.5  # Social parameter
        
        # Initialize particles within bounds
        self.positions = np.zeros((n_particles, n_dimensions))
        for i in range(n_dimensions):
            self.positions[:, i] = np.random.uniform(
                bounds[i][0], bounds[i][1], n_particles
            )
        
        self.velocities = np.random.uniform(-0.1, 0.1, (n_particles, n_dimensions))
        
        # Personal best
        self.pbest_positions = self.positions.copy()
        self.pbest_fitness = np.full(n_particles, -float('inf'))  # Maximizing accuracy
        
        # Global best
        self.gbest_position = None
        self.gbest_fitness = -float('inf')
        
        # History
        self.fitness_history = []
        self.iteration_details = []
        
    def optimize(self, fitness_func, X_train, y_train):
        """Run PSO optimization."""
        print(f"\nRunning PSO with {self.n_particles} particles for {self.max_iter} iterations...")
        print("This may take several minutes...\n")
        
        for iteration in range(self.max_iter):
            iteration_start = time.time()
            
            # Evaluate fitness for all particles
            for i in range(self.n_particles):
                fitness = fitness_func(self.positions[i], X_train, y_train)
                
                # Update personal best
                if fitness > self.pbest_fitness[i]:
                    self.pbest_fitness[i] = fitness
                    self.pbest_positions[i] = self.positions[i].copy()
                
                # Update global best
                if fitness > self.gbest_fitness:
                    self.gbest_fitness = fitness
                    self.gbest_position = self.positions[i].copy()
            
            # Store history
            self.fitness_history.append(self.gbest_fitness)
            
            iteration_time = time.time() - iteration_start
            self.iteration_details.append({
                'iteration': iteration + 1,
                'best_fitness': self.gbest_fitness,
                'time': iteration_time
            })
            
            print(f"  Iteration {iteration + 1}/{self.max_iter} - "
                  f"Best Accuracy: {self.gbest_fitness:.4f} ({self.gbest_fitness*100:.2f}%) - "
                  f"Time: {iteration_time:.1f}s")
            
            # Update velocities and positions
            for i in range(self.n_particles):
                r1 = np.random.random(self.n_dimensions)
                r2 = np.random.random(self.n_dimensions)
                
                cognitive = self.c1 * r1 * (self.pbest_positions[i] - self.positions[i])
                social = self.c2 * r2 * (self.gbest_position - self.positions[i])
                
                self.velocities[i] = self.w * self.velocities[i] + cognitive + social
                
                # Update position
                self.positions[i] += self.velocities[i]
                
                # Apply bounds
                for j in range(self.n_dimensions):
                    self.positions[i, j] = np.clip(
                        self.positions[i, j],
                        self.bounds[j][0],
                        self.bounds[j][1]
                    )
        
        return self.gbest_position, self.gbest_fitness

# ============================================================================
# 5. RUN PSO OPTIMIZATION
# ============================================================================
print("\n3. RUNNING PSO HYPERPARAMETER OPTIMIZATION")
print("-" * 70)

# Define bounds
bounds = [
    (NEURONS_MIN, NEURONS_MAX),      # neurons
    (LR_MIN, LR_MAX),                # learning rate
    (BATCH_MIN, BATCH_MAX),          # batch size
    (DROPOUT_MIN, DROPOUT_MAX)       # dropout rate
]

# Initialize PSO
pso = HyperparameterPSO(
    n_particles=10,
    n_dimensions=4,
    bounds=bounds,
    max_iter=20
)

# Run optimization
start_time = time.time()
best_params, best_fitness = pso.optimize(evaluate_hyperparameters, 
                                         train_images_flat, train_labels)
pso_time = time.time() - start_time

print(f"\nPSO Optimization completed in {pso_time:.2f} seconds ({pso_time/60:.1f} minutes)")

# Extract best hyperparameters
best_neurons = int(best_params[0])
best_lr = best_params[1]
best_batch = int(best_params[2])
best_dropout = best_params[3]

print("\n4. BEST HYPERPARAMETERS FOUND BY PSO")
print("-" * 70)
print(f"Number of neurons: {best_neurons}")
print(f"Learning rate: {best_lr:.6f}")
print(f"Batch size: {best_batch}")
print(f"Dropout rate: {best_dropout:.4f}")
print(f"Validation accuracy: {best_fitness:.4f} ({best_fitness*100:.2f}%)")

# ============================================================================
# 6. TRAIN MODEL WITH PSO-OPTIMIZED HYPERPARAMETERS
# ============================================================================
print("\n5. TRAINING WITH PSO-OPTIMIZED HYPERPARAMETERS")
print("-" * 70)

model_pso = models.Sequential([
    layers.Input(shape=(784,)),
    layers.Dense(best_neurons, activation='relu'),
    layers.Dropout(best_dropout),
    layers.Dense(10, activation='softmax')
])

optimizer_pso = keras.optimizers.Adam(learning_rate=best_lr)
model_pso.compile(
    optimizer=optimizer_pso,
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

history_pso = model_pso.fit(
    train_images_flat, train_labels,
    epochs=10,
    batch_size=best_batch,
    validation_split=0.2,
    verbose=1
)

test_loss_pso, test_acc_pso = model_pso.evaluate(test_images_flat, test_labels, verbose=0)
print(f"\nPSO-Optimized Model Test Accuracy: {test_acc_pso:.4f} ({test_acc_pso*100:.2f}%)")

# ============================================================================
# 7. TRAIN MODEL WITH DEFAULT HYPERPARAMETERS
# ============================================================================
print("\n6. TRAINING WITH DEFAULT HYPERPARAMETERS (FOR COMPARISON)")
print("-" * 70)

# Default hyperparameters
default_neurons = 128
default_lr = 0.001
default_batch = 32
default_dropout = 0.2

print(f"Default neurons: {default_neurons}")
print(f"Default learning rate: {default_lr}")
print(f"Default batch size: {default_batch}")
print(f"Default dropout rate: {default_dropout}")

model_default = models.Sequential([
    layers.Input(shape=(784,)),
    layers.Dense(default_neurons, activation='relu'),
    layers.Dropout(default_dropout),
    layers.Dense(10, activation='softmax')
])

optimizer_default = keras.optimizers.Adam(learning_rate=default_lr)
model_default.compile(
    optimizer=optimizer_default,
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

history_default = model_default.fit(
    train_images_flat, train_labels,
    epochs=10,
    batch_size=default_batch,
    validation_split=0.2,
    verbose=1
)

test_loss_default, test_acc_default = model_default.evaluate(test_images_flat, test_labels, verbose=0)
print(f"\nDefault Model Test Accuracy: {test_acc_default:.4f} ({test_acc_default*100:.2f}%)")

# ============================================================================
# 8. COMPARISON AND ANALYSIS
# ============================================================================
print("\n" + "=" * 70)
print("COMPARISON: PSO-OPTIMIZED VS DEFAULT HYPERPARAMETERS")
print("=" * 70)

print("\n7. HYPERPARAMETER COMPARISON")
print("-" * 70)
print(f"{'Hyperparameter':<20} {'Default':<20} {'PSO-Optimized':<20}")
print("-" * 70)
print(f"{'Neurons':<20} {default_neurons:<20} {best_neurons:<20}")
print(f"{'Learning Rate':<20} {default_lr:<20.6f} {best_lr:<20.6f}")
print(f"{'Batch Size':<20} {default_batch:<20} {best_batch:<20}")
print(f"{'Dropout Rate':<20} {default_dropout:<20.4f} {best_dropout:<20.4f}")

print("\n8. PERFORMANCE COMPARISON")
print("-" * 70)
print(f"{'Metric':<30} {'Default':<15} {'PSO-Optimized':<15} {'Improvement'}")
print("-" * 70)
print(f"{'Test Accuracy':<30} {test_acc_default:.4f}        {test_acc_pso:.4f}        {(test_acc_pso - test_acc_default)*100:+.2f}%")

improvement_pct = ((test_acc_pso - test_acc_default) / test_acc_default) * 100
print(f"\nRelative improvement: {improvement_pct:+.2f}%")

if test_acc_pso > test_acc_default:
    print(f"[OK] PSO-optimized hyperparameters achieve better performance")
else:
    print(f"[OK] Default hyperparameters perform similarly or better")

# ============================================================================
# 9. VISUALIZATION
# ============================================================================

# Plot 1: PSO Convergence
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# PSO convergence
axes[0, 0].plot(pso.fitness_history, linewidth=2, marker='o', markersize=4)
axes[0, 0].set_title('PSO Convergence (Best Validation Accuracy)', fontsize=12, fontweight='bold')
axes[0, 0].set_xlabel('Iteration', fontsize=10)
axes[0, 0].set_ylabel('Validation Accuracy', fontsize=10)
axes[0, 0].grid(True, alpha=0.3)
axes[0, 0].set_ylim([0.9, 1.0])

# Training comparison
axes[0, 1].plot(history_default.history['val_accuracy'], label='Default', linewidth=2)
axes[0, 1].plot(history_pso.history['val_accuracy'], label='PSO-Optimized', linewidth=2)
axes[0, 1].set_title('Validation Accuracy Comparison', fontsize=12, fontweight='bold')
axes[0, 1].set_xlabel('Epoch', fontsize=10)
axes[0, 1].set_ylabel('Validation Accuracy', fontsize=10)
axes[0, 1].legend()
axes[0, 1].grid(True, alpha=0.3)

# Hyperparameter comparison
params = ['Neurons', 'LR×1000', 'Batch Size', 'Dropout×100']
default_vals = [default_neurons, default_lr*1000, default_batch, default_dropout*100]
pso_vals = [best_neurons, best_lr*1000, best_batch, best_dropout*100]

x = np.arange(len(params))
width = 0.35

axes[1, 0].bar(x - width/2, default_vals, width, label='Default', alpha=0.7)
axes[1, 0].bar(x + width/2, pso_vals, width, label='PSO-Optimized', alpha=0.7)
axes[1, 0].set_title('Hyperparameter Values Comparison', fontsize=12, fontweight='bold')
axes[1, 0].set_ylabel('Value', fontsize=10)
axes[1, 0].set_xticks(x)
axes[1, 0].set_xticklabels(params, fontsize=9)
axes[1, 0].legend()
axes[1, 0].grid(True, alpha=0.3, axis='y')

# Test accuracy comparison
models_list = ['Default', 'PSO-Optimized']
accuracies = [test_acc_default, test_acc_pso]
colors = ['blue', 'green']

bars = axes[1, 1].bar(models_list, accuracies, color=colors, alpha=0.7, edgecolor='black', linewidth=2)
for bar in bars:
    height = bar.get_height()
    axes[1, 1].text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.4f}', ha='center', va='bottom', fontweight='bold')

axes[1, 1].set_title('Test Accuracy Comparison', fontsize=12, fontweight='bold')
axes[1, 1].set_ylabel('Test Accuracy', fontsize=10)
axes[1, 1].set_ylim([0.96, 0.99])
axes[1, 1].grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig(f"{output_dir}/pso_hyperparameter_optimization.png", dpi=300, bbox_inches='tight')
print(f"\nVisualization saved to: {output_dir}/pso_hyperparameter_optimization.png")
plt.close()

# Save results
with open(f"{output_dir}/optimization_results.txt", 'w') as f:
    f.write("PSO Hyperparameter Optimization Results\n")
    f.write("=" * 70 + "\n\n")
    f.write("Best Hyperparameters Found:\n")
    f.write(f"  Neurons: {best_neurons}\n")
    f.write(f"  Learning Rate: {best_lr:.6f}\n")
    f.write(f"  Batch Size: {best_batch}\n")
    f.write(f"  Dropout Rate: {best_dropout:.4f}\n\n")
    f.write("Performance Comparison:\n")
    f.write(f"  Default Test Accuracy: {test_acc_default:.4f}\n")
    f.write(f"  PSO-Optimized Test Accuracy: {test_acc_pso:.4f}\n")
    f.write(f"  Improvement: {(test_acc_pso - test_acc_default)*100:+.2f}%\n\n")
    f.write(f"PSO Optimization Time: {pso_time:.2f}s ({pso_time/60:.1f} min)\n")

print(f"Results saved to: {output_dir}/optimization_results.txt")

print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)
print("[OK] PSO hyperparameter optimization completed")
print(f"[OK] Best hyperparameters found in {pso_time/60:.1f} minutes")
print(f"[OK] PSO-optimized model: {test_acc_pso*100:.2f}% test accuracy")
print(f"[OK] Default model: {test_acc_default*100:.2f}% test accuracy")
print(f"[OK] Improvement: {(test_acc_pso - test_acc_default)*100:+.2f}%")
print(f"[OK] All outputs saved to: {output_dir}/")
print("=" * 70)
