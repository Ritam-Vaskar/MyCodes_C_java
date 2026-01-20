import heapq
from collections import defaultdict

class Graph:
    def __init__(self):
        self.graph = defaultdict(list)
    
    def add_edge(self, u, v, cost):
        """Add an edge from node u to node v with given cost"""
        self.graph[u].append((v, cost))
    
    def uniform_cost_search(self, start, goal):
        """
        Uniform Cost Search algorithm
        Returns: path from start to goal and total cost
        """
        # Priority queue: (cost, node, path)
        priority_queue = [(0, start, [start])]
        # Set to track visited nodes
        visited = set()
        
        print(f"\nStarting Uniform Cost Search from '{start}' to '{goal}'")
        print("-" * 60)
        
        while priority_queue:
            # Get the node with minimum cost
            current_cost, current_node, path = heapq.heappop(priority_queue)
            
            print(f"Exploring: {current_node} | Cost: {current_cost} | Path: {' -> '.join(path)}")
            
            # If we reached the goal
            if current_node == goal:
                print("-" * 60)
                print(f"✓ Goal '{goal}' reached!")
                return path, current_cost
            
            # Skip if already visited
            if current_node in visited:
                continue
            
            # Mark as visited
            visited.add(current_node)
            
            # Explore neighbors
            for neighbor, edge_cost in self.graph[current_node]:
                if neighbor not in visited:
                    new_cost = current_cost + edge_cost
                    new_path = path + [neighbor]
                    heapq.heappush(priority_queue, (new_cost, neighbor, new_path))
        
        print("-" * 60)
        print(f"✗ No path found from '{start}' to '{goal}'")
        return None, float('inf')


def example1():
    """Example 1: Simple graph"""
    print("\n" + "="*60)
    print("EXAMPLE 1: Simple Graph")
    print("="*60)
    
    g = Graph()
    # Create a simple graph
    g.add_edge('A', 'B', 4)
    g.add_edge('A', 'C', 2)
    g.add_edge('B', 'C', 1)
    g.add_edge('B', 'D', 5)
    g.add_edge('C', 'D', 8)
    g.add_edge('C', 'E', 10)
    g.add_edge('D', 'E', 2)
    
    print("\nGraph Structure:")
    print("A -> B (cost: 4), C (cost: 2)")
    print("B -> C (cost: 1), D (cost: 5)")
    print("C -> D (cost: 8), E (cost: 10)")
    print("D -> E (cost: 2)")
    
    path, cost = g.uniform_cost_search('A', 'E')
    
    if path:
        print(f"\nOptimal Path: {' -> '.join(path)}")
        print(f"Total Cost: {cost}")


def example2():
    """Example 2: More complex graph"""
    print("\n" + "="*60)
    print("EXAMPLE 2: Complex Graph (Romania Map)")
    print("="*60)
    
    g = Graph()
    # Romanian cities graph (classic AI example)
    g.add_edge('Arad', 'Zerind', 75)
    g.add_edge('Arad', 'Sibiu', 140)
    g.add_edge('Arad', 'Timisoara', 118)
    g.add_edge('Zerind', 'Oradea', 71)
    g.add_edge('Oradea', 'Sibiu', 151)
    g.add_edge('Timisoara', 'Lugoj', 111)
    g.add_edge('Lugoj', 'Mehadia', 70)
    g.add_edge('Mehadia', 'Drobeta', 75)
    g.add_edge('Drobeta', 'Craiova', 120)
    g.add_edge('Sibiu', 'Fagaras', 99)
    g.add_edge('Sibiu', 'Rimnicu', 80)
    g.add_edge('Rimnicu', 'Craiova', 146)
    g.add_edge('Rimnicu', 'Pitesti', 97)
    g.add_edge('Fagaras', 'Bucharest', 211)
    g.add_edge('Craiova', 'Pitesti', 138)
    g.add_edge('Pitesti', 'Bucharest', 101)
    
    print("\nFinding shortest path from Arad to Bucharest...")
    
    path, cost = g.uniform_cost_search('Arad', 'Bucharest')
    
    if path:
        print(f"\nOptimal Path: {' -> '.join(path)}")
        print(f"Total Cost: {cost} km")


def example3():
    """Example 3: Grid-based graph"""
    print("\n" + "="*60)
    print("EXAMPLE 3: Grid Navigation")
    print("="*60)
    
    g = Graph()
    # Create a grid-like graph
    g.add_edge('Start', 'A', 1)
    g.add_edge('Start', 'B', 4)
    g.add_edge('A', 'C', 2)
    g.add_edge('A', 'D', 5)
    g.add_edge('B', 'D', 2)
    g.add_edge('C', 'Goal', 3)
    g.add_edge('D', 'Goal', 1)
    
    print("\nGrid Structure:")
    print("Start -> A (cost: 1), B (cost: 4)")
    print("A -> C (cost: 2), D (cost: 5)")
    print("B -> D (cost: 2)")
    print("C -> Goal (cost: 3)")
    print("D -> Goal (cost: 1)")
    
    path, cost = g.uniform_cost_search('Start', 'Goal')
    
    if path:
        print(f"\nOptimal Path: {' -> '.join(path)}")
        print(f"Total Cost: {cost}")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("UNIFORM COST SEARCH ALGORITHM")
    print("="*60)
    print("\nUniform Cost Search (UCS) is a graph search algorithm that")
    print("explores nodes in order of their cumulative path cost.")
    print("It guarantees finding the optimal (lowest cost) path.")
    
    # Run all examples
    example1()
    example2()
    example3()
    
    print("\n" + "="*60)
    print("All examples completed successfully!")
    print("="*60)
