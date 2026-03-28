import random
import math
import matplotlib.pyplot as plt
import numpy as np


class GeneticAlgorithm:
    def __init__(self, pop_size=30, generations=50, crossover_rate=0.80, 
                 mutation_rate=0.02, tournament_size=3, chromosome_length=20):
        self.pop_size = pop_size
        self.generations = generations
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.tournament_size = tournament_size
        self.chromosome_length = chromosome_length
        self.x_min = 0.0
        self.x_max = 10.0
        
        self.best_fitness_history = []
        self.avg_fitness_history = []
        self.best_solution_history = []
    
    def objective_function(self, x):
        return math.sin(x) + x
    
    def decode_chromosome(self, chromosome):
        decimal_value = int(chromosome, 2)
        
        max_decimal = 2**self.chromosome_length - 1
        x = self.x_min + (decimal_value / max_decimal) * (self.x_max - self.x_min)
        
        return x
    
    def encode_value(self, x):
        max_decimal = 2**self.chromosome_length - 1
        decimal_value = int(((x - self.x_min) / (self.x_max - self.x_min)) * max_decimal)
        chromosome = format(decimal_value, f'0{self.chromosome_length}b')
        return chromosome
    
    def initialize_population(self):
        population = []
        for _ in range(self.pop_size):
            chromosome = ''.join(random.choice('01') for _ in range(self.chromosome_length))
            population.append(chromosome)
        return population
    
    def calculate_fitness(self, chromosome):
        x = self.decode_chromosome(chromosome)
        return self.objective_function(x)
    
    def tournament_selection(self, population, fitness_values):
        tournament_indices = random.sample(range(len(population)), self.tournament_size)
        
        best_idx = max(tournament_indices, key=lambda i: fitness_values[i])
        
        return population[best_idx]
    
    def one_point_crossover(self, parent1, parent2):
        if random.random() < self.crossover_rate:
            point = random.randint(1, self.chromosome_length - 1)
            
            offspring1 = parent1[:point] + parent2[point:]
            offspring2 = parent2[:point] + parent1[point:]
            
            return offspring1, offspring2
        else:
            return parent1, parent2
    
    def bit_flip_mutation(self, chromosome):
        chromosome_list = list(chromosome)
        
        for i in range(len(chromosome_list)):
            if random.random() < self.mutation_rate:
                chromosome_list[i] = '1' if chromosome_list[i] == '0' else '0'
        
        return ''.join(chromosome_list)
    
    def get_statistics(self, population, fitness_values):
        best_fitness = max(fitness_values)
        avg_fitness = sum(fitness_values) / len(fitness_values)
        best_idx = fitness_values.index(best_fitness)
        best_chromosome = population[best_idx]
        best_x = self.decode_chromosome(best_chromosome)
        
        return best_fitness, avg_fitness, best_chromosome, best_x
    
    def run(self, verbose=True):
        population = self.initialize_population()
        
        print("=" * 70)
        print("Genetic Algorithm - Maximizing f(x) = sin(x) + x")
        print("=" * 70)
        print(f"Population Size: {self.pop_size}")
        print(f"Generations: {self.generations}")
        print(f"Chromosome Length: {self.chromosome_length} bits")
        print(f"Crossover Rate: {self.crossover_rate}")
        print(f"Mutation Rate: {self.mutation_rate} (per bit)")
        print(f"Tournament Size: {self.tournament_size}")
        print(f"Range: x ∈ [{self.x_min}, {self.x_max}]")
        print("=" * 70 + "\n")
        
        for generation in range(self.generations):
            fitness_values = [self.calculate_fitness(chr) for chr in population]
            
            best_fitness, avg_fitness, best_chromosome, best_x = self.get_statistics(
                population, fitness_values
            )
            
            self.best_fitness_history.append(best_fitness)
            self.avg_fitness_history.append(avg_fitness)
            self.best_solution_history.append(best_x)
            
            if verbose and (generation == 0 or (generation + 1) % 10 == 0 or 
                          generation == self.generations - 1):
                print(f"Generation {generation + 1:3d} | "
                      f"Best x: {best_x:.6f} | "
                      f"Best f(x): {best_fitness:.6f} | "
                      f"Avg f(x): {avg_fitness:.6f}")
            
            new_population = []
            
            new_population.append(best_chromosome)
            
            while len(new_population) < self.pop_size:
                parent1 = self.tournament_selection(population, fitness_values)
                parent2 = self.tournament_selection(population, fitness_values)
                
                offspring1, offspring2 = self.one_point_crossover(parent1, parent2)
                
                offspring1 = self.bit_flip_mutation(offspring1)
                offspring2 = self.bit_flip_mutation(offspring2)
                
                new_population.append(offspring1)
                if len(new_population) < self.pop_size:
                    new_population.append(offspring2)
            
            population = new_population[:self.pop_size]
        
        fitness_values = [self.calculate_fitness(chr) for chr in population]
        best_fitness, avg_fitness, best_chromosome, best_x = self.get_statistics(
            population, fitness_values
        )
        
        print("\n" + "=" * 70)
        print("Final Results")
        print("=" * 70)
        print(f"Best x found: {best_x:.6f}")
        print(f"Best f(x) = sin({best_x:.6f}) + {best_x:.6f} = {best_fitness:.6f}")
        print(f"Binary representation: {best_chromosome}")
        print("=" * 70)
        
        return best_x, best_fitness
    
    def plot_results(self, save_path=None):
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
        
        generations = range(1, len(self.best_fitness_history) + 1)
        
        ax1.plot(generations, self.best_fitness_history, 'b-', linewidth=2, 
                label='Best Fitness', marker='o', markersize=4, markevery=5)
        ax1.plot(generations, self.avg_fitness_history, 'r--', linewidth=2, 
                label='Average Fitness', marker='s', markersize=4, markevery=5)
        ax1.set_xlabel('Generation', fontsize=12)
        ax1.set_ylabel('Fitness Value', fontsize=12)
        ax1.set_title('Fitness Evolution over Generations', fontsize=14, fontweight='bold')
        ax1.legend(fontsize=10)
        ax1.grid(True, alpha=0.3)
        
        ax2_twin = ax2.twinx()
        
        ax2.plot(generations, self.best_solution_history, 'g-', linewidth=2, 
                label='Best x Value', marker='d', markersize=4, markevery=5)
        ax2.set_xlabel('Generation', fontsize=12)
        ax2.set_ylabel('x Value', fontsize=12, color='g')
        ax2.tick_params(axis='y', labelcolor='g')
        ax2.set_title('Best Solution Evolution', fontsize=14, fontweight='bold')
        ax2.grid(True, alpha=0.3)
        
        x_range = np.linspace(self.x_min, self.x_max, 1000)
        y_range = [self.objective_function(x) for x in x_range]
        ax2_twin.plot(x_range, y_range, 'orange', linewidth=1, alpha=0.3, 
                     label='f(x) = sin(x) + x')
        ax2_twin.set_ylabel('f(x)', fontsize=12, color='orange')
        ax2_twin.tick_params(axis='y', labelcolor='orange')
        
        best_x = self.best_solution_history[-1]
        best_fx = self.best_fitness_history[-1]
        ax2_twin.plot(best_x, best_fx, 'r*', markersize=20, 
                     label=f'Best Solution: x={best_x:.4f}')
        
        lines1, labels1 = ax2.get_legend_handles_labels()
        lines2, labels2 = ax2_twin.get_legend_handles_labels()
        ax2_twin.legend(lines1 + lines2, labels1 + labels2, fontsize=10, loc='lower right')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"\nPlot saved to: {save_path}")
        
        plt.show()


