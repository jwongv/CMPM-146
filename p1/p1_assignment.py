from p1_support import load_level, show_level
from math import sqrt
from heapq import heappush, heappop

def dijkstras_shortest_path(src, dst, graph, adj):
	
	#Intialize previous and distance dictionary as well as visited list
	#Initialize the queue with the src
	prev = {}
	dist = {}
	visited = []
	prev[src] = None
	dist[src] = 0
	queue = [(0, src)]
	node_dist = None
	node_pos = None

	while queue:
		#Pop the lowest distnace node
		node_dist, node_pos = heappop(queue)
		#If we found the goal node, break
		if node_pos == dst:
			break
		#Get a list of accessible neighbor nodes and iterate through them
		#Once we've iterated through all neighbors, append the node to visited list
		neighbors = adj(graph, node_pos)
		for next_node in neighbors:
			next_dist, next_pos = next_node
			#If the neighbor has not been visited, calculate it's tentative distance
			#If the neighbor is not in the dist dictionary or its tentative distance is lower than it's current listed one
			#Update its dist and prev and add it to the queue
			if next_pos not in visited:
				temp_dist = node_dist + next_dist
				if next_pos not in dist or temp_dist < dist[next_pos]:
					dist[next_pos] = temp_dist
					prev[next_pos] = node_pos
					heappush(queue, (temp_dist, next_pos))
		visited.append(node_pos)

	#Return the path from src to dst if possible
	#Backtrack from dst using prev dictionary.
	#Reverse the path and return it
	if node_pos == dst:
		path = []
		while node_pos:
			path.append(node_pos)
			node_pos = prev[node_pos]
		path.reverse()
		return path
	else:
		return []



def navigation_edges(level, cell):
	#Initialize neighbor list
	neighbors = []
	x, y = cell
	#Iterate through all combinations of neighboring nodes
	#Add neighbors to list if they are 'spaces' and not our current node
	for dx in [-1, 0, 1]:
  		for dy in [-1, 0, 1]:
  			adjacent_cell = (x + dx, y + dy)
  			dist = sqrt(dx * dx + dy * dy)
  			if dist > 0 and adjacent_cell in level['spaces']:
  				neighbors.append( (dist, adjacent_cell) )
  	return neighbors

def test_route(filename, src_waypoint, dst_waypoint):
	level = load_level(filename)

	show_level(level)

	src = level['waypoints'][src_waypoint]
	dst = level['waypoints'][dst_waypoint]

	path = dijkstras_shortest_path(src, dst, level, navigation_edges)

	if path:
		show_level(level, path)
	else:
		print "No path possible!"

if __name__ ==  '__main__':
	import sys
	_, filename, src_waypoint, dst_waypoint = sys.argv
	test_route(filename, src_waypoint, dst_waypoint)
