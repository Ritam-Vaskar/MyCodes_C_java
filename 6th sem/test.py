import math
import random
from typing import List, Tuple


def euclidean_distance(a: Tuple[float, float], b: Tuple[float, float]) -> float:
	return math.hypot(a[0] - b[0], a[1] - b[1])


def build_distance_matrix(cities: List[Tuple[float, float]]) -> List[List[float]]:
	n = len(cities)
	matrix = [[0.0] * n for _ in range(n)]
	for i in range(n):
		for j in range(i + 1, n):
			d = euclidean_distance(cities[i], cities[j])
			matrix[i][j] = d
			matrix[j][i] = d
	return matrix


def route_distance(route: List[int], dist: List[List[float]]) -> float:
	total = 0.0
	for i in range(len(route) - 1):
		total += dist[route[i]][route[i + 1]]
	total += dist[route[-1]][route[0]]
	return total


def create_individual(n: int) -> List[int]:
	individual = list(range(n))
	random.shuffle(individual)
	return individual


def initial_population(pop_size: int, n: int) -> List[List[int]]:
	return [create_individual(n) for _ in range(pop_size)]


def tournament_selection(
	population: List[List[int]],
	fitness: List[float],
	k: int = 3,
) -> List[int]:
	participants = random.sample(range(len(population)), k)
	best = min(participants, key=lambda idx: fitness[idx])
	return population[best][:]


def ordered_crossover(parent1: List[int], parent2: List[int]) -> List[int]:
	n = len(parent1)
	left, right = sorted(random.sample(range(n), 2))
	child = [-1] * n
	child[left : right + 1] = parent1[left : right + 1]

	p2_values = [gene for gene in parent2 if gene not in child]
	ptr = 0
	for i in range(n):
		if child[i] == -1:
			child[i] = p2_values[ptr]
			ptr += 1
	return child


def mutate_swap(route: List[int], mutation_rate: float) -> None:
	if random.random() < mutation_rate:
		i, j = random.sample(range(len(route)), 2)
		route[i], route[j] = route[j], route[i]


def genetic_tsp(
	cities: List[Tuple[float, float]],
	pop_size: int = 120,
	generations: int = 500,
	mutation_rate: float = 0.08,
	elite_size: int = 2,
) -> Tuple[List[int], float]:
	n = len(cities)
	if n < 2:
		return list(range(n)), 0.0

	dist = build_distance_matrix(cities)
	population = initial_population(pop_size, n)

	best_route: List[int] = []
	best_distance = float("inf")

	for _ in range(generations):
		fitness = [route_distance(ind, dist) for ind in population]

		generation_best_idx = min(range(pop_size), key=lambda i: fitness[i])
		generation_best_dist = fitness[generation_best_idx]
		if generation_best_dist < best_distance:
			best_distance = generation_best_dist
			best_route = population[generation_best_idx][:]

		ranked_indices = sorted(range(pop_size), key=lambda i: fitness[i])
		new_population = [population[idx][:] for idx in ranked_indices[:elite_size]]

		while len(new_population) < pop_size:
			p1 = tournament_selection(population, fitness, k=3)
			p2 = tournament_selection(population, fitness, k=3)
			child = ordered_crossover(p1, p2)
			mutate_swap(child, mutation_rate)
			new_population.append(child)

		population = new_population

	return best_route, best_distance


def read_cities() -> List[Tuple[float, float]]:
	n = int(input("Enter number of cities: ").strip())
	mode = input("Enter mode (1 = manual coordinates, 2 = random coordinates): ").strip()

	cities: List[Tuple[float, float]] = []

	if mode == "1":
		print("Enter coordinates as: x y")
		for i in range(n):
			x, y = map(float, input(f"City {i} -> ").split())
			cities.append((x, y))
	else:
		limit = float(input("Enter max coordinate value (e.g., 100): ").strip())
		for _ in range(n):
			cities.append((random.uniform(0, limit), random.uniform(0, limit)))

	return cities


def main() -> None:
	random.seed()
	cities = read_cities()

	route, distance = genetic_tsp(
		cities,
		pop_size=150,
		generations=700,
		mutation_rate=0.1,
		elite_size=3,
	)

	if not route:
		print("No route found.")
		return

	print("\nBest route (city indices):")
	print(" -> ".join(map(str, route)) + f" -> {route[0]}")
	print(f"Total distance: {distance:.4f}")


if __name__ == "__main__":
	main()