def verify_solution():
    print("\n" + "=" * 70)
    print("Verification: Analytical Analysis")
    print("=" * 70)
    
    x_test = np.linspace(0, 10, 1000)
    y_test = np.sin(x_test) + x_test
    
    max_idx = np.argmax(y_test)
    max_x = x_test[max_idx]
    max_y = y_test[max_idx]
    
    print(f"\nAnalytical maximum (by sampling):")
    print(f"x ≈ {max_x:.6f}")
    print(f"f(x) ≈ {max_y:.6f}")
    print(f"\nNote: Since f'(x) = cos(x) + 1 ≥ 0 for all x,")
    print(f"the function is non-decreasing, so the maximum is at x = {10.0:.1f}")
    print(f"f({10.0:.1f}) = sin({10.0:.1f}) + {10.0:.1f} = {math.sin(10) + 10:.6f}")
    print("=" * 70)


def main():
    random.seed(42)
    
    ga = GeneticAlgorithm(
        pop_size=30,
        generations=50,
        crossover_rate=0.80,
        mutation_rate=0.02,
        tournament_size=3,
        chromosome_length=20
    )
    
    best_x, best_fitness = ga.run(verbose=True)
    
    verify_solution()
    
    try:
        ga.plot_results(save_path="c:\\C programing\\6th sem\\day7\\ga_results.png")
    except Exception as e:
        print(f"\nNote: Could not display plot: {e}")
        print("(This is normal if running without display)")


if __name__ == "__main__":
    main()
