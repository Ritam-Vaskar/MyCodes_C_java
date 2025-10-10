#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

#define MAX_NODES 100
#define MAX_NAME 25
#define MAX_CHILDREN 50
#define MAX_PRODUCTS 50

typedef struct {
    char name[MAX_NAME];
    char children[MAX_CHILDREN][MAX_NAME];
    int child_count;
    int switch_count;
    char current_path[MAX_NAME];  
} Junction;

Junction junctions[MAX_NODES];
int junction_count = 0;
int K; 
char products[MAX_PRODUCTS][MAX_NAME];
int product_count = 0;


int findJunction(const char* name) {
    for (int i = 0; i < junction_count; i++) {
        if (strcmp(junctions[i].name, name) == 0) {
            return i;
        }
    }
    return -1;
}


int findParentJunction(const char* name) {
    for (int i = 0; i < junction_count; i++) {
        for (int j = 0; j < junctions[i].child_count; j++) {
            if (strcmp(junctions[i].children[j], name) == 0) {
                return i;
            }
        }
    }
    return -1;
}


bool buildPath(const char* start, char path[][MAX_NAME], int* path_len) {
    *path_len = 0;
    char current[MAX_NAME];
    strcpy(current, start);
    
    
    while (strcmp(current, "center") != 0) {
        int parent_idx = findParentJunction(current);
        if (parent_idx == -1) {
            return false; // Path not found
        }
        
        strcpy(path[(*path_len)++], junctions[parent_idx].name);
        strcpy(current, junctions[parent_idx].name);
        
        if (*path_len > MAX_NODES) {
            return false; 
        }
    }
    
    return *path_len > 0;
}


int calculateCost(const char* product_name) {
    char path[MAX_NODES][MAX_NAME];
    int path_len = 0;
    
    
    if (!buildPath(product_name, path, &path_len)) {
        return 0;
    }
    
    int waiting_time = 0;
    int cooling_time = 0;
    int reset_time = 0;
    
    
    char prev_node[MAX_NAME];
    strcpy(prev_node, product_name);
    
   
    for (int i = 0; i < path_len; i++) {
        int junction_idx = findJunction(path[i]);
        waiting_time++; 
        
       
        if (strlen(junctions[junction_idx].current_path) == 0) {
            
            strcpy(junctions[junction_idx].current_path, prev_node);
            junctions[junction_idx].switch_count++;
            cooling_time++;
        } else if (strcmp(junctions[junction_idx].current_path, prev_node) != 0) {
           
            if (junctions[junction_idx].switch_count < K) {
                
                strcpy(junctions[junction_idx].current_path, prev_node);
                junctions[junction_idx].switch_count++;
                cooling_time++;
            } else {
                reset_time++;
            }
        }
        
        strcpy(prev_node, path[i]);
    }
    
    return waiting_time + cooling_time * 2 + reset_time * 3;
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
    
   
    for (int i = 0; i < n; i++) {
        char line[1000];
        if (fgets(line, sizeof(line), fp) == NULL) break;
        
        char* token = strtok(line, " \n");
        if (token == NULL) continue;
        
    
        strcpy(junctions[junction_count].name, token);
        junctions[junction_count].child_count = 0;
        junctions[junction_count].switch_count = 0;
        junctions[junction_count].current_path[0] = '\0';
        
        
        while ((token = strtok(NULL, " \n")) != NULL) {
            strcpy(junctions[junction_count].children[junctions[junction_count].child_count++], token);
        }
        
        junction_count++;
    }
    
   
    char product_line[1000];
    if (fgets(product_line, sizeof(product_line), fp) != NULL) {
        char* token = strtok(product_line, " \n");
        while (token != NULL) {
            strcpy(products[product_count++], token);
            token = strtok(NULL, " \n");
        }
    }
    

    fscanf(fp, "%d", &K);
    
    if (fp != stdin) {
        fclose(fp);
    }
    
   
    int total_time = 0;
    for (int i = 0; i < product_count; i++) {
        int cost = calculateCost(products[i]);
        total_time += cost;
    }
    
    printf("%d\n", total_time);
    
    return 0;
}
