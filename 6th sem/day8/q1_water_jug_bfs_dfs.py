from collections import deque


class WaterJugSolver:
    def __init__(self, jug1_capacity, jug2_capacity, target):
        self.jug1_capacity = jug1_capacity
        self.jug2_capacity = jug2_capacity
        self.target = target

    def is_goal(self, state):
        x, y = state
        return x == self.target or y == self.target

    def get_next_states(self, state):
        x, y = state

        next_states = set()

        next_states.add((self.jug1_capacity, y))
        next_states.add((x, self.jug2_capacity))

        next_states.add((0, y))
        next_states.add((x, 0))

        transfer_to_jug2 = min(x, self.jug2_capacity - y)
        next_states.add((x - transfer_to_jug2, y + transfer_to_jug2))

        transfer_to_jug1 = min(y, self.jug1_capacity - x)
        next_states.add((x + transfer_to_jug1, y - transfer_to_jug1))

        next_states.discard(state)
        return sorted(next_states)

    def reconstruct_path(self, parent, end_state):
        path = []
        current = end_state

        while current is not None:
            path.append(current)
            current = parent[current]

        path.reverse()
        return path

    def solve_bfs(self):
        start = (0, 0)
        queue = deque([start])
        visited = {start}
        parent = {start: None}

        while queue:
            current = queue.popleft()

            if self.is_goal(current):
                return self.reconstruct_path(parent, current)

            for nxt in self.get_next_states(current):
                if nxt not in visited:
                    visited.add(nxt)
                    parent[nxt] = current
                    queue.append(nxt)

        return None

    def solve_dfs(self):
        start = (0, 0)
        stack = [start]
        visited = {start}
        parent = {start: None}

        while stack:
            current = stack.pop()

            if self.is_goal(current):
                return self.reconstruct_path(parent, current)

            for nxt in reversed(self.get_next_states(current)):
                if nxt not in visited:
                    visited.add(nxt)
                    parent[nxt] = current
                    stack.append(nxt)

        return None


def print_solution(path, method_name):
    print("\n" + "=" * 60)
    print(f"Water Jug Problem using {method_name}")
    print("=" * 60)

    if path is None:
        print("No solution found.")
        return

    print(f"Total Steps: {len(path) - 1}")
    print("Path:")
    for i, (x, y) in enumerate(path):
        print(f"Step {i:2d}: Jug1 = {x}L, Jug2 = {y}L")


def main():
    jug1_capacity = 4
    jug2_capacity = 3
    target = 2

    solver = WaterJugSolver(jug1_capacity, jug2_capacity, target)

    print("Water Jug Problem")
    print(f"Jug1 Capacity: {jug1_capacity}L")
    print(f"Jug2 Capacity: {jug2_capacity}L")
    print(f"Target: {target}L")

    bfs_path = solver.solve_bfs()
    print_solution(bfs_path, "BFS")

    dfs_path = solver.solve_dfs()
    print_solution(dfs_path, "DFS")


if __name__ == "__main__":
    main()
