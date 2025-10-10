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
    int neighbors[MAX_NODES][MAX_NODES];
    int neighborCount[MAX_NODES];
} Graph;

typedef struct {
    int x1, y1, x2, y2;
} Segment;

PointList allPoints;
Graph roadNetwork;
int houseIndex;
int totalCycles = 0;
bool alreadyVisited[MAX_NODES];
int currentRoute[MAX_NODES];
int routeLength;
char uniqueCycles[1000][500];
int uniqueCycleCount = 0;
Segment roadSegments[MAX_EDGES];
int segmentCount = 0;

int findOrAddPoint(int x, int y) {
    for (int i = 0; i < allPoints.count; i++) {
        if (allPoints.points[i].x == x && allPoints.points[i].y == y) {
            return i;
        }
    }
    allPoints.points[allPoints.count].x = x;
    allPoints.points[allPoints.count].y = y;
    return allPoints.count++;
}

bool pointOnSegment(int px, int py, int x1, int y1, int x2, int y2) {
    if (px < (x1 < x2 ? x1 : x2) || px > (x1 > x2 ? x1 : x2)) return false;
    if (py < (y1 < y2 ? y1 : y2) || py > (y1 > y2 ? y1 : y2)) return false;
    
    if (x1 == x2) {
        return px == x1;
    }
    if (y1 == y2) {
        return py == y1;
    }
    
    return (py - y1) * (x2 - x1) == (y2 - y1) * (px - x1);
}

void addEdge(int u, int v) {
    if (u == v) return;
    
    for (int i = 0; i < roadNetwork.neighborCount[u]; i++) {
        if (roadNetwork.neighbors[u][i] == v) return;
    }
    
    roadNetwork.neighbors[u][roadNetwork.neighborCount[u]++] = v;
    roadNetwork.neighbors[v][roadNetwork.neighborCount[v]++] = u;
}

void createPathString(int* routePath, int len, char* str) {
    int minPos = 0;
    for (int i = 1; i < len; i++) {
        if (routePath[i] < routePath[minPos]) {
            minPos = i;
        }
    }
    
    char forward[500] = "";
    char backward[500] = "";
    
    for (int i = 0; i < len; i++) {
        char temp[20];
        sprintf(temp, "%d,", routePath[(minPos + i) % len]);
        strcat(forward, temp);
    }
    
    for (int i = 0; i < len; i++) {
        char temp[20];
        int idx = (minPos - i + len) % len;
        sprintf(temp, "%d,", routePath[idx]);
        strcat(backward, temp);
    }
    
    if (strcmp(forward, backward) < 0) {
        strcpy(str, forward);
    } else {
        strcpy(str, backward);
    }
}

bool isPathUnique(int* routePath, int len) {
    char pathStr[500];
    createPathString(routePath, len, pathStr);
    
    for (int i = 0; i < uniqueCycleCount; i++) {
        if (strcmp(uniqueCycles[i], pathStr) == 0) {
            return false;
        }
    }
    
    strcpy(uniqueCycles[uniqueCycleCount++], pathStr);
    return true;
}

void findCycles(int currentNode, int startNode) {
    alreadyVisited[currentNode] = true;
    currentRoute[routeLength++] = currentNode;
    
    for (int i = 0; i < roadNetwork.neighborCount[currentNode]; i++) {
        int nextNode = roadNetwork.neighbors[currentNode][i];
        
        if (nextNode == startNode && routeLength >= 3) {
            if (isPathUnique(currentRoute, routeLength)) {
                totalCycles++;
            }
        }
        else if (!alreadyVisited[nextNode]) {
            findCycles(nextNode, startNode);
        }
    }
    
    routeLength--;
    alreadyVisited[currentNode] = false;
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
    
    allPoints.count = 0;
    memset(roadNetwork.neighborCount, 0, sizeof(roadNetwork.neighborCount));
    segmentCount = 0;
    
    for (int i = 0; i < N; i++) {
        fscanf(fp, "%d %d %d %d", &roadSegments[i].x1, &roadSegments[i].y1, &roadSegments[i].x2, &roadSegments[i].y2);
        segmentCount++;
    }
    
    int houseX, houseY;
    fscanf(fp, "%d %d", &houseX, &houseY);
    
    for (int i = 0; i < segmentCount; i++) {
        findOrAddPoint(roadSegments[i].x1, roadSegments[i].y1);
        findOrAddPoint(roadSegments[i].x2, roadSegments[i].y2);
    }
    
    houseIndex = findOrAddPoint(houseX, houseY);
    
    for (int i = 0; i < segmentCount; i++) {
        int x1 = roadSegments[i].x1, y1 = roadSegments[i].y1;
        int x2 = roadSegments[i].x2, y2 = roadSegments[i].y2;
        
        int pointsOnSeg[MAX_NODES];
        int pointsOnSegCount = 0;
        
        for (int j = 0; j < allPoints.count; j++) {
            int px = allPoints.points[j].x;
            int py = allPoints.points[j].y;
            
            if (pointOnSegment(px, py, x1, y1, x2, y2)) {
                pointsOnSeg[pointsOnSegCount++] = j;
            }
        }
        
        for (int a = 0; a < pointsOnSegCount - 1; a++) {
            for (int b = a + 1; b < pointsOnSegCount; b++) {
                int idx1 = pointsOnSeg[a];
                int idx2 = pointsOnSeg[b];
                int px1 = allPoints.points[idx1].x, py1 = allPoints.points[idx1].y;
                int px2 = allPoints.points[idx2].x, py2 = allPoints.points[idx2].y;
                
                int dist1 = (px1 - x1) * (px1 - x1) + (py1 - y1) * (py1 - y1);
                int dist2 = (px2 - x1) * (px2 - x1) + (py2 - y1) * (py2 - y1);
                
                if (dist1 > dist2) {
                    int temp = pointsOnSeg[a];
                    pointsOnSeg[a] = pointsOnSeg[b];
                    pointsOnSeg[b] = temp;
                }
            }
        }
        
        for (int j = 0; j < pointsOnSegCount - 1; j++) {
            addEdge(pointsOnSeg[j], pointsOnSeg[j + 1]);
        }
    }
    
    if (fp != stdin) fclose(fp);
    
    memset(alreadyVisited, false, sizeof(alreadyVisited));
    routeLength = 0;
    uniqueCycleCount = 0;
    totalCycles = 0;
    
    findCycles(houseIndex, houseIndex);
    
    printf("%d\n", totalCycles);
    
    return 0;
}