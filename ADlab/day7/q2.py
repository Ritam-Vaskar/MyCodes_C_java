"""
Question 2: PSO for Neural Network Weight Optimization
- Implement Particle Swarm Optimization algorithm
- Use PSO to optimize neural network weights (instead of backpropagation)
- Compare PSO-trained vs Adam-trained models
- Analyze convergence, accuracy, and computational complexity
"""

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models
import numpy as np
import matplotlib.pyplot as plt
import time
import os

# Create output directory
output_dir = "output/q2"
os.makedirs(output_dir, exist_ok=True)

print("=" * 70)
print("QUESTION 2: PSO FOR NEURAL NETWORK WEIGHT OPTIMIZATION")
print("=" * 70)

# ============================================================================
# 1. LOAD AND PREPARE DATA
# ============================================================================
print("\n1. LOADING AND PREPARING DATA")
print("-" * 70)

# Load MNIST dataset
mnist = keras.datasets.mnist
(train_images, train_labels), (test_images, test_labels) = mnist.load_data()

# Use a subset for faster PSO training
train_size = 5000
test_size = 1000

train_images = train_images[:train_size]
train_labels = train_labels[:train_size]
test_images = test_images[:test_size]
test_labels = test_labels[:test_size]

# Normalize and flatten
train_images_flat = train_images.reshape(-1, 784) / 255.0
test_images_flat = test_images.reshape(-1, 784) / 255.0

print(f"Training samples: {len(train_images)}")
print(f"Test samples: {len(test_images)}")
print(f"Input features: 784")
print(f"Output classes: 10")

# ============================================================================
# 2. DEFINE NEURAL NETWORK ARCHITECTURE
# ============================================================================
print("\n2. NEURAL NETWORK ARCHITECTURE")
print("-" * 70)

input_size = 784
hidden_size = 32
output_size = 10

print(f"Input layer: {input_size} neurons")
print(f"Hidden layer: {hidden_size} neurons")
print(f"Output layer: {output_size} neurons")

# Calculate total number of weights and biases
weights1_size = input_size * hidden_size
biases1_size = hidden_size
weights2_size = hidden_size * output_size
biases2_size = output_size
total_params = weights1_size + biases1_size + weights2_size + biases2_size

print(f"\nParameter breakdown:")
print(f"  Weights (input -> hidden): {weights1_size:,}")
print(f"  Biases (hidden): {biases1_size:,}")
print(f"  Weights (hidden -> output): {weights2_size:,}")
print(f"  Biases (output): {biases2_size:,}")
print(f"  Total parameters: {total_params:,}")

# ============================================================================
# 3. NEURAL NETWORK FORWARD PASS AND FITNESS FUNCTION
# ============================================================================

def softmax(x):
    """Compute softmax values for each set of scores in x."""
    exp_x = np.exp(x - np.max(x, axis=1, keepdims=True))
    return exp_x / np.sum(exp_x, axis=1, keepdims=True)

def forward_pass(X, weights):
    """Forward pass through the neural network."""
    # Decode weights from particle position
    w1 = weights[:weights1_size].reshape(input_size, hidden_size)
    b1 = weights[weights1_size:weights1_size + biases1_size]
    w2 = weights[weights1_size + biases1_size:weights1_size + biases1_size + weights2_size].reshape(hidden_size, output_size)
    b2 = weights[weights1_size + biases1_size + weights2_size:]
    
    # Layer 1: Input → Hidden (ReLU activation)
    z1 = np.dot(X, w1) + b1
    a1 = np.maximum(0, z1)  # ReLU
    
    # Layer 2: Hidden → Output (Softmax activation)
    z2 = np.dot(a1, w2) + b2
    a2 = softmax(z2)
    
    return a2

