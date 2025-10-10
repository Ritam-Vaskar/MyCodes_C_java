# Custom Test Cases Documentation

## Test Case 1: Simple Tree Switching
Input: custom_test1.txt

Tree 0:
  1 -> 2, 3
  2 -> 4

Tree 1:
  5 -> 6
  6 -> 2

Start: 4, Destination: 5

Expected Path Analysis:
- 4 (tree 0) -> 2 (tree 0, UP, +1) = 1
- 2 (switch to tree 1, +1) = 2
- 2 (tree 1) -> 6 (tree 1, UP, +1) = 3
- 6 (tree 1) -> 5 (tree 1, UP, +1) = 4

Expected Output: 4

---

## Test Case 2: Multiple Shared Spots
Input: custom_test2.txt

Tree 0:
  10 -> 20
  20 -> 30, 40

Tree 1:
  50 -> 60
  60 -> 40

Tree 2:
  30 -> 50

Start: 10, Destination: 30

Shared spots: 30 (tree 0, 2), 40 (tree 0, 1)

Expected Path Analysis:
Path 1: 10 -> 20 -> 30 (all tree 0)
- 10 (tree 0) -> 20 (tree 0, DOWN, +0) = 0
- 20 (tree 0) -> 30 (tree 0, DOWN, +0) = 0

Expected Output: 0

---

## Test Case 3: Single Climb Path
Input: custom_test3.txt

Tree 0:
  1 -> 2
  2 -> 3, 4, 5

Tree 1:
  3 -> 6

Start: 1, Destination: 6

Expected Path Analysis:
- 1 (tree 0) -> 2 (tree 0, DOWN, +0) = 0
- 2 (tree 0) -> 3 (tree 0, DOWN, +0) = 0
- 3 (switch to tree 1, +1) = 1
- 3 (tree 1) -> 6 (tree 1, DOWN, +0) = 1

Expected Output: 1
