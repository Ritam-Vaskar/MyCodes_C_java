"""
Q2: Treasure Hunt using Best-First Search
Problem: Find treasure in a grid using Manhattan distance as heuristic
The algorithm always moves to the most promising cell first (minimum heuristic value)
"""

import heapq
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle
from matplotlib.animation import FuncAnimation
import time


class TreasureGrid:
    """Represents a grid with a hidden treasure"""
    
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.treasure_pos = None
        self.start_pos = None
        self.obstacles = set()
        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]
    
    def set_treasure(self, row, col):
        """Set the treasure position"""
        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.treasure_pos = (row, col)
            self.grid[row][col] = 2  # 2 represents treasure
        else:
            raise ValueError("Treasure position out of bounds")
    
    def set_start(self, row, col):
        """Set the starting position"""
        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.start_pos = (row, col)
            self.grid[row][col] = 1  # 1 represents start
        else:
            raise ValueError("Start position out of bounds")
    
    def add_obstacle(self, row, col):
        """Add an obstacle to the grid"""
        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.obstacles.add((row, col))
            self.grid[row][col] = -1  # -1 represents obstacle
    
    def is_valid_position(self, row, col):
        """Check if a position is valid and not an obstacle"""
        return (0 <= row < self.rows and 
                0 <= col < self.cols and 
                (row, col) not in self.obstacles)
    
    def get_neighbors(self, row, col):
        """Get all valid neighboring cells (4-directional movement)"""
        neighbors = []
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up
        
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if self.is_valid_position(new_row, new_col):
                neighbors.append((new_row, new_col))
        
        return neighbors


def manhattan_distance(pos1, pos2):
    """
    Calculate Manhattan distance between two positions
    Manhattan distance = |x1 - x2| + |y1 - y2|
    """
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])


def best_first_search(grid, start, treasure):
    """
    Best-First Search using Manhattan distance as heuristic
    Always explores the cell with minimum heuristic value first
    
    Returns: (path, explored_cells, priority_queue_states)
    """
    # Priority queue: (heuristic_value, position)
    pq = []
    heapq.heappush(pq, (manhattan_distance(start, treasure), start))
    
    # Track visited cells and parent for path reconstruction
    visited = {start: None}
    explored_order = [start]
    
    # For visualization
    pq_states = []
    
    while pq:
        # Store current priority queue state for visualization
        pq_states.append([(h, pos) for h, pos in pq])
        
        # Get cell with minimum heuristic value
        current_heuristic, current_pos = heapq.heappop(pq)
        
        # Check if treasure found
        if current_pos == treasure:
            # Reconstruct path
            path = []
            node = treasure
            while node is not None:
                path.append(node)
                node = visited[node]
            path.reverse()
            return path, explored_order, pq_states
        
        # Explore neighbors
        for neighbor in grid.get_neighbors(current_pos[0], current_pos[1]):
            if neighbor not in visited:
                visited[neighbor] = current_pos
                explored_order.append(neighbor)
                
                # Calculate heuristic and add to priority queue
                h_value = manhattan_distance(neighbor, treasure)
                heapq.heappush(pq, (h_value, neighbor))
    
    # Treasure not found
    return None, explored_order, pq_states


