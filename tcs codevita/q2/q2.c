#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <limits.h>
#include <stdbool.h>

#define MAX_N 25

typedef struct {
    int row, col, distance;
} Position;

typedef struct {
    Position* data;
    int size, capacity;
} PriorityQueue;

typedef struct {
    Position* data;
    int front, rear, size, capacity;
} Queue;

Queue* createQueue(int capacity) {
    Queue* q = (Queue*)malloc(sizeof(Queue));
    q->capacity = capacity;
    q->front = 0;
    q->size = 0;
    q->rear = capacity - 1;
    q->data = (Position*)malloc(q->capacity * sizeof(Position));
    return q;
}

int isEmpty(Queue* q) {
    return q->size == 0;
}

void enqueue(Queue* q, Position item) {
    q->rear = (q->rear + 1) % q->capacity;
    q->data[q->rear] = item;
    q->size++;
}

Position dequeue(Queue* q) {
    Position item = q->data[q->front];
    q->front = (q->front + 1) % q->capacity;
    q->size--;
    return item;
}

void freeQueue(Queue* q) {
    free(q->data);
    free(q);
}

char grid[MAX_N][MAX_N];
int dist[MAX_N][MAX_N];
int dx[] = {-1, 1, 0, 0};
int dy[] = {0, 0, -1, 1};

void parseWall(char wall[MAX_N][MAX_N * 10], int n, int* sourceRow, int* sourceCol, int* destRow, int* destCol) {
    int currentRow = 0, currentCol = 0;
    
    for (int i = 0; i < n; i++) {
        currentCol = 0;
        int j = 0;
        while (wall[i][j] != '\0' && wall[i][j] != '\n') {
            if (wall[i][j] >= '0' && wall[i][j] <= '9') {
                int length = 0;
                while (wall[i][j] >= '0' && wall[i][j] <= '9') {
                    length = length * 10 + (wall[i][j] - '0');
                    j++;
                }
                
                if (wall[i][j] != '\0' && wall[i][j] != '\n') {
                    char brickType = wall[i][j];
                    
                    for (int k = 0; k < length; k++) {
                        if (currentCol < n) {
                            grid[currentRow][currentCol] = brickType;
                            if (brickType == 'S') {
                                *sourceRow = currentRow;
                                *sourceCol = currentCol;
                            } else if (brickType == 'D') {
                                *destRow = currentRow;
                                *destCol = currentCol;
                            }
                            currentCol++;
                        }
                    }
                    j++;
                }
            } else {
                j++;
            }
        }
        currentRow++;
    }
}

int bfs(int n, int sourceRow, int sourceCol, int destRow, int destCol) {
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            dist[i][j] = INT_MAX;
        }
    }
    
    Queue* q = createQueue(n * n * 10);
    Position start = {sourceRow, sourceCol, 0};
    enqueue(q, start);
    dist[sourceRow][sourceCol] = 0;
    
    while (!isEmpty(q)) {
        Position current = dequeue(q);
        int row = current.row;
        int col = current.col;
        int currentDist = current.distance;
        
        if (row == destRow && col == destCol) {
            freeQueue(q);
            return currentDist;
        }
        
        if (currentDist > dist[row][col]) continue;
        
        for (int i = 0; i < 4; i++) {
            int nextRow = row + dx[i];
            int nextCol = col + dy[i];
            
            if (nextRow >= 0 && nextRow < n && nextCol >= 0 && nextCol < n) {
                char cellType = grid[nextRow][nextCol];
                int newDistance;
                
                if (cellType == 'R') {
                    continue;
                }
                else if (cellType == 'G') {
                    newDistance = currentDist + 1;
                }
                else if (cellType == 'D') {
                    newDistance = currentDist;
                }
                else if (cellType == 'S') {
                    continue;
                }
                else {
                    continue;
                }
                
                if (newDistance < dist[nextRow][nextCol]) {
                    dist[nextRow][nextCol] = newDistance;
                    Position next = {nextRow, nextCol, newDistance};
                    enqueue(q, next);
                }
            }
        }
    }
    
    freeQueue(q);
    return -1;
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
    
    int n;
    fscanf(fp, "%d\n", &n);
    
    char wall[MAX_N][MAX_N * 10];
    for (int i = 0; i < n; i++) {
        fgets(wall[i], MAX_N * 10, fp);
    }
    
    int sourceRow, sourceCol, destRow, destCol;
    parseWall(wall, n, &sourceRow, &sourceCol, &destRow, &destCol);
    
    int result = bfs(n, sourceRow, sourceCol, destRow, destCol);
    printf("%d\n", result);
    
    if (fp != stdin) {
        fclose(fp);
    }
    
    return 0;
}