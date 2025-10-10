#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <limits.h>

#define MAX_SPOTS 1000
#define MAX_TREES 50

typedef struct Edge {
    int to;
    struct Edge* next;
} Edge;

typedef struct {
    int spot;
    int energy;
    int tree;
} State;

typedef struct {
    State* data;
    int size;
    int capacity;
} PriorityQueue;

Edge* adjList[MAX_SPOTS];
int spotTrees[MAX_SPOTS][MAX_TREES];
int spotTreeCount[MAX_SPOTS];
int parent[MAX_SPOTS][MAX_SPOTS][MAX_TREES];  // parent[p][child_index][tree] stores children per tree
int parentCount[MAX_SPOTS][MAX_TREES];  // Count of children for each spot on each tree
int visited[MAX_SPOTS][MAX_TREES];

PriorityQueue* createPQ() {
    PriorityQueue* pq = (PriorityQueue*)malloc(sizeof(PriorityQueue));
    pq->capacity = 10000;
    pq->size = 0;
    pq->data = (State*)malloc(pq->capacity * sizeof(State));
    return pq;
}

void swap(State* a, State* b) {
    State temp = *a;
    *a = *b;
    *b = temp;
}

void heapifyUp(PriorityQueue* pq, int idx) {
    while (idx > 0) {
        int parent = (idx - 1) / 2;
        if (pq->data[idx].energy < pq->data[parent].energy) {
            swap(&pq->data[idx], &pq->data[parent]);
            idx = parent;
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
        
        if (left < pq->size && pq->data[left].energy < pq->data[smallest].energy)
            smallest = left;
        if (right < pq->size && pq->data[right].energy < pq->data[smallest].energy)
            smallest = right;
            
        if (smallest != idx) {
            swap(&pq->data[idx], &pq->data[smallest]);
            idx = smallest;
        } else {
            break;
        }
    }
}

void push(PriorityQueue* pq, State s) {
    if (pq->size >= pq->capacity) {
        pq->capacity *= 2;
        pq->data = (State*)realloc(pq->data, pq->capacity * sizeof(State));
    }
    pq->data[pq->size] = s;
    heapifyUp(pq, pq->size);
    pq->size++;
}

State pop(PriorityQueue* pq) {
    State result = pq->data[0];
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
    newEdge->to = to;
    newEdge->next = adjList[from];
    adjList[from] = newEdge;
}

void addSpotToTree(int spot, int tree) {
    for (int i = 0; i < spotTreeCount[spot]; i++) {
        if (spotTrees[spot][i] == tree) return;
    }
    spotTrees[spot][spotTreeCount[spot]++] = tree;
}

void addParentChild(int p, int c, int tree) {
    parent[p][parentCount[p][tree]++][tree] = c;
}

int isParent(int p, int c, int tree) {
    for (int i = 0; i < parentCount[p][tree]; i++) {
        if (parent[p][i][tree] == c) return 1;
    }
    return 0;
}

int findMinEnergy(int start, int destination) {
    memset(visited, 0, sizeof(visited));
    PriorityQueue* pq = createPQ();
    
    for (int i = 0; i < spotTreeCount[start]; i++) {
        State s = {start, 0, spotTrees[start][i]};
        push(pq, s);
    }
    
    while (!isEmpty(pq)) {
        State current = pop(pq);
        
        if (current.spot == destination) {
            free(pq->data);
            free(pq);
            return current.energy;
        }
        
        if (visited[current.spot][current.tree]) continue;
        visited[current.spot][current.tree] = 1;
        
        // First, consider switching trees at the current spot
        for (int i = 0; i < spotTreeCount[current.spot]; i++) {
            int newTree = spotTrees[current.spot][i];
            if (newTree != current.tree && !visited[current.spot][newTree]) {
                State newState = {current.spot, current.energy + 1, newTree};
                push(pq, newState);
            }
        }
        
        // Now consider moving to adjacent spots on the current tree
        Edge* edge = adjList[current.spot];
        while (edge != NULL) {
            int neighbor = edge->to;
            
            // Check if neighbor is on the current tree
            int neighborOnCurrentTree = 0;
            for (int i = 0; i < spotTreeCount[neighbor]; i++) {
                if (spotTrees[neighbor][i] == current.tree) {
                    neighborOnCurrentTree = 1;
                    break;
                }
            }
            
            if (neighborOnCurrentTree) {
                int energyCost = 0;
                
                // Check if climbing up (neighbor is parent of current on this tree)
                if (isParent(neighbor, current.spot, current.tree)) {
                    energyCost = 1;
                }
                // Otherwise climbing down, cost = 0
                
                int newEnergy = current.energy + energyCost;
                
                if (!visited[neighbor][current.tree]) {
                    State newState = {neighbor, newEnergy, current.tree};
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
    
    memset(adjList, 0, sizeof(adjList));
    memset(spotTreeCount, 0, sizeof(spotTreeCount));
    memset(parentCount, 0, sizeof(parentCount));
    
    int currentTree = 0;
    
    for (int i = 0; i < n; i++) {
        char line[1000];
        fgets(line, sizeof(line), stdin);
        
        // Remove newline
        line[strcspn(line, "\n")] = 0;
        
        if (strcmp(line, "break") == 0) {
            currentTree++;
            continue;
        }
        
        int spots[100];
        int count = 0;
        char* token = strtok(line, " ");
        
        while (token != NULL) {
            spots[count++] = atoi(token);
            token = strtok(NULL, " ");
        }
        
        if (count > 0) {
            int p = spots[0];
            
            for (int j = 1; j < count; j++) {
                int child = spots[j];
                addEdge(p, child);
                addEdge(child, p);
                addSpotToTree(p, currentTree);
                addSpotToTree(child, currentTree);
                addParentChild(p, child, currentTree);
            }
        }
    }
    
    int start, destination;
    scanf("%d %d", &start, &destination);
    
    int result = findMinEnergy(start, destination);
    printf("%d\n", result);
    
    // Free memory
    for (int i = 0; i < MAX_SPOTS; i++) {
        Edge* edge = adjList[i];
        while (edge != NULL) {
            Edge* temp = edge;
            edge = edge->next;
            free(temp);
        }
    }
    
    return 0;
}