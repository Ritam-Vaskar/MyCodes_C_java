# Algorithm: Matrix Path Finding

## Problem Statement
Generate an m×m matrix with 80% ones and 20% zeros randomly distributed, then find all possible paths from top-left (0,0) to bottom-right (m-1, m-1) that only traverse through cells containing 1.

---

## Algorithm 1: Generate Matrix with 80% Ones

**Input:** Matrix size `m`  
**Output:** m×m matrix with 80% ones, 20% zeros

```
ALGORITHM generate_matrix(m):
    1. total_elements ← m × m
    2. num_ones ← floor(total_elements × 0.8)
    3. num_zeros ← total_elements - num_ones
    
    4. Create array with num_ones 1's and num_zeros 0's
    5. Randomly shuffle the array
    6. Reshape array into m×m matrix
    
    7. RETURN matrix
```

**Time Complexity:** O(m²)  
**Space Complexity:** O(m²)

---

## Algorithm 2: Count Possible Paths (Dynamic Programming)

**Input:** Matrix of 0s and 1s  
**Output:** Total count of valid paths

```
ALGORITHM possible_paths(matrix):
    1. m ← number of rows
    2. n ← number of columns
    3. Create dp[m][n] initialized with 0
    4. dp[0][0] ← 1  // Starting point has 1 path
    
    5. FOR i = 0 TO m-1:
        FOR j = 0 TO n-1:
            IF matrix[i][j] == 1:
                IF i > 0:
                    dp[i][j] += dp[i-1][j]  // Add paths from top
                IF j > 0:
                    dp[i][j] += dp[i][j-1]  // Add paths from left
    
    6. RETURN dp[m-1][n-1]
```

**Explanation:**
- `dp[i][j]` = number of ways to reach cell (i,j) from (0,0)
- Can only move RIGHT or DOWN
- Only traverse cells with value 1
- Bottom-right cell contains total path count

**Time Complexity:** O(m × n)  
**Space Complexity:** O(m × n)

---

## Algorithm 3: Print All Paths (Backtracking/DFS)

**Input:** Matrix, starting position (i, j), current path  
**Output:** Prints all valid paths

```
ALGORITHM print_path(matrix, i, j, path):
    // Base case: Invalid cell
    1. IF matrix[i][j] == 0:
        RETURN  // Cannot traverse through 0
    
    // Add current position to path
    2. path ← path + "(i,j)"
    
    // Base case: Reached destination
    3. IF i == m-1 AND j == n-1:
        PRINT path
        RETURN
    
    // Recursive case: Try moving DOWN
    4. IF i < m-1 AND matrix[i+1][j] == 1:
        print_path(matrix, i+1, j, path + "->")
    
    // Recursive case: Try moving RIGHT
    5. IF j < n-1 AND matrix[i][j+1] == 1:
        print_path(matrix, i, j+1, path + "->")
```

**Initial Call:** `print_path(matrix, 0, 0, "")`

**Explanation:**
- Uses Depth-First Search (DFS) with backtracking
- At each cell, tries two directions: DOWN and RIGHT
- Only proceeds if next cell contains 1
- Prints complete path when reaching bottom-right
- Naturally backtracks when hitting dead ends

**Time Complexity:** O(2^(m+n)) worst case (exponential)  
**Space Complexity:** O(m + n) for recursion stack

---

## Complete Workflow

```
START
    ↓
1. INPUT: Get matrix size m
    ↓
2. GENERATE: Create m×m matrix with 80% ones, 20% zeros
    ↓
3. DISPLAY: Show matrix
    ↓
4. STATISTICS: Count and show percentage of 1s and 0s
    ↓
5. COUNT PATHS: Use DP to count total possible paths
    ↓
6. PRINT PATHS: Use DFS to print all valid paths
    ↓
END
```

---

## Example Walkthrough

**Matrix (3×3):**
```
[1  1  0]
[1  0  1]
[1  1  1]
```

**Step 1: Count Paths (DP)**
```
DP Table:
[1  1  0]  ← dp values
[1  0  0]
[1  1  1]
```
- (0,0): 1 path (starting point)
- (0,1): 1 path (from left)
- (1,0): 1 path (from top)
- (2,0): 1 path (from top)
- (2,1): 1 path (from left)
- (2,2): 1 path (from left, since top is 0)

**Total paths: 1**

**Step 2: Print Paths (DFS)**

Starting at (0,0):
- Try DOWN to (1,0) ✓ → Try DOWN to (2,0) ✓
  - At (2,0): Try RIGHT to (2,1) ✓
    - At (2,1): Try RIGHT to (2,2) ✓ → **DESTINATION!**
    - **Path found:** (0,0)->(1,0)->(2,0)->(2,1)->(2,2)
- Try RIGHT to (0,1) ✓
  - Try DOWN to (1,1) ✗ (value is 0, blocked)
  - Try RIGHT to (0,2) ✗ (value is 0, blocked)
  - Dead end, backtrack

**Valid Paths:**
1. (0,0)->(1,0)->(2,0)->(2,1)->(2,2)

---

## Key Constraints

1. **Movement:** Only RIGHT (j+1) or DOWN (i+1)
2. **Valid cells:** Only traverse cells with value 1
3. **Start:** Always (0,0)
4. **End:** Always (m-1, n-1)
5. **No diagonal movement**

---

## Complexity Summary

| Algorithm | Time | Space |
|-----------|------|-------|
| Generate Matrix | O(m²) | O(m²) |
| Count Paths (DP) | O(m²) | O(m²) |
| Print Paths (DFS) | O(2^(m+n)) | O(m+n) |
