#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <limits.h>
#include <stdbool.h>

#define MAX_N 100
#define MAX_STR_LEN 1000
#define MAX_PIECE_LEN 20
#define INF 1000000

char target[MAX_STR_LEN + 1];
char pieces[MAX_N][MAX_PIECE_LEN + 1];
int costs[MAX_N];
int n;
int target_len;

// DP arrays
// dp[i] = minimum cost to cover first i characters of target
int dp1[MAX_STR_LEN + 1]; // With rearrangement
int dp2[MAX_STR_LEN + 1]; // Without rearrangement

// Check if we can form subsequence target[start..end-1] using characters from piece (with rearrangement)
bool canFormWithRearrangement(int start, int end, const char* piece) {
    int freq[26] = {0};
    for (int i = 0; piece[i] != '\0'; i++) {
        freq[piece[i] - 'a']++;
    }
    
    for (int i = start; i < end; i++) {
        if (freq[target[i] - 'a'] > 0) {
            freq[target[i] - 'a']--;
        } else {
            return false;
        }
    }
    return true;
}

// Check if we can form subsequence target[start..end-1] using piece as a subsequence (without rearrangement)
bool canFormWithoutRearrangement(int start, int end, const char* piece) {
    int piece_idx = 0;
    int piece_len = strlen(piece);
    
    for (int i = start; i < end; i++) {
        bool found = false;
        while (piece_idx < piece_len) {
            if (piece[piece_idx] == target[i]) {
                piece_idx++;
                found = true;
                break;
            }
            piece_idx++;
        }
        if (!found) return false;
    }
    return true;
}

void solveDPWithRearrangement() {
    for (int i = 0; i <= target_len; i++) {
        dp1[i] = INF;
    }
    dp1[0] = 0;
    
    for (int i = 0; i < target_len; i++) {
        if (dp1[i] >= INF) continue;
        
        for (int j = 0; j < n; j++) {
            // Try to extend from position i using piece j
            for (int len = 1; len <= strlen(pieces[j]) && i + len <= target_len; len++) {
                if (canFormWithRearrangement(i, i + len, pieces[j])) {
                    if (dp1[i] + costs[j] < dp1[i + len]) {
                        dp1[i + len] = dp1[i] + costs[j];
                    }
                }
            }
        }
    }
}

void solveDPWithoutRearrangement() {
    for (int i = 0; i <= target_len; i++) {
        dp2[i] = INF;
    }
    dp2[0] = 0;
    
    for (int i = 0; i < target_len; i++) {
        if (dp2[i] >= INF) continue;
        
        for (int j = 0; j < n; j++) {
            // Try to extend from position i using piece j
            for (int len = 1; len <= strlen(pieces[j]) && i + len <= target_len; len++) {
                if (canFormWithoutRearrangement(i, i + len, pieces[j])) {
                    if (dp2[i] + costs[j] < dp2[i + len]) {
                        dp2[i + len] = dp2[i] + costs[j];
                    }
                }
            }
        }
    }
}

int main(int argc, char* argv[]) {
    FILE* fp;
    
    if (argc > 1) {
        fp = fopen(argv[1], "r");
        if (fp == NULL) {
            printf("Error opening file: %s\n", argv[1]);
            return 1;
        }
    } else {
        fp = stdin;
    }
    
    // Read input
    fgets(target, sizeof(target), fp);
    target[strcspn(target, "\n")] = '\0';
    target_len = strlen(target);
    
    fscanf(fp, "%d", &n);
    for (int i = 0; i < n; i++) {
        fscanf(fp, "%s", pieces[i]);
    }
    for (int i = 0; i < n; i++) {
        fscanf(fp, "%d", &costs[i]);
    }
    
    if (fp != stdin) {
        fclose(fp);
    }
    
    // Solve both cases
    solveDPWithRearrangement();
    solveDPWithoutRearrangement();
    
    // Calculate difference
    int diff = dp2[target_len] - dp1[target_len];
    
    printf("%d\n", diff);
    
    return 0;
}

