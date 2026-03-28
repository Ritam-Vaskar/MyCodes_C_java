from collections import deque
class TowerOfHanoiSolver:
	def __init__(self, num_disks=5):
		self.num_disks = num_disks
		self.start = (tuple(range(num_disks, 0, -1)), tuple(), tuple())
		self.goal = (tuple(), tuple(), tuple(range(num_disks, 0, -1)))
	def is_goal(self, state):
		return state == self.goal
	def get_next_states(self, state):
		pegs = [list(peg) for peg in state]
		next_states = []
		for from_peg in range(3):
			if not pegs[from_peg]:
				continue
			moving_disk = pegs[from_peg][-1]
			for to_peg in range(3):
				if from_peg == to_peg:
					continue
				if not pegs[to_peg] or pegs[to_peg][-1] > moving_disk:
					new_pegs = [list(peg) for peg in pegs]
					new_pegs[from_peg].pop()
					new_pegs[to_peg].append(moving_disk)
					new_state = tuple(tuple(peg) for peg in new_pegs)
					move = (from_peg, to_peg, moving_disk)
					next_states.append((new_state, move))
		return next_states
	def reconstruct_path(self, parent, move_taken, end_state):
		states = []
		moves = []
		current = end_state
		while current is not None:
			states.append(current)
			moves.append(move_taken.get(current))
			current = parent[current]
		states.reverse()
		moves.reverse()
		return states, moves[1:]

	def solve_bfs(self):
		queue = deque([self.start])
		visited = {self.start}
		parent = {self.start: None}
		move_taken = {self.start: None}

		while queue:
			current = queue.popleft()

			if self.is_goal(current):
				return self.reconstruct_path(parent, move_taken, current)

			for nxt_state, move in self.get_next_states(current):
				if nxt_state not in visited:
					visited.add(nxt_state)
					parent[nxt_state] = current
					move_taken[nxt_state] = move
					queue.append(nxt_state)

		return None, None

	def solve_dfs(self):
		stack = [self.start]
		visited = {self.start}
		parent = {self.start: None}
		move_taken = {self.start: None}

		while stack:
			current = stack.pop()

			if self.is_goal(current):
				return self.reconstruct_path(parent, move_taken, current)

			for nxt_state, move in reversed(self.get_next_states(current)):
				if nxt_state not in visited:
					visited.add(nxt_state)
					parent[nxt_state] = current
					move_taken[nxt_state] = move
					stack.append(nxt_state)

		return None, None


def format_state(state):
	labels = ["A", "B", "C"]
	parts = []
	for i, peg in enumerate(state):
		parts.append(f"{labels[i]}:{list(peg)}")
	return " | ".join(parts)


def print_solution(states, moves, method_name):
	print("\n" + "=" * 60)
	print(f"Tower of Hanoi using {method_name}")
	print("=" * 60)

	if states is None:
		print("No solution found.")
		return

	print(f"Total Moves: {len(moves)}")
	print(f"Initial State: {format_state(states[0])}")

	for i, (move, state) in enumerate(zip(moves, states[1:]), start=1):
		from_peg, to_peg, disk = move
		print(
			f"Step {i:2d}: Move disk {disk} from "
			f"{chr(65 + from_peg)} -> {chr(65 + to_peg)}"
		)
		print(f"         {format_state(state)}")


def main():
	num_disks = 5
	solver = TowerOfHanoiSolver(num_disks=num_disks)

	print("Tower of Hanoi Problem")
	print(f"Number of stacked disks: {num_disks}")
	print("Source: A, Auxiliary: B, Destination: C")

	bfs_states, bfs_moves = solver.solve_bfs()
	print_solution(bfs_states, bfs_moves, "BFS")

	dfs_states, dfs_moves = solver.solve_dfs()
	print_solution(dfs_states, dfs_moves, "DFS")


if __name__ == "__main__":
	main()