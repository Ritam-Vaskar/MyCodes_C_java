import networkx as nx
import matplotlib.pyplot as plt
from collections import deque
import time

# -----------------------------
# Graph Construction
# -----------------------------

graph = {
    "KIIT_Square": ["Campus_6", "Campus_3"],
    "Campus_6": ["KIIT_Square", "Campus_3", "KIIT_Sports_Complex"],
    "Campus_3": ["KIIT_Square", "Campus_6", "Campus_14"],
    "Campus_14": ["Campus_3", "Campus_25"],
    "KIIT_Sports_Complex": ["Campus_6", "Campus_25"],
    "Campus_25": ["KIIT_Sports_Complex", "Campus_14"]
}

start = "KIIT_Square"
goal = "Campus_25"

# -----------------------------
# BFS Implementation
# -----------------------------

def bfs(graph, start, goal):
    visited = set()
    queue = deque([[start]])
    nodes_explored = 0

    while queue:
        path = queue.popleft()
        node = path[-1]
        nodes_explored += 1

        if node == goal:
            return path, nodes_explored

        if node not in visited:
            visited.add(node)
            for neighbor in graph[node]:
                new_path = list(path)
                new_path.append(neighbor)
                queue.append(new_path)

    return None, nodes_explored

# -----------------------------
# DFS Implementation
# -----------------------------

def dfs(graph, start, goal):
    visited = set()
    stack = [[start]]
    nodes_explored = 0

    while stack:
        path = stack.pop()
        node = path[-1]
        nodes_explored += 1

        if node == goal:
            return path, nodes_explored

        if node not in visited:
            visited.add(node)
            for neighbor in graph[node]:
                new_path = list(path)
                new_path.append(neighbor)
                stack.append(new_path)

    return None, nodes_explored

# -----------------------------
# Bi-Directional BFS
# -----------------------------

def bidirectional_bfs(graph, start, goal):
    if start == goal:
        return [start], 1

    forward_queue = deque([[start]])
    backward_queue = deque([[goal]])

    forward_visited = {start: [start]}
    backward_visited = {goal: [goal]}

    nodes_explored = 0

    while forward_queue and backward_queue:
        # Forward step
        path = forward_queue.popleft()
        node = path[-1]
        nodes_explored += 1

        for neighbor in graph[node]:
            if neighbor not in forward_visited:
                new_path = path + [neighbor]
                forward_visited[neighbor] = new_path
                forward_queue.append(new_path)

                if neighbor in backward_visited:
                    return new_path + backward_visited[neighbor][::-1][1:], nodes_explored

        # Backward step
        path = backward_queue.popleft()
        node = path[-1]
        nodes_explored += 1

        for neighbor in graph[node]:
            if neighbor not in backward_visited:
                new_path = path + [neighbor]
                backward_visited[neighbor] = new_path
                backward_queue.append(new_path)

                if neighbor in forward_visited:
                    return forward_visited[neighbor] + new_path[::-1][1:], nodes_explored

    return None, nodes_explored

# -----------------------------
# Run Algorithms
# -----------------------------

bfs_path, bfs_nodes = bfs(graph, start, goal)
dfs_path, dfs_nodes = dfs(graph, start, goal)
bibfs_path, bibfs_nodes = bidirectional_bfs(graph, start, goal)

print("BFS Path:", bfs_path)
print("BFS Nodes Explored:", bfs_nodes)
print()

print("DFS Path:", dfs_path)
print("DFS Nodes Explored:", dfs_nodes)
print()

print("Bi-BFS Path:", bibfs_path)
print("Bi-BFS Nodes Explored:", bibfs_nodes)

# -----------------------------
# Graph Visualization
# -----------------------------

G = nx.Graph()

for node in graph:
    for neighbor in graph[node]:
        G.add_edge(node, neighbor)

# Manual positioning to match Google Maps layout
# Coordinates match the actual map orientation from the image
pos = {
    "KIIT_Square": (5, 0),              # Far right (start point)
    "Campus_6": (3, 0.3),               # Center-right
    "Campus_3": (1.5, 0),               # Center-left
    "Campus_14": (0.2, 1.8),            # Left-middle area
    "KIIT_Sports_Complex": (2.5, 1.5),  # Upper-middle
    "Campus_25": (0, 3)                 # Top-left (destination)
}

# Alternative: Use spring layout (automatic positioning)
# pos = nx.spring_layout(G, seed=42)

plt.figure(figsize=(12, 8))
nx.draw(G, pos, with_labels=True, node_size=3000, node_color="lightblue")

# Highlight shortest path (Bi-BFS)
path_edges = list(zip(bibfs_path, bibfs_path[1:]))
nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color="red", width=3)

plt.title("City Map Graph with Shortest Path Highlighted")
plt.show()
