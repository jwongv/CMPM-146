import json
from collections import namedtuple
from heapq import heappush, heappop

with open('Crafting.json') as f:
	Crafting = json.load(f)

item_index = {}
Items = Crafting['Items']
#Setup item_index dictionary
for i in range(len(Items)):
	item_index[Items[i]] = i




def make_checker(rule):
	  # this code runs once
	  # do something with rule['Consumes'] and rule['Requires']
	requires = None
  	consumes = None
  	if 'Requires' in rule:
  		requires = rule['Requires']
  	if 'Consumes' in rule:
  		consumes = rule['Consumes']
	def check(state):
		if consumes:
			for i in consumes:
				if state[item_index[i]] < consumes[i]:
					return False

		if requires:
			for i in requires:
				if state[item_index[i]] < 1:
					return False

		return True
	
	return check

def make_effector(rule):
	  # this code runs once
  # do something with rule['Produces'] and rule['Consumes']
  	consumes = None
  	produces = rule['Produces']
  	if 'Consumes' in rule:
  		consumes = rule['Consumes']
	def effect(state):
		#Convert state to list
		next_state_list = list(state)
		if consumes:
			for i in consumes:
				next_state_list[item_index[i]] = state[item_index[i]] - consumes[i]
		for i in produces:
			next_state_list[item_index[i]] = state[item_index[i]] + produces[i]

		return tuple(next_state_list)
	
	return effect

def make_goal_checker(goal):
	#Convert goal to tuple and compare to inventory
	goal_tuple = inventory_to_tuple(goal)
	def is_goal(state):
		for i in range(len(state)):
			if state[i] < goal_tuple[i]:
				return False
		print "Goal Found!"
		return True
	return is_goal

def make_initial_state(inventory):
	state = inventory_to_tuple(inventory)
	#state = inventory_to_frozenset(inventory_tuple)
	return state


def search(graph, initial, is_goal, limit, heuristic):

	dist = {}
	prev = {}
	actions = {}
	visited = []
	queue = []
	current_state = initial
	heappush(queue,(0,current_state))
	current_dist = None
	current_node = None
	prev[initial] = None
	dist[initial] = 0
	actions[initial] = None

	while queue:
		current_dist, current_node = heappop(queue)
		if is_goal(current_node):
			break
		#Might need to check if not start state. Otherwise we need to remove the heuristic
		if current_node != initial:
			current_dist = current_dist - heuristic(current_node)
		for action, next_state, cost in graph(current_node):
			if next_state not in visited:
				temp_dist = current_dist + cost
				if next_state not in dist or temp_dist < dist[next_state]:
					dist[next_state] = temp_dist
					prev[next_state] = current_node
					actions[next_state] = action
					heappush(queue, (temp_dist + heuristic(next_state), next_state))
		visited.append(current_node)


	plan = []
	total_cost = current_dist
	if is_goal(current_node):
		while current_node and actions[current_node]:
			plan.append(actions[current_node])
			current_node = prev[current_node]
		plan.reverse()

	return total_cost, plan


def inventory_to_tuple(d):
	return tuple(d.get(name,0) for i,name in enumerate(Items))


initial_state = make_initial_state(Crafting['Initial'])
is_goal = make_goal_checker(Crafting['Goal'])

def heuristic(state):
	if (state[0] > 1 or state[1] > 1 or state[2] > 1 or state[4] > 1 or state[6] > 1 or state[7] > 1 or state[8] > 1 or state[12] > 1 or state[13] > 1 or state[14] > 1 or state[15] > 1 or state[16] > 1):
		return 1000
	if (state[11] > 6):
		return 1000
	if (state[9] > 7):
		return 1000
	if (state[5] > 6):
		return 1000
	if (state[3] > 8):
		return 1000
	if (state[10] > 16):
		return 1000
	return 0

Recipe = namedtuple('Recipe',['name','check','effect','cost'])
all_recipes = []
for name, rule in Crafting['Recipes'].items():
	checker = make_checker(rule)
	effector = make_effector(rule)
	recipe = Recipe(name, checker, effector, rule['Time'])
	all_recipes.append(recipe)

def graph(state):
	for r in all_recipes:
		if r.check(state):
			yield(r.name, r.effect(state), r.cost)


print search(graph, initial_state, is_goal, 50, heuristic)

"""
t_initial = 'a'
t_limit = 20

edges = {'a': {'b':1,'c':10}, 'b':{'c':1}}

def t_graph(state):
	for next_state, cost in edges[state].items():
		yield ((state,next_state), next_state, cost)

def t_is_goal(state):
	return state == 'c'

def t_heuristic(state):
	return 0

print search(t_graph, t_initial, t_is_goal, t_limit, t_heuristic)
"""