def fitness_function(weights, X, y):
    """
    Fitness function: Classification error (lower is better)
    Returns the error rate (1 - accuracy)
    """
    predictions = forward_pass(X, weights)
    predicted_labels = np.argmax(predictions, axis=1)
    accuracy = np.mean(predicted_labels == y)
    error = 1 - accuracy
    
    # Add cross-entropy loss for better optimization
    epsilon = 1e-10
    ce_loss = -np.mean(np.log(predictions[np.arange(len(y)), y] + epsilon))
    
    # Combined fitness (weighted sum)
    fitness = error + 0.1 * ce_loss
    return fitness

# ============================================================================
# 4. PARTICLE SWARM OPTIMIZATION IMPLEMENTATION
# ============================================================================
print("\n3. PARTICLE SWARM OPTIMIZATION SETUP")
print("-" * 70)

class PSO:
    def __init__(self, n_particles, n_dimensions, bounds, max_iter=30):
        self.n_particles = n_particles
        self.n_dimensions = n_dimensions
        self.bounds = bounds
        self.max_iter = max_iter
        
        # PSO hyperparameters
        self.w = 0.7  # Inertia weight
        self.c1 = 1.5  # Cognitive parameter
        self.c2 = 1.5  # Social parameter
        
        # Initialize particles
        self.positions = np.random.uniform(bounds[0], bounds[1], 
                                          (n_particles, n_dimensions))
        self.velocities = np.random.uniform(-0.1, 0.1, 
                                           (n_particles, n_dimensions))
        
        # Personal best
        self.pbest_positions = self.positions.copy()
        self.pbest_fitness = np.full(n_particles, float('inf'))
        
        # Global best
        self.gbest_position = None
        self.gbest_fitness = float('inf')
        
        # History
        self.fitness_history = []
        
    def optimize(self, fitness_func, X, y):
        """Run PSO optimization."""
        print(f"\nRunning PSO with {self.n_particles} particles for {self.max_iter} iterations...")
        
        for iteration in range(self.max_iter):
            # Evaluate fitness for all particles
            for i in range(self.n_particles):
                fitness = fitness_func(self.positions[i], X, y)
                
                # Update personal best
                if fitness < self.pbest_fitness[i]:
                    self.pbest_fitness[i] = fitness
                    self.pbest_positions[i] = self.positions[i].copy()
                
                # Update global best
                if fitness < self.gbest_fitness:
                    self.gbest_fitness = fitness
                    self.gbest_position = self.positions[i].copy()
            
            # Store history
            self.fitness_history.append(self.gbest_fitness)
            
            # Update velocities and positions
            for i in range(self.n_particles):
                r1 = np.random.random(self.n_dimensions)
                r2 = np.random.random(self.n_dimensions)
                
                cognitive = self.c1 * r1 * (self.pbest_positions[i] - self.positions[i])
                social = self.c2 * r2 * (self.gbest_position - self.positions[i])
                
                self.velocities[i] = (self.w * self.velocities[i] + 
                                     cognitive + social)
                
                # Update position
                self.positions[i] += self.velocities[i]
                
                # Apply bounds
                self.positions[i] = np.clip(self.positions[i], 
                                           self.bounds[0], self.bounds[1])
            
            if (iteration + 1) % 5 == 0:
                acc = 1 - self.gbest_fitness
                print(f"  Iteration {iteration + 1}/{self.max_iter} - Best Fitness: {self.gbest_fitness:.4f} (Acc: {acc:.4f})")
        
        return self.gbest_position, self.gbest_fitness

# Initialize PSO
n_particles = 20
bounds = (-1, 1)  # Weight bounds
max_iter = 30

print(f"Number of particles: {n_particles}")
print(f"Dimensions (parameters): {total_params:,}")
print(f"Maximum iterations: {max_iter}")
print(f"Weight bounds: [{bounds[0]}, {bounds[1]}]")
print(f"Inertia weight (w): 0.7")
print(f"Cognitive parameter (c1): 1.5")
print(f"Social parameter (c2): 1.5")

# ============================================================================
# 5. TRAIN PSO MODEL
# ============================================================================
print("\n4. TRAINING WITH PSO")
print("-" * 70)

start_time = time.time()
pso = PSO(n_particles=n_particles, n_dimensions=total_params, 
          bounds=bounds, max_iter=max_iter)