def visualize_grid(grid, path=None, explored=None, current=None, title="Treasure Hunt"):
    """Visualize the grid with path and explored cells"""
    fig, ax = plt.subplots(figsize=(10, 10))
    
    # Create color map
    grid_array = np.array(grid.grid)
    
    # Base grid
    ax.imshow(grid_array, cmap='gray_r', alpha=0.3)
    
    # Color cells
    for i in range(grid.rows):
        for j in range(grid.cols):
            # Obstacles
            if (i, j) in grid.obstacles:
                rect = Rectangle((j-0.5, i-0.5), 1, 1, 
                               facecolor='black', alpha=0.8)
                ax.add_patch(rect)
            # Explored cells
            elif explored and (i, j) in explored and (i, j) != grid.start_pos:
                rect = Rectangle((j-0.5, i-0.5), 1, 1, 
                               facecolor='lightblue', alpha=0.5)
                ax.add_patch(rect)
            # Path cells
            if path and (i, j) in path and (i, j) not in [grid.start_pos, grid.treasure_pos]:
                rect = Rectangle((j-0.5, i-0.5), 1, 1, 
                               facecolor='yellow', alpha=0.7)
                ax.add_patch(rect)
    
    # Mark start position
    if grid.start_pos:
        ax.plot(grid.start_pos[1], grid.start_pos[0], 'go', 
               markersize=20, label='Start')
    
    # Mark treasure position
    if grid.treasure_pos:
        ax.plot(grid.treasure_pos[1], grid.treasure_pos[0], 'r*', 
               markersize=30, label='Treasure')
    
    # Mark current position
    if current:
        ax.plot(current[1], current[0], 'bo', 
               markersize=15, alpha=0.7, label='Current')
    
    # Draw path
    if path and len(path) > 1:
        path_x = [pos[1] for pos in path]
        path_y = [pos[0] for pos in path]
        ax.plot(path_x, path_y, 'r-', linewidth=3, alpha=0.6)
    
    # Grid lines
    ax.set_xticks(np.arange(-0.5, grid.cols, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, grid.rows, 1), minor=True)
    ax.grid(which='minor', color='gray', linestyle='-', linewidth=0.5)
    ax.tick_params(which='minor', size=0)
    
    # Labels
    ax.set_xticks(range(grid.cols))
    ax.set_yticks(range(grid.rows))
    ax.set_xlabel('Column', fontsize=12)
    ax.set_ylabel('Row', fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.legend(loc='upper right')
    
    plt.tight_layout()
    return fig, ax


def visualize_heuristic_values(grid, treasure_pos):
    """Visualize the Manhattan distance heuristic values for all cells"""
    fig, ax = plt.subplots(figsize=(12, 10))
    
    # Calculate heuristic values for all cells
    heuristic_grid = np.zeros((grid.rows, grid.cols))
    for i in range(grid.rows):
        for j in range(grid.cols):
            if (i, j) in grid.obstacles:
                heuristic_grid[i][j] = -1
            else:
                heuristic_grid[i][j] = manhattan_distance((i, j), treasure_pos)
    
    # Create heatmap
    masked_grid = np.ma.masked_where(heuristic_grid == -1, heuristic_grid)
    im = ax.imshow(masked_grid, cmap='RdYlGn_r', alpha=0.8)
    
    # Add colorbar
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('Manhattan Distance to Treasure', fontsize=12)
    
    # Add text annotations
    for i in range(grid.rows):
        for j in range(grid.cols):
            if (i, j) in grid.obstacles:
                text = 'X'
                color = 'white'
            else:
                text = str(int(heuristic_grid[i][j]))
                color = 'black' if heuristic_grid[i][j] > np.max(masked_grid)/2 else 'white'
            
            ax.text(j, i, text, ha='center', va='center', 
                   color=color, fontsize=10, fontweight='bold')
    
    # Mark treasure
    ax.plot(treasure_pos[1], treasure_pos[0], 'r*', 
           markersize=30, label='Treasure')
    
    # Mark start
    if grid.start_pos:
        ax.plot(grid.start_pos[1], grid.start_pos[0], 'go', 
               markersize=20, label='Start')
    
    # Grid lines
    ax.set_xticks(np.arange(-0.5, grid.cols, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, grid.rows, 1), minor=True)
    ax.grid(which='minor', color='white', linestyle='-', linewidth=2)
    
    ax.set_xticks(range(grid.cols))
    ax.set_yticks(range(grid.rows))
    ax.set_xlabel('Column', fontsize=12)
    ax.set_ylabel('Row', fontsize=12)
    ax.set_title('Manhattan Distance Heuristic Values', 
                fontsize=14, fontweight='bold')
    ax.legend(loc='upper right')
    
    plt.tight_layout()
    return fig


def print_search_details(grid, path, explored, pq_states):
    """Print detailed information about the search process"""
    print("\n" + "="*70)
    print("SEARCH DETAILS")
    print("="*70)
    
    print(f"\nGrid Size: {grid.rows} x {grid.cols}")
    print(f"Start Position: {grid.start_pos}")
    print(f"Treasure Position: {grid.treasure_pos}")
    print(f"Number of Obstacles: {len(grid.obstacles)}")
    
    print(f"\nSearch Results:")
    print(f"  Treasure Found: {'Yes' if path else 'No'}")
    if path:
        print(f"  Path Length: {len(path)} steps")
        print(f"  Cells Explored: {len(explored)}")
        print(f"  Efficiency: {len(path)/len(explored)*100:.1f}% (path/explored)")
    
    print(f"\nPath taken:")
    if path:
        for i, pos in enumerate(path):
            h_value = manhattan_distance(pos, grid.treasure_pos)
            print(f"  Step {i}: {pos} (heuristic = {h_value})")
    
    print(f"\nExploration order (first 20 cells):")
    for i, pos in enumerate(explored[:20]):
        h_value = manhattan_distance(pos, grid.treasure_pos)
        print(f"  {i+1}. {pos} (heuristic = {h_value})")
    if len(explored) > 20:
        print(f"  ... and {len(explored)-20} more cells")


def create_sample_scenario_1():
    """Create a simple scenario with no obstacles"""
    grid = TreasureGrid(10, 10)
    grid.set_start(0, 0)
    grid.set_treasure(9, 9)
    return grid, "Simple Grid - No Obstacles"


def create_sample_scenario_2():
    """Create a scenario with obstacles forming a maze"""
    grid = TreasureGrid(15, 15)
    grid.set_start(1, 1)
    grid.set_treasure(13, 13)
    
    # Add wall obstacles
    for i in range(3, 12):
        grid.add_obstacle(i, 5)
        grid.add_obstacle(i, 10)
    
    for j in range(5, 11):
        grid.add_obstacle(3, j)
        grid.add_obstacle(11, j)
    
    # Add some scattered obstacles
    obstacles = [(1, 7), (2, 8), (6, 2), (8, 13), (12, 4)]
    for obs in obstacles:
        grid.add_obstacle(obs[0], obs[1])
    
    return grid, "Complex Maze with Obstacles"


def create_sample_scenario_3():
    """Create a scenario with a spiral pattern"""
    grid = TreasureGrid(12, 12)
    grid.set_start(0, 0)
    grid.set_treasure(6, 6)
    
    # Create spiral obstacles
    for i in range(1, 11):
        grid.add_obstacle(i, 3)
        grid.add_obstacle(i, 8)
    
    for j in range(3, 9):
        grid.add_obstacle(1, j)
        grid.add_obstacle(10, j)
    
    for i in range(3, 9):
        grid.add_obstacle(i, 5)
    
    return grid, "Spiral Pattern"


def run_scenario(grid, scenario_name, save_prefix):
    """Run Best-First Search on a scenario and generate visualizations"""
    print("\n" + "="*70)
    print(f"SCENARIO: {scenario_name}")
    print("="*70)
    
    start_time = time.time()
    path, explored, pq_states = best_first_search(
        grid, grid.start_pos, grid.treasure_pos
    )
    end_time = time.time()
    
    if path:
        print(f"\n✓ Treasure found in {len(path)} steps!")
        print(f"  Execution time: {(end_time - start_time)*1000:.4f} ms")
        print(f"  Total cells explored: {len(explored)}")
    else:
        print("\n✗ Treasure not found!")
    
    # Print detailed search information
    print_search_details(grid, path, explored, pq_states)
    
    # Visualize heuristic values
    print(f"\nGenerating heuristic visualization...")
    fig_heuristic = visualize_heuristic_values(grid, grid.treasure_pos)
    plt.savefig(f'{save_prefix}_heuristic.png', dpi=150, bbox_inches='tight')
    print(f"✓ Saved as '{save_prefix}_heuristic.png'")
    plt.close()
    
    # Visualize final result
    print(f"Generating path visualization...")
    fig_result, _ = visualize_grid(grid, path, explored, 
                                   title=f"{scenario_name} - Best-First Search Result")
    plt.savefig(f'{save_prefix}_result.png', dpi=150, bbox_inches='tight')
    print(f"✓ Saved as '{save_prefix}_result.png'")
    plt.close()
    
    return path, explored


def main():
    """Main function to demonstrate Best-First Search"""
    print("\n" + "="*70)
    print("TREASURE HUNT USING BEST-FIRST SEARCH")
    print("Heuristic: Manhattan Distance")
    print("="*70)
    
    # Run multiple scenarios
    scenarios = [
        (create_sample_scenario_1, "scenario1"),
        (create_sample_scenario_2, "scenario2"),
        (create_sample_scenario_3, "scenario3"),
    ]
    
    results = []
    
    for create_scenario, prefix in scenarios:
        grid, name = create_scenario()
        path, explored = run_scenario(grid, name, prefix)
        results.append({
            'name': name,
            'path_length': len(path) if path else 0,
            'explored': len(explored),
            'success': path is not None
        })
    
    # Summary comparison
    print("\n" + "="*70)
    print("SUMMARY COMPARISON")
    print("="*70)
    print(f"\n{'Scenario':<35} {'Success':<10} {'Path':<8} {'Explored':<10} {'Efficiency'}")
    print("-"*70)
    
    for result in results:
        efficiency = (result['path_length'] / result['explored'] * 100 
                     if result['explored'] > 0 else 0)
        print(f"{result['name']:<35} "
              f"{'Yes' if result['success'] else 'No':<10} "
              f"{result['path_length']:<8} "
              f"{result['explored']:<10} "
              f"{efficiency:.1f}%")
    
    print("\n" + "="*70)
    print("KEY OBSERVATIONS:")
    print("="*70)
    print("1. Best-First Search uses Manhattan distance as heuristic")
    print("2. Always explores the cell with minimum heuristic value first")
    print("3. Efficiently finds treasure by moving towards it greedily")
    print("4. Performance depends on obstacle placement")
    print("5. Not always optimal but very fast for finding a path")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
