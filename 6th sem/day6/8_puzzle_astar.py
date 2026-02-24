"""
8-Puzzle Solver using A* Algorithm
The puzzle is represented as a 3x3 grid with numbers 1-8 and one empty space (0)
Goal state: [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
"""

import heapq
from copy import deepcopy

class PuzzleNode:
    def __init__(self, state, parent=None, move=None, depth=0):
        self.state = state
        self.parent = parent
        self.move = move
        self.depth = depth
        self.cost = depth + self.heuristic()
        
    def heuristic(self):
        """Manhattan distance heuristic"""
        distance = 0
        goal_positions = {
            1: (0, 0), 2: (0, 1), 3: (0, 2),
            4: (1, 0), 5: (1, 1), 6: (1, 2),
            7: (2, 0), 8: (2, 1), 0: (2, 2)
        }
        
        for i in range(3):
            for j in range(3):
                value = self.state[i][j]
                if value != 0:
                    goal_i, goal_j = goal_positions[value]
                    distance += abs(i - goal_i) + abs(j - goal_j)
        return distance
    
    def __lt__(self, other):
        return self.cost < other.cost
    
    def __eq__(self, other):
        return self.state == other.state
    
    def __hash__(self):
        return hash(str(self.state))
    
    def get_blank_position(self):
        """Find the position of the blank tile (0)"""
        for i in range(3):
            for j in range(3):
                if self.state[i][j] == 0:
                    return i, j
        return None
    
    def get_possible_moves(self):
        """Generate all possible moves from current state"""
        moves = []
        i, j = self.get_blank_position()
        
        # Possible directions: UP, DOWN, LEFT, RIGHT
        directions = [(-1, 0, 'UP'), (1, 0, 'DOWN'), (0, -1, 'LEFT'), (0, 1, 'RIGHT')]
        
        for di, dj, move_name in directions:
            new_i, new_j = i + di, j + dj
            if 0 <= new_i < 3 and 0 <= new_j < 3:
                # Create new state
                new_state = deepcopy(self.state)
                # Swap blank with adjacent tile
                new_state[i][j], new_state[new_i][new_j] = new_state[new_i][new_j], new_state[i][j]
                moves.append((new_state, move_name))
        
        return moves
    
    def is_goal(self):
        """Check if current state is the goal state"""
        goal = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
        return self.state == goal
    
    def print_state(self):
        """Print the puzzle state in a nice format"""
        for row in self.state:
            print(' '.join(str(x) if x != 0 else '_' for x in row))
        print()


def solve_8_puzzle(initial_state):
    """
    Solve 8-puzzle using A* algorithm
    Returns the solution path and number of nodes explored
    """
    start_node = PuzzleNode(initial_state)
    
    if start_node.is_goal():
        return [start_node], 0
    
    # Priority queue for open list
    open_list = []
    heapq.heappush(open_list, start_node)
    
    # Closed list to track visited states
    closed_list = set()
    
    nodes_explored = 0
    
    while open_list:
        # Get node with lowest cost
        current_node = heapq.heappop(open_list)
        
        # Add to closed list
        state_tuple = str(current_node.state)
        if state_tuple in closed_list:
            continue
        
        closed_list.add(state_tuple)
        nodes_explored += 1
        
        # Check if goal reached
        if current_node.is_goal():
            # Reconstruct path
            path = []
            node = current_node
            while node:
                path.append(node)
                node = node.parent
            return path[::-1], nodes_explored
        
        # Generate successor nodes
        for new_state, move in current_node.get_possible_moves():
            new_node = PuzzleNode(new_state, current_node, move, current_node.depth + 1)
            
            if str(new_state) not in closed_list:
                heapq.heappush(open_list, new_node)
    
    return None, nodes_explored


def print_solution(path, nodes_explored):
    """Print the solution path"""
    if path is None:
        print("No solution found!")
        return
    
    print("=" * 50)
    print("8-PUZZLE SOLVER USING A* ALGORITHM")
    print("=" * 50)
    print(f"\nSolution found in {len(path) - 1} moves")
    print(f"Nodes explored: {nodes_explored}")
    print(f"\nSolution path:\n")
    
    for i, node in enumerate(path):
        if i == 0:
            print(f"Initial State:")
        else:
            print(f"Step {i} - Move: {node.move}")
        node.print_state()
        print(f"Cost (f = g + h): {node.cost} (g={node.depth}, h={node.heuristic()})")
        print()


if __name__ == "__main__":
    # Example 1: Easy puzzle (few moves required)
    print("\n" + "=" * 50)
    print("EXAMPLE 1: Easy Puzzle")
    print("=" * 50)
    initial_state_1 = [
        [1, 2, 3],
        [4, 5, 6],
        [0, 7, 8]
    ]
    
    path1, nodes1 = solve_8_puzzle(initial_state_1)
    print_solution(path1, nodes1)
    
    # Example 2: Medium difficulty puzzle
    print("\n" + "=" * 50)
    print("EXAMPLE 2: Medium Puzzle")
    print("=" * 50)
    initial_state_2 = [
        [1, 2, 3],
        [4, 0, 6],
        [7, 5, 8]
    ]
    
    path2, nodes2 = solve_8_puzzle(initial_state_2)
    print_solution(path2, nodes2)
    
    # Example 3: More challenging puzzle
    print("\n" + "=" * 50)
    print("EXAMPLE 3: Challenging Puzzle")
    print("=" * 50)
    initial_state_3 = [
        [1, 2, 3],
        [0, 4, 6],
        [7, 5, 8]
    ]
    
    path3, nodes3 = solve_8_puzzle(initial_state_3)
    print_solution(path3, nodes3)
    
    # Example 4: Another challenging configuration
    print("\n" + "=" * 50)
    print("EXAMPLE 4: Random Configuration")
    print("=" * 50)
    initial_state_4 = [
        [1, 2, 3],
        [5, 6, 0],
        [7, 8, 4]
    ]
    
    path4, nodes4 = solve_8_puzzle(initial_state_4)
    print_solution(path4, nodes4)
    
    print("\n" + "=" * 50)
    print("All examples completed!")
    print("=" * 50)
