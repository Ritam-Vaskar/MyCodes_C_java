"""
Question 5: PSO-based Neural Architecture Search (NAS)
- Use PSO to automatically search for optimal neural network architecture
- Particle encoding: Number of hidden layers (1-3), Neurons per layer (32-256),
  Activation function (ReLU/Tanh), Dropout rate
- Compare best architecture vs manually designed model
"""

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models
import numpy as np
import matplotlib.pyplot as plt
import time
import os

# Create output directory
output_dir = "output/q5"
os.makedirs(output_dir, exist_ok=True)

print("=" * 70)
print("QUESTION 5: PSO-BASED NEURAL ARCHITECTURE SEARCH (NAS)")
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
# 2. DEFINE ARCHITECTURE SEARCH SPACE
# ============================================================================
print("\n2. ARCHITECTURE SEARCH SPACE")
print("-" * 70)

LAYERS_MIN, LAYERS_MAX = 1, 3
NEURONS_MIN, NEURONS_MAX = 32, 256
ACTIVATION_OPTIONS = ['relu', 'tanh']  # 0 = relu, 1 = tanh
DROPOUT_MIN, DROPOUT_MAX = 0.0, 0.5

print(f"Number of hidden layers: [{LAYERS_MIN}, {LAYERS_MAX}]")
print(f"Neurons per layer: [{NEURONS_MIN}, {NEURONS_MAX}]")
print(f"Activation functions: {ACTIVATION_OPTIONS}")
print(f"Dropout rate: [{DROPOUT_MIN}, {DROPOUT_MAX}]")

# Architecture encoding:
# [n_layers, neurons_layer1, neurons_layer2, neurons_layer3, 
#  activation (0=relu, 1=tanh), dropout_rate]
N_DIMENSIONS = 6

print(f"\nParticle encoding dimension: {N_DIMENSIONS}")
print("  - Position[0]: Number of layers (1-3)")
print("  - Position[1]: Neurons in layer 1 (32-256)")
print("  - Position[2]: Neurons in layer 2 (32-256, if exists)")
print("  - Position[3]: Neurons in layer 3 (32-256, if exists)")
print("  - Position[4]: Activation function (0=ReLU, 1=Tanh)")
print("  - Position[5]: Dropout rate (0.0-0.5)")

# ============================================================================
# 3. ARCHITECTURE EVALUATION FUNCTION
# ============================================================================

def decode_architecture(params):
    """Decode particle position into architecture specification."""
    n_layers = int(np.clip(params[0], LAYERS_MIN, LAYERS_MAX))
    neurons = [
        int(np.clip(params[1], NEURONS_MIN, NEURONS_MAX)),
        int(np.clip(params[2], NEURONS_MIN, NEURONS_MAX)),
        int(np.clip(params[3], NEURONS_MIN, NEURONS_MAX))
    ][:n_layers]  # Only use neurons for active layers
    
    activation_idx = int(np.round(np.clip(params[4], 0, 1)))
    activation = ACTIVATION_OPTIONS[activation_idx]
    
    dropout = np.clip(params[5], DROPOUT_MIN, DROPOUT_MAX)
    
    return n_layers, neurons, activation, dropout

def build_model_from_architecture(n_layers, neurons, activation, dropout):
    """Build a Keras model from architecture specification."""
    model = models.Sequential()
    model.add(layers.Input(shape=(784,)))
    
    # Add hidden layers
    for i in range(n_layers):
        model.add(layers.Dense(neurons[i], activation=activation))
        model.add(layers.Dropout(dropout))
    
    # Output layer
    model.add(layers.Dense(10, activation='softmax'))
    
    return model

def evaluate_architecture(params, X_train, y_train, epochs=5):
    """
    Evaluate an architecture
    Returns: validation accuracy (fitness)
    """
    # Decode architecture
    n_layers, neurons, activation, dropout = decode_architecture(params)
    
    # Build model
    try:
        model = build_model_from_architecture(n_layers, neurons, activation, dropout)
        
        model.compile(
            optimizer='adam',
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )
        
        # Train with validation split
        history = model.fit(
            X_train, y_train,
            epochs=epochs,
            batch_size=32,
            validation_split=0.2,
            verbose=0
        )
        
        # Return final validation accuracy
        val_accuracy = history.history['val_accuracy'][-1]
        return val_accuracy
    
    except Exception as e:
        # Return low fitness if architecture is invalid
        return 0.5