best_weights, best_fitness = pso.optimize(fitness_function, train_images_flat, train_labels)
pso_time = time.time() - start_time

print(f"\nPSO Training completed in {pso_time:.2f} seconds")
print(f"Best fitness achieved: {best_fitness:.4f}")

# Evaluate PSO model
pso_train_pred = forward_pass(train_images_flat, best_weights)
pso_train_acc = np.mean(np.argmax(pso_train_pred, axis=1) == train_labels)

pso_test_pred = forward_pass(test_images_flat, best_weights)
pso_test_acc = np.mean(np.argmax(pso_test_pred, axis=1) == test_labels)

print(f"PSO Train Accuracy: {pso_train_acc:.4f} ({pso_train_acc*100:.2f}%)")
print(f"PSO Test Accuracy: {pso_test_acc:.4f} ({pso_test_acc*100:.2f}%)")

# ============================================================================
# 6. TRAIN ADAM MODEL FOR COMPARISON
# ============================================================================
print("\n5. TRAINING WITH ADAM (FOR COMPARISON)")
print("-" * 70)

adam_model = models.Sequential([
    layers.Input(shape=(784,)),
    layers.Dense(32, activation='relu'),
    layers.Dense(10, activation='softmax')
])

adam_model.compile(optimizer='adam',
                   loss='sparse_categorical_crossentropy',
                   metrics=['accuracy'])

start_time = time.time()
adam_history = adam_model.fit(train_images_flat, train_labels, 
                              epochs=30, batch_size=32, 
                              validation_split=0.2, verbose=0)
adam_time = time.time() - start_time

print(f"\nAdam Training completed in {adam_time:.2f} seconds")

# Evaluate Adam model
adam_train_loss, adam_train_acc = adam_model.evaluate(train_images_flat, train_labels, verbose=0)
adam_test_loss, adam_test_acc = adam_model.evaluate(test_images_flat, test_labels, verbose=0)

print(f"Adam Train Accuracy: {adam_train_acc:.4f} ({adam_train_acc*100:.2f}%)")
print(f"Adam Test Accuracy: {adam_test_acc:.4f} ({adam_test_acc*100:.2f}%)")

# ============================================================================
# 7. COMPARISON AND ANALYSIS
# ============================================================================
print("\n" + "=" * 70)
print("COMPARISON AND ANALYSIS")
print("=" * 70)

print("\n1. ACCURACY COMPARISON")
print("-" * 70)
print(f"{'Metric':<25} {'PSO':<15} {'Adam':<15}")
print("-" * 70)
print(f"{'Training Accuracy':<25} {pso_train_acc:.4f}        {adam_train_acc:.4f}")
print(f"{'Test Accuracy':<25} {pso_test_acc:.4f}        {adam_test_acc:.4f}")
print(f"{'Training Time (s)':<25} {pso_time:.2f}          {adam_time:.2f}")

print("\n2. CONVERGENCE SPEED")
print("-" * 70)
print(f"PSO iterations: {max_iter}")
print(f"Adam epochs: 30")
print(f"PSO converged to: {1 - best_fitness:.4f} accuracy")
print(f"Adam converged to: {adam_train_acc:.4f} accuracy")

print("\n3. COMPUTATIONAL COMPLEXITY")
print("-" * 70)
print(f"PSO:")
print(f"  - Time complexity per iteration: O(particles × samples × parameters)")
print(f"  - Space complexity: O(particles × parameters)")
print(f"  - Total time: {pso_time:.2f}s")
print(f"\nAdam:")
print(f"  - Time complexity per epoch: O(samples × parameters)")
print(f"  - Space complexity: O(parameters)")
print(f"  - Total time: {adam_time:.2f}s")

# ============================================================================
# 8. VISUALIZATION
# ============================================================================

