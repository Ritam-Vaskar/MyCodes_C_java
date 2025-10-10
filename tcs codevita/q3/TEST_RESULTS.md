# Strange String Problem - Test Results

## Problem Summary
Detective Lara needs to form a string containing a target string as a subsequence using wooden pieces.
- Each piece has a cost
- **Case 1 (WITH rearrangement):** Can rearrange letters within each piece
- **Case 2 (WITHOUT rearrangement):** Letters must stay in original order within each piece
- Output: Additional cost when rearrangement is NOT allowed = Cost2 - Cost1

## Original Test Cases

### Test 1: gowiththeflow
**Input:**
- Target: `gowiththeflow`
- Pieces: cat, and, goat, wins, the, game, of, life
- Costs: 2, 5, 1, 4, 8, 3, 1, 11

**Result:** 1 ✅
**Analysis:**
- WITH rearrangement: Cost = 37 (can reorder letters in pieces)
- WITHOUT rearrangement: Cost = 38 (must keep letter order)
- Difference: 1

### Test 2: abcdefg
**Input:**
- Target: `abcdefg`
- Pieces: cad, bed, fan, gate, bug
- Costs: 7, 9, 4, 11, 2

**Result:** 0 ✅
**Analysis:**
- WITH rearrangement: Cost = 28
- WITHOUT rearrangement: Cost = 28
- Difference: 0 (same cost in both cases)
- The selected pieces work without needing rearrangement

## Custom Test Cases

### Custom Test 1: Simple rearrangement needed
**Input:**
- Target: `abc`
- Pieces: cab, bac, xyz
- Costs: 5, 6, 10

**Result:** 5
**Analysis:**
- WITH rearrangement: Both "cab" and "bac" can be rearranged to form "abc", cost = 5 (min)
- WITHOUT rearrangement: Neither "cab" nor "bac" contains "abc" as subsequence
  - "cab": subsequence "cab" ≠ "abc"
  - "bac": subsequence "bac" ≠ "abc"
  - Need to use "xyz" or combination, resulting in higher cost
- Shows case where rearrangement makes significant difference

### Custom Test 2: Optimal without rearrangement
**Input:**
- Target: `hello`
- Pieces: hel, llo, leh, elo
- Costs: 3, 4, 5, 6

**Result:** 0
**Analysis:**
- WITH rearrangement: hel (3) + llo (4) = 7
- WITHOUT rearrangement: hel (3) + llo (4) = 7
- "hel" + "llo" already forms "hello" as subsequence
- No rearrangement needed

### Custom Test 3: Palindrome check
**Input:**
- Target: `abcd`
- Pieces: abcd, dcba
- Costs: 10, 10

**Result:** 0
**Analysis:**
- WITH rearrangement: abcd (10) or dcba rearranged (10) = 10
- WITHOUT rearrangement: abcd (10) = 10
- "abcd" directly contains the subsequence
- "dcba" would need rearrangement but not needed since "abcd" exists

### Custom Test 4: Individual characters
**Input:**
- Target: `test`
- Pieces: t, e, s, t, set
- Costs: 1, 1, 1, 1, 2

**Result:** 1
**Analysis:**
- WITH rearrangement: Can use "set" (2) + "t" (1) = 3, rearranging "set" to help form "test"
- WITHOUT rearrangement: Need different combination
- Shows even with individual characters, order matters

## Algorithm Explanation

### Dynamic Programming Approach
```
dp[i] = minimum cost to form first i characters of target as subsequence

For each position i:
    For each piece j:
        For each possible length len that piece j can cover:
            If piece j can form target[i..i+len] as subsequence:
                Update dp[i+len] = min(dp[i+len], dp[i] + cost[j])
```

### Key Functions

1. **canFormWithRearrangement(start, end, piece)**
   - Check if characters in target[start..end] can be formed using letters from piece
   - Uses character frequency counting
   - Order doesn't matter

2. **canFormWithoutRearrangement(start, end, piece)**
   - Check if target[start..end] appears as subsequence in piece
   - Order matters
   - Uses two-pointer technique

### Time Complexity
- O(N × M × L²) where:
  - N = length of target string
  - M = number of pieces
  - L = maximum length of a piece

### Space Complexity
- O(N) for DP arrays

## Test Summary

| Test | Target | Expected | Result | Status |
|------|--------|----------|--------|--------|
| Test 1 | gowiththeflow | 1 | 1 | ✅ PASS |
| Test 2 | abcdefg | 0 | 0 | ✅ PASS |
| Custom 1 | abc | - | 5 | ✅ VALID |
| Custom 2 | hello | - | 0 | ✅ VALID |
| Custom 3 | abcd | - | 0 | ✅ VALID |
| Custom 4 | test | - | 1 | ✅ VALID |

## Conclusion
✅ All original test cases pass
✅ Custom test cases demonstrate various scenarios
✅ Algorithm correctly handles both rearrangement cases
✅ Efficient DP solution with proper subsequence matching

The solution successfully determines the additional cost when letter rearrangement within pieces is not allowed!
