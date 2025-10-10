#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <limits.h>

#define MAX_SPOTS 1000
#define MAX_TREES 50

typedef struct Edge {
    int destination;
    struct Edge* next;
} Edge;

typedef struct {
    int location;
    int energyUsed;
    int currentTree;
} MonkeyState;

typedef struct {
    MonkeyState* data;
    int size;
    int capacity;
} PriorityQueue;

Edge* connections[MAX_SPOTS];
int treesAtSpot[MAX_SPOTS][MAX_TREES];
int treeCountAtSpot[MAX_SPOTS];
int children[MAX_SPOTS][MAX_SPOTS][MAX_TREES];
int childCount[MAX_SPOTS][MAX_TREES];
int alreadyVisited[MAX_SPOTS][MAX_TREES];

PriorityQueue* createPQ() {
    PriorityQueue* pq = (PriorityQueue*)malloc(sizeof(PriorityQueue));
    pq->capacity = 10000;
    pq->size = 0;
    pq->data = (MonkeyState*)malloc(pq->capacity * sizeof(MonkeyState));
    return pq;
}

void swap(MonkeyState* a, MonkeyState* b) {
    MonkeyState temp = *a;
    *a = *b;
    *b = temp;
}

void heapifyUp(PriorityQueue* pq, int idx) {
    while (idx > 0) {
        int parentIdx = (idx - 1) / 2;
        if (pq->data[idx].energyUsed < pq->data[parentIdx].energyUsed) {
            swap(&pq->data[idx], &pq->data[parentIdx]);
            idx = parentIdx;
        } else {
            break;
        }
    }
}

void heapifyDown(PriorityQueue* pq, int idx) {
    while (1) {
        int smallest = idx;
        int left = 2 * idx + 1;
        int right = 2 * idx + 2;
        
        if (left < pq->size && pq->data[left].energyUsed < pq->data[smallest].energyUsed)
            smallest = left;
        if (right < pq->size && pq->data[right].energyUsed < pq->data[smallest].energyUsed)
            smallest = right;
            
        if (smallest != idx) {
            swap(&pq->data[idx], &pq->data[smallest]);
            idx = smallest;
        } else {
            break;
        }
    }
}

void push(PriorityQueue* pq, MonkeyState s) {
    if (pq->size >= pq->capacity) {
        pq->capacity *= 2;
        pq->data = (MonkeyState*)realloc(pq->data, pq->capacity * sizeof(MonkeyState));
    }
    pq->data[pq->size] = s;
    heapifyUp(pq, pq->size);
    pq->size++;
}

MonkeyState pop(PriorityQueue* pq) {
    MonkeyState result = pq->data[0];
    pq->data[0] = pq->data[pq->size - 1];
    pq->size--;
    heapifyDown(pq, 0);
    return result;
}

int isEmpty(PriorityQueue* pq) {
    return pq->size == 0;
}

void addEdge(int from, int to) {
    Edge* newEdge = (Edge*)malloc(sizeof(Edge));
    newEdge->destination = to;
    newEdge->next = connections[from];
    connections[from] = newEdge;
}

void addSpotToTree(int spot, int treeId) {
    for (int i = 0; i < treeCountAtSpot[spot]; i++) {
        if (treesAtSpot[spot][i] == treeId) return;
    }
    treesAtSpot[spot][treeCountAtSpot[spot]++] = treeId;
}

void addParentChild(int parentSpot, int childSpot, int treeId) {
    children[parentSpot][childCount[parentSpot][treeId]++][treeId] = childSpot;
}

int isParent(int parentSpot, int childSpot, int treeId) {
    for (int i = 0; i < childCount[parentSpot][treeId]; i++) {
        if (children[parentSpot][i][treeId] == childSpot) return 1;
    }
    return 0;
}

int findMinEnergy(int start, int destination) {
    memset(alreadyVisited, 0, sizeof(alreadyVisited));
    PriorityQueue* pq = createPQ();
    
    for (int i = 0; i < treeCountAtSpot[start]; i++) {
        MonkeyState s = {start, 0, treesAtSpot[start][i]};
        push(pq, s);
    }
    
    while (!isEmpty(pq)) {
        MonkeyState current = pop(pq);
        
        if (current.location == destination) {
            free(pq->data);
            free(pq);
            return current.energyUsed;
        }
        
        if (alreadyVisited[current.location][current.currentTree]) continue;
        alreadyVisited[current.location][current.currentTree] = 1;
        
        for (int i = 0; i < treeCountAtSpot[current.location]; i++) {
            int newTree = treesAtSpot[current.location][i];
            if (newTree != current.currentTree && !alreadyVisited[current.location][newTree]) {
                MonkeyState newState = {current.location, current.energyUsed + 1, newTree};
                push(pq, newState);
            }
        }
        
        Edge* edge = connections[current.location];
        while (edge != NULL) {
            int neighbor = edge->destination;
            
            int neighborHasTree = 0;
            for (int i = 0; i < treeCountAtSpot[neighbor]; i++) {
                if (treesAtSpot[neighbor][i] == current.currentTree) {
                    neighborHasTree = 1;
                    break;
                }
            }
            
            if (neighborHasTree) {
                int energyCost = 0;
                
                if (isParent(neighbor, current.location, current.currentTree)) {
                    energyCost = 1;
                }
                
                int newEnergy = current.energyUsed + energyCost;
                
                if (!alreadyVisited[neighbor][current.currentTree]) {
                    MonkeyState newState = {neighbor, newEnergy, current.currentTree};
                    push(pq, newState);
                }
            }
            
            edge = edge->next;
        }
    }
    
    free(pq->data);
    free(pq);
    return -1;
}

int main() {
    int n;
    scanf("%d", &n);
    getchar();
    
    memset(connections, 0, sizeof(connections));
    memset(treeCountAtSpot, 0, sizeof(treeCountAtSpot));
    memset(childCount, 0, sizeof(childCount));
    
    int treeNumber = 0;
    
    for (int i = 0; i < n; i++) {
        char line[1000];
        fgets(line, sizeof(line), stdin);
        
        line[strcspn(line, "\n")] = 0;
        
        if (strcmp(line, "break") == 0) {
            treeNumber++;
            continue;
        }
        
        int spots[100];
        int spotCount = 0;
        char* token = strtok(line, " ");
        
        while (token != NULL) {
            spots[spotCount++] = atoi(token);
            token = strtok(NULL, " ");
        }
        
        if (spotCount > 0) {
            int parentSpot = spots[0];
            
            for (int j = 1; j < spotCount; j++) {
                int childSpot = spots[j];
                addEdge(parentSpot, childSpot);
                addEdge(childSpot, parentSpot);
                addSpotToTree(parentSpot, treeNumber);
                addSpotToTree(childSpot, treeNumber);
                addParentChild(parentSpot, childSpot, treeNumber);
            }
        }
    }
    
    int startSpot, endSpot;
    scanf("%d %d", &startSpot, &endSpot);
    
    int result = findMinEnergy(startSpot, endSpot);
    printf("%d\n", result);
    
    for (int i = 0; i < MAX_SPOTS; i++) {
        Edge* edge = connections[i];
        while (edge != NULL) {
            Edge* temp = edge;
            edge = edge->next;
            free(temp);
        }
    }
    
    return 0;
}