# Plot 1: PSO Convergence
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# PSO Fitness convergence
axes[0, 0].plot(pso.fitness_history, linewidth=2, marker='o', markersize=4)
axes[0, 0].set_title('PSO Convergence (Fitness vs Iteration)', fontsize=12, fontweight='bold')
axes[0, 0].set_xlabel('Iteration', fontsize=10)
axes[0, 0].set_ylabel('Fitness (Error)', fontsize=10)
axes[0, 0].grid(True, alpha=0.3)

# PSO Accuracy convergence
pso_acc_history = [1 - f for f in pso.fitness_history]
axes[0, 1].plot(pso_acc_history, linewidth=2, marker='o', markersize=4, color='green')
axes[0, 1].set_title('PSO Convergence (Accuracy vs Iteration)', fontsize=12, fontweight='bold')
axes[0, 1].set_xlabel('Iteration', fontsize=10)
axes[0, 1].set_ylabel('Accuracy', fontsize=10)
axes[0, 1].grid(True, alpha=0.3)

# Adam Training History
axes[1, 0].plot(adam_history.history['accuracy'], label='Train', linewidth=2)
axes[1, 0].plot(adam_history.history['val_accuracy'], label='Validation', linewidth=2)
axes[1, 0].set_title('Adam Training (Accuracy vs Epoch)', fontsize=12, fontweight='bold')
axes[1, 0].set_xlabel('Epoch', fontsize=10)
axes[1, 0].set_ylabel('Accuracy', fontsize=10)
axes[1, 0].legend()
axes[1, 0].grid(True, alpha=0.3)

# Comparison Bar Chart
metrics = ['Train Acc', 'Test Acc']
pso_values = [pso_train_acc, pso_test_acc]
adam_values = [adam_train_acc, adam_test_acc]

x = np.arange(len(metrics))
width = 0.35

axes[1, 1].bar(x - width/2, pso_values, width, label='PSO', color='orange')
axes[1, 1].bar(x + width/2, adam_values, width, label='Adam', color='blue')
axes[1, 1].set_title('Accuracy Comparison', fontsize=12, fontweight='bold')
axes[1, 1].set_ylabel('Accuracy', fontsize=10)
axes[1, 1].set_xticks(x)
axes[1, 1].set_xticklabels(metrics)
axes[1, 1].legend()
axes[1, 1].grid(True, alpha=0.3, axis='y')
axes[1, 1].set_ylim([0, 1])

plt.tight_layout()
plt.savefig(f"{output_dir}/pso_vs_adam_comparison.png", dpi=300, bbox_inches='tight')
print(f"\nComparison plots saved to: {output_dir}/pso_vs_adam_comparison.png")
plt.close()

# Save results
with open(f"{output_dir}/results_summary.txt", 'w') as f:
    f.write("PSO vs Adam Comparison Results\n")
    f.write("=" * 70 + "\n\n")
    f.write(f"PSO Results:\n")
    f.write(f"  Training Accuracy: {pso_train_acc:.4f}\n")
    f.write(f"  Test Accuracy: {pso_test_acc:.4f}\n")
    f.write(f"  Training Time: {pso_time:.2f}s\n\n")
    f.write(f"Adam Results:\n")
    f.write(f"  Training Accuracy: {adam_train_acc:.4f}\n")
    f.write(f"  Test Accuracy: {adam_test_acc:.4f}\n")
    f.write(f"  Training Time: {adam_time:.2f}s\n\n")
    f.write(f"Winner:\n")
    if adam_test_acc > pso_test_acc:
        f.write(f"  Adam achieves higher test accuracy ({adam_test_acc:.4f} vs {pso_test_acc:.4f})\n")
    else:
        f.write(f"  PSO achieves higher test accuracy ({pso_test_acc:.4f} vs {adam_test_acc:.4f})\n")

print(f"Results summary saved to: {output_dir}/results_summary.txt")

print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)
print("[OK] PSO implementation completed")
print("[OK] Adam baseline trained for comparison")
print(f"[OK] PSO achieved {pso_test_acc*100:.2f}% test accuracy")
print(f"[OK] Adam achieved {adam_test_acc*100:.2f}% test accuracy")
print(f"[OK] All results saved to: {output_dir}/")
print("=" * 70)
