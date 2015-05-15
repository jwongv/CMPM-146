from p6_game import Simulator
from collections import deque

ANALYSIS = {}

def analyze(design):
	ANALYSIS.clear()
	sim = Simulator(design)
	init = sim.get_initial_state()
	moves = sim.get_moves()
	next_state = sim.get_next_state(init, moves[0])


	queue = deque([])
	visited = []
	ANALYSIS[init] = None

	queue.append(init)
	visited.append(init)
	while len(queue) > 0:
		current_state = queue.popleft()

		if current_state[0] == (8,2):
			print "Goal is reachable with the following ability combination:"
			for ability in current_state[1]:
				print ability
			if len(current_state[1]) == 0:
				print "Does not require any abilities!"

		for move in moves:
			next_state = sim.get_next_state(current_state, move)
			#position, abilities = next_state
			if next_state == None:
				continue
			if next_state not in visited:
				ANALYSIS[next_state] = current_state
				queue.append(next_state)
				visited.append(next_state)

def inspect((i,j), draw_line):
	reachable = False
	current_state = None
	current_abilities = []
	line_color = 0
	line_offset = 0
	possible_end_states = []

	for state in ANALYSIS:
		if state[0] == (i,j):
			reachable = True
			possible_end_states.append(state)

	if reachable:
		print "(%d,%d) is reachable!" %(i,j)
	else:
		print "(%d,%d) is unreachable!" %(i,j)

	for state in possible_end_states:
		current_state = state
		current_abilities = state[1]
		while current_state and ANALYSIS[current_state]:
			draw_line(current_state[0], ANALYSIS[current_state][0], current_abilities, current_state[1])
			current_state = ANALYSIS[current_state]

    