# Test Case 2 Analysis

Input:
```
5
3G1R1G
1G1R1G2R
1S1R1G1R1D
2R1G1R1G
5G
```

Expected Output: 7

Grid parsing:
Row 0: 3G + 1R + 1G = GGGRG
Row 1: 1G + 1R + 1G + 2R = GRGRR
Row 2: 1S + 1R + 1G + 1R + 1D = SRGRD
Row 3: 2R + 1G + 1R + 1G = RRGRG
Row 4: 5G = GGGGG

Visual:
```
  0 1 2 3 4
0 G G G R G
1 G R G R R
2 S R G R D
3 R R G R G
4 G G G G G
```

S at (2,0), D at (2,4)

Possible paths:
1. Down to bottom row, across, then up:
   S(2,0) -> need to go through (3,0) which is R - BLOCKED

2. Up to top, across:
   S(2,0) -> (1,0)G -> (0,0)G -> (0,1)G -> (0,2)G -> blocked by R at (0,3)
   
3. From (0,2), go down and around:
   ... (0,2)G -> (1,2)G -> (2,2)G -> (3,2)G -> (4,2)G -> (4,3)G -> (4,4)G -> (3,4)G -> D(2,4)
   Total: 1+1+1+1+1+1+1+1+1+1+1 = 11 green bricks

I keep getting 11. Unless there's a path I'm missing?

Wait! What if we can go:
S(2,0) -> (2,2)[G] directly? No, there's R at (2,1).

Hmm, I'm stumped. Let me check if maybe the expected output in the problem is wrong, or if I'm misunderstanding something fundamental.

Actually, let me double-check my grid parsing is correct by looking at test 1:
