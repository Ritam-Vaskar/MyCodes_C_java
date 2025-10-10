#include <stdio.h>
#include <string.h>
#include <ctype.h>

// LED segment patterns (7 segments labeled as indices 0-6)
int patterns[17][7] = {
    {1,1,1,0,1,1,1}, // 0
    {0,0,1,0,0,1,0}, // 1
    {1,0,1,1,1,0,1}, // 2
    {1,0,1,1,0,1,1}, // 3
    {0,1,1,1,0,1,0}, // 4
    {1,1,0,1,0,1,1}, // 5
    {1,1,0,1,1,1,1}, // 6
    {1,0,1,0,0,1,0}, // 7
    {1,1,1,1,1,1,1}, // 8
    {1,1,1,1,0,1,1}, // 9
    {1,1,0,0,1,1,0}, // +
    {0,1,0,1,0,0,0}, // -
    {1,1,0,0,1,1,0}, // * (same as +)
    {0,1,0,1,0,0,0}, // / (same as -)
    {0,0,0,0,0,0,0}, // ( 
    {0,0,0,0,0,0,0}, // )
    {-1,-1,-1,-1,-1,-1,-1} // invalid
};

char charMap[] = "0123456789+-*/()";

int charToIdx(char c) {
    if (c >= '0' && c <= '9') return c - '0';
    if (c == '+') return 10;
    if (c == '-') return 11;
    if (c == '*') return 12;
    if (c == '/') return 13;
    if (c == '(') return 14;
    if (c == ')') return 15;
    return 16;
}

char idxToChar(int idx) {
    if (idx >= 0 && idx <= 15) return charMap[idx];
    return '?';
}

int canTransform(char from, char to) {
    int fromIdx = charToIdx(from);
    int toIdx = charToIdx(to);
    
    if (fromIdx == 16 || toIdx == 16) return 0;
    
    int diff = 0;
    for (int i = 0; i < 7; i++) {
        if (patterns[fromIdx][i] != patterns[toIdx][i]) diff++;
    }
    return diff == 1;
}

long long evaluateExpression(const char* expr, const char* prec) {
    int len = strlen(expr);
    long long* values = malloc(sizeof(long long) * len);
    char* ops = malloc(sizeof(char) * len);
    int valCount = 0, opCount = 0;
    
    int i = 0;
    while (i < len) {
        if (isdigit(expr[i])) {
            long long num = 0;
            while (i < len && isdigit(expr[i])) {
                num = num * 10 + (expr[i] - '0');
                i++;
            }
            values[valCount++] = num;
        } else if (expr[i] == '(') {
            i++;
        } else if (expr[i] == ')') {
            i++;
        } else if (strchr("+-*/", expr[i])) {
            ops[opCount++] = expr[i];
            i++;
        } else {
            i++;
        }
    }
    
    if (valCount == 0) {
        free(values);
        free(ops);
        return -1;
    }
    
    // Apply operators with precedence
    while (opCount > 0) {
        int maxPrec = -1, maxIdx = -1;
        for (int j = 0; j < opCount; j++) {
            int p = strchr(prec, ops[j]) - prec;
            if (maxPrec < 0 || p < maxPrec) {
                maxPrec = p;
                maxIdx = j;
            }
        }
        
        long long left = values[maxIdx];
        long long right = values[maxIdx + 1];
        long long result;
        
        if (ops[maxIdx] == '+') result = left + right;
        else if (ops[maxIdx] == '-') result = left - right;
        else if (ops[maxIdx] == '*') result = left * right;
        else if (ops[maxIdx] == '/') {
            if (right == 0) {
                free(values);
                free(ops);
                return -1;
            }
            result = left / right;
        }
        
        for (int j = maxIdx; j < valCount - 1; j++) {
            values[j] = values[j + 1];
        }
        for (int j = maxIdx; j < opCount - 1; j++) {
            ops[j] = ops[j + 1];
        }
        valCount--;
        opCount--;
    }
    
    long long res = values[0];
    free(values);
    free(ops);
    return res;
}

int isValidEquation(const char* expr) {
    int i = 0, len = strlen(expr);
    while (i < len && (isdigit(expr[i]) || strchr("+-*/()", expr[i]) || expr[i] == ' ')) i++;
    return i == len;
}

int main() {
    int n;
    scanf("%d", &n);
    getchar();
    
    char line1[200], line2[200], line3[200], prec[10];
    fgets(line1, sizeof(line1), stdin);
    fgets(line2, sizeof(line2), stdin);
    fgets(line3, sizeof(line3), stdin);
    fgets(prec, sizeof(prec), stdin);
    
    // Parse expression from 3 lines
    char expr[100] = "";
    int pos = 0;
    for (int i = 0; i < n; i++) {
        int col = i * 4;
        if (col + 3 < strlen(line1)) {
            char c = line1[col];
            if (c != ' ') expr[pos++] = c;
        }
    }
    expr[pos] = '\0';
    
    long long maxWorth = 0;
    
    // Try toggling each position in the expression
    for (int i = 0; i < strlen(expr); i++) {
        char orig = expr[i];
        
        for (char c = '0'; c <= '9'; c++) {
            if (canTransform(orig, c)) {
                expr[i] = c;
                if (isValidEquation(expr)) {
                    long long val = evaluateExpression(expr, prec);
                    if (val > 0) maxWorth += val;
                }
                expr[i] = orig;
            }
        }
        
        for (char c = '+'; c <= '/'; c = (c == '+' ? '-' : c == '-' ? '*' : '/')) {
            if (canTransform(orig, c)) {
                expr[i] = c;
                if (isValidEquation(expr)) {
                    long long val = evaluateExpression(expr, prec);
                    if (val > 0) maxWorth += val;
                }
                expr[i] = orig;
            }
        }
    }
    
    printf("%lld\n", maxWorth);
    return 0;
}