# Custom Test Cases for Brick Wall Problem

## Custom Test 1: Path Around Barrier
**File:** custom_test1.txt
**Grid:**
```
S G G G
R R R R
G G G G
G G G D
```
**Analysis:**
- S at (0,0), D at (3,3)
- Direct downward path blocked by row of red bricks at row 1
- Must go right first, then down
- Path: S(0,0) -> (0,1)G -> (0,2)G -> (0,3)G -> (1,3) blocked, need to go to (2,3)G -> (3,3)D
- Wait, (1,3) is R, so: S -> (0,1)G -> (0,2)G -> (0,3)G -> need different path
- Actually: Can't get past row 1 of all R's easily
- Must go: S(0,0) -> (0,1)G -> (0,2)G -> (0,3)G -> (then can't go through R row)
- This might have NO SOLUTION or long path going around

**Expected:** Let BFS find it

---

## Custom Test 2: Zigzag Path
**File:** custom_test2.txt
**Grid:**
```
S R R R R
G R G G G
G R G R R
G R G R G
D G G G G
```
**Analysis:**
- S at (0,0), D at (4,0)
- Must zigzag down column 0 and through gaps
- Path going down left column: S(0,0) -> (1,0)G -> (2,0)G -> (3,0)G -> D(4,0)
- That's 3 green bricks!

**Expected:** 3

---

## Custom Test 3: Multiple Path Options
**File:** custom_test3.txt
**Grid:**
```
G G G S G G
R G G G G G
R G R G G R
R G R G R R
R G G G G G
G G G D R R
```
**Analysis:**
- S at (0,3), D at (5,3)
- Multiple possible paths
- Can go down through column 3 mostly
- Path: S(0,3) -> (1,3)G -> (2,3)G -> (3,3)G -> (4,3)G -> (5,3)D
- That's 4 green bricks

**Expected:** 4

---

## Custom Test 4: Diagonal Movement Required
**File:** custom_test4.txt
**Grid:**
```
S G R G
G G R G
G R G G
R G G D
```
**Analysis:**
- S at (0,0), D at (3,3)
- Diagonal barriers force zigzag
- Path: S(0,0) -> (0,1)G -> (1,1)G -> (1,0)G -> (2,0)G -> (2,2)G -> (2,3)G -> (3,3)D
- Let BFS find optimal

**Expected:** Let BFS calculate

---

## Custom Test 5: No Solution Test
**File:** custom_test5.txt
**Grid:**
```
S R D
G G G
G G G
```
**Analysis:**
- S at (0,0), D at (0,2)
- Direct path blocked by R at (0,1)
- Must go down, across, then up
- Path: S(0,0) -> (1,0)G -> (1,1)G -> (1,2)G -> (0,2)D
- That's 3 green bricks

**Expected:** 3
