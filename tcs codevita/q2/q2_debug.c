#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <limits.h>

#define MAX_N 25

typedef struct {
    int x, y, dist;
} Node;

typedef struct {
    Node* data;
    int front, rear, size, capacity;
} Queue;

Queue* createQueue(int capacity) {
    Queue* q = (Queue*)malloc(sizeof(Queue));
    q->capacity = capacity;
    q->front = 0;
    q->size = 0;
    q->rear = capacity - 1;
    q->data = (Node*)malloc(q->capacity * sizeof(Node));
    return q;
}

int isEmpty(Queue* q) {
    return q->size == 0;
}

void enqueue(Queue* q, Node item) {
    q->rear = (q->rear + 1) % q->capacity;
    q->data[q->rear] = item;
    q->size++;
}

Node dequeue(Queue* q) {
    Node item = q->data[q->front];
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

void parseWall(char wall[MAX_N][MAX_N * 10], int n, int* srcX, int* srcY, int* dstX, int* dstY) {
    int row = 0, col = 0;
    
    for (int i = 0; i < n; i++) {
        col = 0;
        int j = 0;
        while (wall[i][j] != '\0' && wall[i][j] != '\n') {
            if (wall[i][j] >= '0' && wall[i][j] <= '9') {
                int length = 0;
                while (wall[i][j] >= '0' && wall[i][j] <= '9') {
                    length = length * 10 + (wall[i][j] - '0');
                    j++;
                }
                
                if (wall[i][j] != '\0' && wall[i][j] != '\n') {
                    char type = wall[i][j];
                    
                    for (int k = 0; k < length; k++) {
                        if (col < n) {
                            grid[row][col] = type;
                            if (type == 'S') {
                                *srcX = row;
                                *srcY = col;
                            } else if (type == 'D') {
                                *dstX = row;
                                *dstY = col;
                            }
                            col++;
                        }
                    }
                    j++;
                }
            } else {
                j++;
            }
        }
        row++;
    }
}

void printGrid(int n) {
    printf("\n=== Grid ===\n");
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            printf("%c ", grid[i][j]);
        }
        printf("\n");
    }
    printf("\n");
}

int bfs(int n, int srcX, int srcY, int dstX, int dstY) {
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            dist[i][j] = INT_MAX;
        }
    }
    
    Queue* q = createQueue(n * n * 10);
    Node start = {srcX, srcY, 0};
    enqueue(q, start);
    dist[srcX][srcY] = 0;
    
    printf("Source: (%d, %d) = '%c'\n", srcX, srcY, grid[srcX][srcY]);
    printf("Destination: (%d, %d) = '%c'\n", dstX, dstY, grid[dstX][dstY]);
    
    while (!isEmpty(q)) {
        Node curr = dequeue(q);
        int x = curr.x;
        int y = curr.y;
        int d = curr.dist;
        
        if (x == dstX && y == dstY) {
            freeQueue(q);
            return d;
        }
        
        if (d > dist[x][y]) continue;
        
        for (int i = 0; i < 4; i++) {
            int nx = x + dx[i];
            int ny = y + dy[i];
            
            if (nx >= 0 && nx < n && ny >= 0 && ny < n) {
                int newDist = d;
                
                if (grid[nx][ny] == 'D') {
                    newDist = d;
                } else if (grid[nx][ny] == 'G') {
                    newDist = d + 1;
                } else if (grid[nx][ny] == 'R') {
                    continue;
                } else if (grid[nx][ny] == 'S') {
                    continue;
                } else {
                    continue;
                }
                
                if (newDist < dist[nx][ny]) {
                    dist[nx][ny] = newDist;
                    Node next = {nx, ny, newDist};
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
    
    int srcX, srcY, dstX, dstY;
    parseWall(wall, n, &srcX, &srcY, &dstX, &dstY);
    
    printGrid(n);
    
    int result = bfs(n, srcX, srcY, dstX, dstY);
    printf("Result: %d\n", result);
    
    if (fp != stdin) {
        fclose(fp);
    }
    
    return 0;
}
