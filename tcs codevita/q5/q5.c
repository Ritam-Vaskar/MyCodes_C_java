#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

#define MAX_NODES 100
#define MAX_EDGES 50

typedef struct {
    int x, y;
} Point;

typedef struct {
    Point points[MAX_NODES];
    int count;
} PointList;

typedef struct {
    int adj[MAX_NODES][MAX_NODES];
    int degree[MAX_NODES];
} Graph;

typedef struct {
    int x1, y1, x2, y2;
} Segment;

PointList pointList;
Graph graph;
int houseIdx;
int totalPaths = 0;
bool visited[MAX_NODES];
int currentPath[MAX_NODES];
int pathLen;
char foundPaths[1000][500];
int foundPathCount = 0;
Segment segments[MAX_EDGES];
int segmentCount = 0;

// Find or add point to list
int findOrAddPoint(int x, int y) {
    for (int i = 0; i < pointList.count; i++) {
        if (pointList.points[i].x == x && pointList.points[i].y == y) {
            return i;
        }
    }
    pointList.points[pointList.count].x = x;
    pointList.points[pointList.count].y = y;
    return pointList.count++;
}

// Check if point (px, py) lies on segment from (x1, y1) to (x2, y2)
bool pointOnSegment(int px, int py, int x1, int y1, int x2, int y2) {
    // Check if point is within bounding box
    if (px < (x1 < x2 ? x1 : x2) || px > (x1 > x2 ? x1 : x2)) return false;
    if (py < (y1 < y2 ? y1 : y2) || py > (y1 > y2 ? y1 : y2)) return false;
    
    // Check if point is on the line
    if (x1 == x2) {
        return px == x1;
    }
    if (y1 == y2) {
        return py == y1;
    }
    
    // Check cross product for collinearity
    return (py - y1) * (x2 - x1) == (y2 - y1) * (px - x1);
}

// Add edge to graph (avoiding duplicates)
void addEdge(int u, int v) {
    if (u == v) return;
    
    // Check if edge already exists
    for (int i = 0; i < graph.degree[u]; i++) {
        if (graph.adj[u][i] == v) return;
    }
    
    graph.adj[u][graph.degree[u]++] = v;
    graph.adj[v][graph.degree[v]++] = u;
}

// Create canonical string representation of a cycle path
void createPathString(int* path, int len, char* str) {
    // Find minimum element position
    int minPos = 0;
    for (int i = 1; i < len; i++) {
        if (path[i] < path[minPos]) {
            minPos = i;
        }
    }
    
    // Create two possible representations starting from minPos
    char forward[500] = "";
    char backward[500] = "";
    
    // Forward direction
    for (int i = 0; i < len; i++) {
        char temp[20];
        sprintf(temp, "%d,", path[(minPos + i) % len]);
        strcat(forward, temp);
    }
    
    // Backward direction
    for (int i = 0; i < len; i++) {
        char temp[20];
        int idx = (minPos - i + len) % len;
        sprintf(temp, "%d,", path[idx]);
        strcat(backward, temp);
    }
    
    // Use lexicographically smaller string
    if (strcmp(forward, backward) < 0) {
        strcpy(str, forward);
    } else {
        strcpy(str, backward);
    }
}

// Check if path already exists
bool isPathUnique(int* path, int len) {
    char pathStr[500];
    createPathString(path, len, pathStr);
    
    for (int i = 0; i < foundPathCount; i++) {
        if (strcmp(foundPaths[i], pathStr) == 0) {
            return false;
        }
    }
    
    strcpy(foundPaths[foundPathCount++], pathStr);
    return true;
}

// DFS to find all cycles
void findCycles(int current, int start) {
    visited[current] = true;
    currentPath[pathLen++] = current;
    
    // Try all neighbors
    for (int i = 0; i < graph.degree[current]; i++) {
        int next = graph.adj[current][i];
        
        // If we can return to start and have visited at least 2 other nodes
        if (next == start && pathLen >= 3) {
            // Found a cycle
            if (isPathUnique(currentPath, pathLen)) {
                totalPaths++;
            }
        }
        // Continue exploring unvisited nodes
        else if (!visited[next]) {
            findCycles(next, start);
        }
    }
    
    // Backtrack
    pathLen--;
    visited[current] = false;
}

int main(int argc, char* argv[]) {
    FILE* fp;
    
    if (argc > 1) {
        fp = fopen(argv[1], "r");
        if (!fp) {
            printf("Error opening file\n");
            return 1;
        }
    } else {
        fp = stdin;
    }
    
    int N;
    fscanf(fp, "%d", &N);
    
    pointList.count = 0;
    memset(graph.degree, 0, sizeof(graph.degree));
    segmentCount = 0;
    
    // Read all segments first
    for (int i = 0; i < N; i++) {
        fscanf(fp, "%d %d %d %d", &segments[i].x1, &segments[i].y1, &segments[i].x2, &segments[i].y2);
        segmentCount++;
    }
    
    // Read house coordinates
    int houseX, houseY;
    fscanf(fp, "%d %d", &houseX, &houseY);
    
    // Collect all unique points (endpoints + intersections)
    for (int i = 0; i < segmentCount; i++) {
        findOrAddPoint(segments[i].x1, segments[i].y1);
        findOrAddPoint(segments[i].x2, segments[i].y2);
    }
    
    // Add house if not already present
    houseIdx = findOrAddPoint(houseX, houseY);
    
    // For each segment, check if any other points lie on it
    // and split the segment accordingly
    for (int i = 0; i < segmentCount; i++) {
        int x1 = segments[i].x1, y1 = segments[i].y1;
        int x2 = segments[i].x2, y2 = segments[i].y2;
        
        // Find all points on this segment
        int pointsOnSeg[MAX_NODES];
        int pointsOnSegCount = 0;
        
        for (int j = 0; j < pointList.count; j++) {
            int px = pointList.points[j].x;
            int py = pointList.points[j].y;
            
            if (pointOnSegment(px, py, x1, y1, x2, y2)) {
                pointsOnSeg[pointsOnSegCount++] = j;
            }
        }
        
        // Sort points on segment by distance from (x1, y1)
        for (int a = 0; a < pointsOnSegCount - 1; a++) {
            for (int b = a + 1; b < pointsOnSegCount; b++) {
                int idx1 = pointsOnSeg[a];
                int idx2 = pointsOnSeg[b];
                int px1 = pointList.points[idx1].x, py1 = pointList.points[idx1].y;
                int px2 = pointList.points[idx2].x, py2 = pointList.points[idx2].y;
                
                int dist1 = (px1 - x1) * (px1 - x1) + (py1 - y1) * (py1 - y1);
                int dist2 = (px2 - x1) * (px2 - x1) + (py2 - y1) * (py2 - y1);
                
                if (dist1 > dist2) {
                    int temp = pointsOnSeg[a];
                    pointsOnSeg[a] = pointsOnSeg[b];
                    pointsOnSeg[b] = temp;
                }
            }
        }
        
        // Add edges between consecutive points on this segment
        for (int j = 0; j < pointsOnSegCount - 1; j++) {
            addEdge(pointsOnSeg[j], pointsOnSeg[j + 1]);
        }
    }
    
    if (fp != stdin) fclose(fp);
    
    // Find all cycles starting from house
    memset(visited, false, sizeof(visited));
    pathLen = 0;
    foundPathCount = 0;
    totalPaths = 0;
    
    findCycles(houseIdx, houseIdx);
    
    printf("%d\n", totalPaths);
    
    return 0;
}
