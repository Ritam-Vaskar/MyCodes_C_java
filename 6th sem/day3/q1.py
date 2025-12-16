
import numpy as np

def generate_matrix(m):
    total_elements = m * m
    
    num_ones = int(total_elements * 0.8)
    num_zeros = total_elements - num_ones
    
    matrix_elements = np.array([1] * num_ones + [0] * num_zeros)
    
    np.random.shuffle(matrix_elements)
    
    matrix = matrix_elements.reshape(m, m)
    
    return matrix

# def generate_matrixseventy(m):
#     total_elements = m * m
    
#     num_ones = int(total_elements * 0.7)
#     num_zeros = total_elements - num_ones
    
#     matrix_elements = np.array([1] * num_ones + [0] * num_zeros)
    
#     np.random.shuffle(matrix_elements)
    
#     matrix = matrix_elements.reshape(m, m)
    
#     return matrix

def matrix_stats(matrix):
    num_ones = np.sum(matrix == 1)
    num_zeros = np.sum(matrix == 0)
    
    print(f"Number of ones: {num_ones}")
    print(f"Number of zeros: {num_zeros}")

    percentage_ones = (num_ones / (num_ones + num_zeros)) * 100
    print(f"Percentage of ones: {percentage_ones:.2f}%")
    print(f"Percentage of zeros: {100 - percentage_ones:.2f}%")
    return num_ones, num_zeros;

#count all possible paths from start to end point through 1s
def possible_paths(matrix, start_i, start_j, end_i, end_j):
    m = len(matrix)
    n = len(matrix[0])
    dp = [[0 for _ in range(n)] for _ in range(m)]
    
    # Check if start point is valid
    if matrix[start_i][start_j] == 0:
        return 0
    
    dp[start_i][start_j] = 1
    
    for i in range(start_i, m):
        for j in range(start_j if i == start_i else 0, n):
            if matrix[i][j] == 1 and not (i == start_i and j == start_j):
                if i > 0 and i > start_i:
                    dp[i][j] += dp[i - 1][j]
                if j > 0 and (i > start_i or j > start_j):
                    dp[i][j] += dp[i][j - 1]
    
    return dp[end_i][end_j]

#print path index like (0,0)->(0,1)->(1,1)->(1,2)->(2,2)
def print_path(matrix, i, j, end_i, end_j, path):
    if matrix[i][j] == 0:
        return
    path = path + f"({i},{j})"
    
    # Check if reached destination
    if i == end_i and j == end_j:
        print(path)
        return
    
    # Try moving down (i, j) -> (i+1, j)
    if i < len(matrix) - 1 and matrix[i+1][j] == 1:
        print_path(matrix, i + 1, j, end_i, end_j, path + "->")
    
    # Try moving right (i, j) -> (i, j+1)
    if j < len(matrix[0]) - 1 and matrix[i][j+1] == 1:
        print_path(matrix, i, j + 1, end_i, end_j, path + "->")


if __name__ == "__main__":
    
    m = int(input("Enter the size of matrix (m): "))
    
    matrix = generate_matrix(m)
    
    print(f"\n{m}×{m} Matrix with 80% ones and 20% zeros:")
    print(matrix)
    num_ones, num_zeros = matrix_stats(matrix)
    
    # Get start and end points from user
    print("\nEnter start point:")
    start_i = int(input("  Row (0 to {}): ".format(m-1)))
    start_j = int(input("  Column (0 to {}): ".format(m-1)))
    
    print("\nEnter end point:")
    end_i = int(input("  Row (0 to {}): ".format(m-1)))
    end_j = int(input("  Column (0 to {}): ".format(m-1)))
    
    # Validate inputs
    if not (0 <= start_i < m and 0 <= start_j < m and 0 <= end_i < m and 0 <= end_j < m):
        print("\nError: Invalid coordinates!")
    elif matrix[start_i][start_j] == 0:
        print(f"\nError: Start point ({start_i},{start_j}) is 0! Must be 1.")
    elif matrix[end_i][end_j] == 0:
        print(f"\nError: End point ({end_i},{end_j}) is 0! Must be 1.")
    elif end_i < start_i or end_j < start_j:
        print("\nError: End point must be down-right from start point!")
    else:
        num_paths = possible_paths(matrix, start_i, start_j, end_i, end_j)
        print(f"\nNumber of paths from ({start_i},{start_j}) to ({end_i},{end_j}): {num_paths}")
        
        if num_paths > 0:
            print(f"\nAll paths from ({start_i},{start_j}) to ({end_i},{end_j}):")
            print_path(matrix, start_i, start_j, end_i, end_j, "")
        else:
            print("\nNo valid paths found!")
    
    