from p6_game import Simulator
import Queue

ANALYSIS = {}

def analyze(design):
	sim = Simulator(design)
	init = sim.get_initial_state()
	moves = sim.get_moves()
	next_state = sim.get_next_state(init, moves[0])

	queue = Queue.Queue()
	prev = {}
	visited = []
	prev[init] = None

	queue.put(init)
	visited.append(init)
	while not queue.empty():
		current_state = queue.get()
		for move in moves:
			next_state = sim.get_next_state(current_state, move)
			position, abilities = next_state
			if next_state not in visited:
				prev[next_state] = current_state
				queue.put(next_state)
				visited.append(next_state)

def inspect((i,j), draw_line):
    # TODO: use ANALYSIS and (i,j) draw some lines
    raise NotImplementedError
