import random
from itertools import permutations


class HillClimbingTSP:
    def __init__(self, cities, distance_matrix):
        self.cities = cities
        self.distance_matrix = distance_matrix
        self.n = len(cities)
    
    def calculate_tour_cost(self, tour):
        cost = 0
        for i in range(len(tour) - 1):
            cost += self.distance_matrix[tour[i]][tour[i + 1]]
        return cost
    
    def get_neighbors(self, tour):
        neighbors = []
        for i in range(len(tour)):
            for j in range(i + 1, len(tour)):
                neighbor = tour.copy()
                neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
                neighbors.append(neighbor)
        return neighbors
    
    def hill_climbing(self, initial_tour=None, max_iterations=1000):
        if initial_tour is None:
            current_tour = list(range(self.n))
            random.shuffle(current_tour)
        else:
            current_tour = initial_tour.copy()
        
        current_cost = self.calculate_tour_cost(current_tour)
        iteration = 0
        
        print(f"Initial Tour: {self.tour_to_string(current_tour)}")
        print(f"Initial Cost: {current_cost} km\n")
        
        while iteration < max_iterations:
            neighbors = self.get_neighbors(current_tour)
            
            best_neighbor = None
            best_neighbor_cost = current_cost
            
            for neighbor in neighbors:
                neighbor_cost = self.calculate_tour_cost(neighbor)
                if neighbor_cost < best_neighbor_cost:
                    best_neighbor = neighbor
                    best_neighbor_cost = neighbor_cost
            
            if best_neighbor is None:
                print(f"Local optimum reached at iteration {iteration}")
                break
            
            current_tour = best_neighbor
            current_cost = best_neighbor_cost
            iteration += 1
            
            print(f"Iteration {iteration}: {self.tour_to_string(current_tour)} - Cost: {current_cost} km")
        
        return current_tour, current_cost, iteration
    
    def tour_to_string(self, tour):
        city_names = [self.cities[i] for i in tour]
        return " -> ".join(city_names)
    
    def find_all_tours(self):
        all_tours = []
        for perm in permutations(range(self.n)):
            tour = list(perm)
            cost = self.calculate_tour_cost(tour)
            all_tours.append((tour, cost))
        
        all_tours.sort(key=lambda x: x[1])
        return all_tours


def main():
    cities = ['A', 'B', 'C']
    
    distance_matrix = [
        [0, 3, 2],
        [3, 0, 1],
        [2, 1, 0]
    ]
    
    print("=" * 60)
    print("Hill Climbing Algorithm for TSP")
    print("=" * 60)
    print(f"Cities: {', '.join(cities)}")
    print("\nDistance Matrix:")
    print("     A  B  C")
    for i, city in enumerate(cities):
        row = f"{city}    " + "  ".join(str(distance_matrix[i][j]) for j in range(len(cities)))
        print(row)
    print("\n" + "=" * 60)
    
    tsp = HillClimbingTSP(cities, distance_matrix)
    
    print("\nAll Possible Tours:")
    print("-" * 60)
    all_tours = tsp.find_all_tours()
    for i, (tour, cost) in enumerate(all_tours, 1):
        tour_str = tsp.tour_to_string(tour)
        print(f"{i}. {tour_str} | Total Cost: {cost} km")
    print("-" * 60)
    
    optimal_tour, optimal_cost = all_tours[0]
    print(f"\n✓ Most Efficient Tour: {tsp.tour_to_string(optimal_tour)}")
    print(f"✓ Minimum Cost: {optimal_cost} km")
    
    print("\n" + "=" * 60)
    print("Running Hill Climbing Algorithm")
    print("=" * 60 + "\n")
    
    test_cases = [
        [0, 1, 2],
        [0, 2, 1],
        [1, 0, 2],
        [1, 2, 0],
        [2, 0, 1],
        [2, 1, 0],
    ]
    
    results = []
    for i, initial in enumerate(test_cases, 1):
        print(f"\nTest Case {i}:")
        print("-" * 60)
        best_tour, best_cost, iterations = tsp.hill_climbing(initial_tour=initial)
        results.append((best_tour, best_cost, iterations))
        print(f"Final Tour: {tsp.tour_to_string(best_tour)}")
        print(f"Final Cost: {best_cost} km")
        print(f"Iterations: {iterations}")
        print("-" * 60)
    
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    print(f"\nOptimal Solution (Verified): {tsp.tour_to_string(optimal_tour)} = {optimal_cost} km")
    
    successful = sum(1 for tour, cost, _ in results if cost == optimal_cost)
    print(f"\nHill Climbing Success Rate: {successful}/{len(test_cases)} ({successful/len(test_cases)*100:.1f}%)")
    
    print("\nConclusion:")
    print(f"The most efficient tour is: {tsp.tour_to_string(optimal_tour)}")
    print(f"Total distance: {optimal_cost} km")
    
    path_details = []
    for i in range(len(optimal_tour) - 1):
        from_city = cities[optimal_tour[i]]
        to_city = cities[optimal_tour[i + 1]]
        distance = distance_matrix[optimal_tour[i]][optimal_tour[i + 1]]
        path_details.append(f"{from_city} --[{distance} km]--> {to_city}")
    
    print("\nDetailed Path:")
    for detail in path_details:
        print(f"  {detail}")


if __name__ == "__main__":
    main()