# ============================================================================
# 4. PSO FOR ARCHITECTURE SEARCH
# ============================================================================

class ArchitectureSearchPSO:
    def __init__(self, n_particles=15, n_dimensions=6, bounds=None, max_iter=20):
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
        self.pbest_fitness = np.full(n_particles, -float('inf'))
        
        # Global best
        self.gbest_position = None
        self.gbest_fitness = -float('inf')
        
        # History
        self.fitness_history = []
        self.architecture_history = []
        
    def optimize(self, fitness_func, X_train, y_train):
        """Run PSO optimization."""
        print(f"\nRunning Architecture Search with {self.n_particles} particles for {self.max_iter} iterations...")
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
            n_layers, neurons, activation, dropout = decode_architecture(self.gbest_position)
            self.architecture_history.append({
                'iteration': iteration + 1,
                'fitness': self.gbest_fitness,
                'n_layers': n_layers,
                'neurons': neurons,
                'activation': activation,
                'dropout': dropout
            })
            
            iteration_time = time.time() - iteration_start
            
            print(f"  Iteration {iteration + 1}/{self.max_iter} - "
                  f"Best Accuracy: {self.gbest_fitness:.4f} - "
                  f"Layers: {n_layers}, Neurons: {neurons}, Act: {activation} - "
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
# 5. RUN ARCHITECTURE SEARCH
# ============================================================================
print("\n3. RUNNING PSO-BASED ARCHITECTURE SEARCH")
print("-" * 70)

# Define bounds for architecture parameters
bounds = [
    (LAYERS_MIN, LAYERS_MAX),      # number of layers
    (NEURONS_MIN, NEURONS_MAX),    # neurons layer 1
    (NEURONS_MIN, NEURONS_MAX),    # neurons layer 2
    (NEURONS_MIN, NEURONS_MAX),    # neurons layer 3
    (0, 1),                        # activation (0=relu, 1=tanh)
    (DROPOUT_MIN, DROPOUT_MAX)     # dropout rate
]

# Initialize PSO
pso = ArchitectureSearchPSO(
    n_particles=15,
    n_dimensions=N_DIMENSIONS,
    bounds=bounds,
    max_iter=20
)

# Run optimization
start_time = time.time()
best_arch_params, best_fitness = pso.optimize(evaluate_architecture, 
                                              train_images_flat, train_labels)
search_time = time.time() - start_time

print(f"\nArchitecture Search completed in {search_time:.2f} seconds ({search_time/60:.1f} minutes)")

# Decode best architecture
best_n_layers, best_neurons, best_activation, best_dropout = decode_architecture(best_arch_params)

print("\n4. BEST ARCHITECTURE FOUND BY PSO")
print("-" * 70)
print(f"Number of hidden layers: {best_n_layers}")
print(f"Neurons per layer: {best_neurons}")
print(f"Activation function: {best_activation}")
print(f"Dropout rate: {best_dropout:.4f}")
print(f"Validation accuracy: {best_fitness:.4f} ({best_fitness*100:.2f}%)")

# ============================================================================
# 6. TRAIN BEST ARCHITECTURE
# ============================================================================
print("\n5. TRAINING BEST ARCHITECTURE")
print("-" * 70)

model_best = build_model_from_architecture(best_n_layers, best_neurons, 
                                          best_activation, best_dropout)
model_best.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

print("\nModel Architecture:")
model_best.summary()

history_best = model_best.fit(
    train_images_flat, train_labels,
    epochs=10,
    batch_size=32,
    validation_split=0.2,
    verbose=1
)

test_loss_best, test_acc_best = model_best.evaluate(test_images_flat, test_labels, verbose=0)
print(f"\nBest Architecture Test Accuracy: {test_acc_best:.4f} ({test_acc_best*100:.2f}%)")

# ============================================================================
# 7. TRAIN MANUALLY DESIGNED BASELINE
# ============================================================================
print("\n6. TRAINING MANUALLY DESIGNED BASELINE (FOR COMPARISON)")
print("-" * 70)

# Manual architecture: 2 layers, [128, 64], ReLU, 0.2 dropout
manual_n_layers = 2
manual_neurons = [128, 64]
manual_activation = 'relu'
manual_dropout = 0.2

print(f"Manual architecture:")
print(f"  Layers: {manual_n_layers}")
print(f"  Neurons: {manual_neurons}")
print(f"  Activation: {manual_activation}")
print(f"  Dropout: {manual_dropout}")

model_manual = build_model_from_architecture(manual_n_layers, manual_neurons,
                                            manual_activation, manual_dropout)
model_manual.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

history_manual = model_manual.fit(
    train_images_flat, train_labels,
    epochs=10,
    batch_size=32,
    validation_split=0.2,
    verbose=1
)

test_loss_manual, test_acc_manual = model_manual.evaluate(test_images_flat, test_labels, verbose=0)
print(f"\nManual Architecture Test Accuracy: {test_acc_manual:.4f} ({test_acc_manual*100:.2f}%)")

# ============================================================================
# 8. COMPARISON AND ANALYSIS
# ============================================================================
print("\n" + "=" * 70)
print("COMPARISON: PSO-OPTIMIZED VS MANUALLY DESIGNED ARCHITECTURE")
print("=" * 70)

print("\n7. ARCHITECTURE COMPARISON")
print("-" * 70)
print(f"{'Component':<20} {'Manual':<30} {'PSO-Optimized':<30}")
print("-" * 70)
print(f"{'Layers':<20} {manual_n_layers:<30} {best_n_layers:<30}")
print(f"{'Neurons':<20} {str(manual_neurons):<30} {str(best_neurons):<30}")
print(f"{'Activation':<20} {manual_activation:<30} {best_activation:<30}")
print(f"{'Dropout':<20} {manual_dropout:<30.4f} {best_dropout:<30.4f}")

# Count parameters
manual_params = model_manual.count_params()
best_params = model_best.count_params()

print(f"{'Total Parameters':<20} {manual_params:<30,} {best_params:<30,}")

print("\n8. PERFORMANCE COMPARISON")
print("-" * 70)
print(f"{'Metric':<30} {'Manual':<15} {'PSO-Optimized':<15} {'Improvement'}")
print("-" * 70)
print(f"{'Test Accuracy':<30} {test_acc_manual:.4f}        {test_acc_best:.4f}        {(test_acc_best - test_acc_manual)*100:+.2f}%")

if test_acc_best > test_acc_manual:
    print(f"\n[OK] PSO-optimized architecture achieves better performance")
else:
    print(f"\n[OK] Manual architecture performs similarly or better")

# ============================================================================
# 9. VISUALIZATION
# ============================================================================

fig = plt.figure(figsize=(16, 10))
gs = fig.add_gridspec(3, 2, hspace=0.3, wspace=0.3)

# Plot 1: PSO Convergence
ax1 = fig.add_subplot(gs[0, 0])
ax1.plot(pso.fitness_history, linewidth=2, marker='o', markersize=5)
ax1.set_title('Architecture Search Convergence', fontsize=12, fontweight='bold')
ax1.set_xlabel('Iteration', fontsize=10)
ax1.set_ylabel('Best Validation Accuracy', fontsize=10)
ax1.grid(True, alpha=0.3)
ax1.set_ylim([0.9, 1.0])

# Plot 2: Number of layers evolution
ax2 = fig.add_subplot(gs[0, 1])
layers_history = [arch['n_layers'] for arch in pso.architecture_history]
ax2.plot(layers_history, linewidth=2, marker='s', markersize=5, color='green')
ax2.set_title('Number of Layers Evolution', fontsize=12, fontweight='bold')
ax2.set_xlabel('Iteration', fontsize=10)
ax2.set_ylabel('Number of Layers', fontsize=10)
ax2.set_yticks([1, 2, 3])
ax2.grid(True, alpha=0.3)

# Plot 3: Training comparison
ax3 = fig.add_subplot(gs[1, 0])
ax3.plot(history_manual.history['val_accuracy'], label='Manual', linewidth=2)
ax3.plot(history_best.history['val_accuracy'], label='PSO-Optimized', linewidth=2)
ax3.set_title('Validation Accuracy Comparison', fontsize=12, fontweight='bold')
ax3.set_xlabel('Epoch', fontsize=10)
ax3.set_ylabel('Validation Accuracy', fontsize=10)
ax3.legend()
ax3.grid(True, alpha=0.3)

# Plot 4: Loss comparison
ax4 = fig.add_subplot(gs[1, 1])
ax4.plot(history_manual.history['val_loss'], label='Manual', linewidth=2)
ax4.plot(history_best.history['val_loss'], label='PSO-Optimized', linewidth=2)
ax4.set_title('Validation Loss Comparison', fontsize=12, fontweight='bold')
ax4.set_xlabel('Epoch', fontsize=10)
ax4.set_ylabel('Validation Loss', fontsize=10)
ax4.legend()
ax4.grid(True, alpha=0.3)

# Plot 5: Architecture visualization
ax5 = fig.add_subplot(gs[2, 0])
arch_names = ['Manual', 'PSO-Best']
arch_acc = [test_acc_manual, test_acc_best]
colors = ['blue', 'green']

bars = ax5.bar(arch_names, arch_acc, color=colors, alpha=0.7, edgecolor='black', linewidth=2)
for bar in bars:
    height = bar.get_height()
    ax5.text(bar.get_x() + bar.get_width()/2., height,
             f'{height:.4f}', ha='center', va='bottom', fontweight='bold', fontsize=11)

ax5.set_title('Test Accuracy Comparison', fontsize=12, fontweight='bold')
ax5.set_ylabel('Test Accuracy', fontsize=10)
ax5.set_ylim([0.96, 0.99])
ax5.grid(True, alpha=0.3, axis='y')

# Plot 6: Parameter count comparison
ax6 = fig.add_subplot(gs[2, 1])
param_names = ['Manual', 'PSO-Best']
param_counts = [manual_params, best_params]
colors_params = ['blue', 'green']

bars2 = ax6.bar(param_names, param_counts, color=colors_params, alpha=0.7, edgecolor='black', linewidth=2)
for bar in bars2:
    height = bar.get_height()
    ax6.text(bar.get_x() + bar.get_width()/2., height,
             f'{int(height):,}', ha='center', va='bottom', fontweight='bold', fontsize=10)

ax6.set_title('Model Complexity (Parameters)', fontsize=12, fontweight='bold')
ax6.set_ylabel('Number of Parameters', fontsize=10)
ax6.grid(True, alpha=0.3, axis='y')

plt.savefig(f"{output_dir}/architecture_search_results.png", dpi=300, bbox_inches='tight')
print(f"\nVisualization saved to: {output_dir}/architecture_search_results.png")
plt.close()

# Save detailed results
with open(f"{output_dir}/architecture_search_results.txt", 'w') as f:
    f.write("PSO-Based Neural Architecture Search Results\n")
    f.write("=" * 70 + "\n\n")
    f.write("Best Architecture Found:\n")
    f.write(f"  Number of Layers: {best_n_layers}\n")
    f.write(f"  Neurons per Layer: {best_neurons}\n")
    f.write(f"  Activation Function: {best_activation}\n")
    f.write(f"  Dropout Rate: {best_dropout:.4f}\n")
    f.write(f"  Total Parameters: {best_params:,}\n\n")
    f.write("Manual Baseline Architecture:\n")
    f.write(f"  Number of Layers: {manual_n_layers}\n")
    f.write(f"  Neurons per Layer: {manual_neurons}\n")
    f.write(f"  Activation Function: {manual_activation}\n")
    f.write(f"  Dropout Rate: {manual_dropout:.4f}\n")
    f.write(f"  Total Parameters: {manual_params:,}\n\n")
    f.write("Performance Comparison:\n")
    f.write(f"  Manual Test Accuracy: {test_acc_manual:.4f}\n")
    f.write(f"  PSO-Optimized Test Accuracy: {test_acc_best:.4f}\n")
    f.write(f"  Improvement: {(test_acc_best - test_acc_manual)*100:+.2f}%\n\n")
    f.write(f"Search Time: {search_time:.2f}s ({search_time/60:.1f} min)\n\n")
    f.write("Architecture Evolution:\n")
    for arch in pso.architecture_history[::5]:  # Every 5 iterations
        f.write(f"  Iteration {arch['iteration']}: "
                f"Layers={arch['n_layers']}, "
                f"Neurons={arch['neurons']}, "
                f"Act={arch['activation']}, "
                f"Acc={arch['fitness']:.4f}\n")

print(f"Results saved to: {output_dir}/architecture_search_results.txt")

print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)
print("[OK] PSO-based Neural Architecture Search completed")
print(f"[OK] Best architecture found in {search_time/60:.1f} minutes")
print(f"[OK] PSO-optimized architecture: {test_acc_best*100:.2f}% test accuracy")
print(f"[OK] Manual baseline: {test_acc_manual*100:.2f}% test accuracy")
print(f"[OK] Improvement: {(test_acc_best - test_acc_manual)*100:+.2f}%")
print(f"[OK] All outputs saved to: {output_dir}/")
print("=" * 70)
