#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <limits.h>
#include <stdbool.h>

#define MAX_N 100
#define MAX_STR_LEN 1000
#define MAX_PIECE_LEN 20
#define INF INT_MAX / 2

char target[MAX_STR_LEN + 1];
char pieces[MAX_N][MAX_PIECE_LEN + 1];
int costs[MAX_N];
int n;
int target_len;

// DP for case 1: When rearrangement is allowed
int dp1[MAX_STR_LEN + 1];

// DP for case 2: When rearrangement is NOT allowed
int dp2[MAX_STR_LEN + 1];

// Count frequency of each character in a string
void countFreq(const char* str, int freq[26]) {
    memset(freq, 0, 26 * sizeof(int));
    for (int i = 0; str[i] != '\0'; i++) {
        freq[str[i] - 'a']++;
    }
}

// Check how many characters from target[start..] can be matched using piece (with rearrangement)
int matchWithRearrangement(int start, const char* piece) {
    if (start >= target_len) return 0;
    
    int freq[26];
    countFreq(piece, freq);
    
    int count = 0;
    for (int i = start; i < target_len; i++) {
        char c = target[i];
        if (freq[c - 'a'] > 0) {
            freq[c - 'a']--;
            count++;
        }
    }
    return count;
}

// Check how many characters from target[start..] can be matched using piece (without rearrangement)
int matchWithoutRearrangement(int start, const char* piece) {
    if (start >= target_len) return 0;
    
    int piece_idx = 0;
    int target_idx = start;
    int count = 0;
    
    while (target_idx < target_len && piece_idx < strlen(piece)) {
        if (target[target_idx] == piece[piece_idx]) {
            count++;
            target_idx++;
            piece_idx++;
        } else {
            piece_idx++;
        }
    }
    
    return count;
}

// Calculate minimum cost when rearrangement IS allowed
int calculateCostWithRearrangement() {
    for (int i = 0; i <= target_len; i++) {
        dp1[i] = INF;
    }
    dp1[0] = 0;
    
    printf("\n=== WITH Rearrangement ===\n");
    for (int i = 0; i < target_len; i++) {
        if (dp1[i] == INF) continue;
        
        printf("At position %d (target so far: '%.*s'), cost = %d\n", i, i, target, dp1[i]);
        
        // Try each piece
        for (int j = 0; j < n; j++) {
            int matched = matchWithRearrangement(i, pieces[j]);
            if (matched > 0) {
                int next_pos = i + matched;
                if (next_pos <= target_len) {
                    int new_cost = dp1[i] + costs[j];
                    printf("  Using piece '%s' (cost %d): matches %d chars -> pos %d, cost %d\n", 
                           pieces[j], costs[j], matched, next_pos, new_cost);
                    if (new_cost < dp1[next_pos]) {
                        dp1[next_pos] = new_cost;
                    }
                }
            }
        }
    }
    
    printf("Final cost WITH rearrangement: %d\n", dp1[target_len]);
    return dp1[target_len];
}

// Calculate minimum cost when rearrangement is NOT allowed
int calculateCostWithoutRearrangement() {
    for (int i = 0; i <= target_len; i++) {
        dp2[i] = INF;
    }
    dp2[0] = 0;
    
    printf("\n=== WITHOUT Rearrangement ===\n");
    for (int i = 0; i < target_len; i++) {
        if (dp2[i] == INF) continue;
        
        printf("At position %d (target so far: '%.*s'), cost = %d\n", i, i, target, dp2[i]);
        
        // Try each piece
        for (int j = 0; j < n; j++) {
            int matched = matchWithoutRearrangement(i, pieces[j]);
            if (matched > 0) {
                int next_pos = i + matched;
                if (next_pos <= target_len) {
                    int new_cost = dp2[i] + costs[j];
                    printf("  Using piece '%s' (cost %d): matches %d chars -> pos %d, cost %d\n", 
                           pieces[j], costs[j], matched, next_pos, new_cost);
                    if (new_cost < dp2[next_pos]) {
                        dp2[next_pos] = new_cost;
                    }
                }
            }
        }
    }
    
    printf("Final cost WITHOUT rearrangement: %d\n", dp2[target_len]);
    return dp2[target_len];
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
    
    // Read target string
    if (fgets(target, sizeof(target), fp) == NULL) {
        printf("Error reading target string\n");
        return 1;
    }
    // Remove newline
    target[strcspn(target, "\n")] = '\0';
    target_len = strlen(target);
    
    // Read number of pieces
    if (fscanf(fp, "%d\n", &n) != 1) {
        printf("Error reading number of pieces\n");
        return 1;
    }
    
    // Read pieces
    for (int i = 0; i < n; i++) {
        if (fscanf(fp, "%s", pieces[i]) != 1) {
            printf("Error reading piece %d\n", i);
            return 1;
        }
    }
    
    // Read costs
    for (int i = 0; i < n; i++) {
        if (fscanf(fp, "%d", &costs[i]) != 1) {
            printf("Error reading cost %d\n", i);
            return 1;
        }
    }
    
    if (fp != stdin) {
        fclose(fp);
    }
    
    printf("Target string: '%s' (length: %d)\n", target, target_len);
    printf("Number of pieces: %d\n", n);
    printf("Pieces and costs:\n");
    for (int i = 0; i < n; i++) {
        printf("  %d: '%s' (cost %d)\n", i, pieces[i], costs[i]);
    }
    
    // Calculate both costs
    int cost_with_rearrangement = calculateCostWithRearrangement();
    int cost_without_rearrangement = calculateCostWithoutRearrangement();
    
    // Calculate the difference
    int difference = cost_without_rearrangement - cost_with_rearrangement;
    
    printf("\nDifference: %d - %d = %d\n", cost_without_rearrangement, cost_with_rearrangement, difference);
    
    return 0;
}
