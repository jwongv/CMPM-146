"""
from collections import deque

def find_path(source_point, destination_point, mesh):

	path = []
	visited_boxes = []
	queue = deque([])
	src_box = None
	dst_box = None
	prev = {}
	detail_points = {}

	for x1, x2, y1, y2 in mesh['boxes']:

		if source_point[0] > x1 and source_point[0] < x2 and source_point[1] > y1 and source_point[1] < y2:
			src_box = (x1, x2, y1, y2)
			queue.append(src_box)
		if destination_point[0] > x1 and destination_point[0] < x2 and destination_point[1] > y1 and destination_point[1] < y2:
			dst_box = (x1, x2, y1, y2)

	current_box = None
	visited_boxes.append(src_box)
	prev[src_box] = None
	detail_points[src_box] = source_point
	while len(queue) > 0:
		current_box = queue.popleft()
		if current_box == dst_box:
			break
		for next_box in mesh['adj'][current_box]:
			if next_box not in visited_boxes:

				x, y = detail_points[current_box]
				x1, x2 = next_box[0], next_box[1]
				x_next = min(x2 - 1, max(x1, x))

				y1, y2 = next_box[2], next_box[3]
				y_next = min(y2 - 1, max(y1,y))

				detail_points[next_box] = (x_next, y_next)

				queue.append(next_box)
				visited_boxes.append(next_box)
				prev[next_box] = current_box


	if current_box == dst_box:
		detail_points[dst_box] = destination_point
		while prev[current_box]:
			path.append((     detail_points[current_box], detail_points[prev[current_box]]      ))
			current_box = prev[current_box]
		path.reverse()



	return path, visited_boxes
"""

"""
from heapq import heappush, heappop
from math import sqrt

def find_path(source_point, destination_point, mesh):

	path = []
	visited_boxes = []
	src_box = None
	dst_box = None
	prev = {}
	dist = {}
	detail_points = {}

	for x1, x2, y1, y2 in mesh['boxes']:

		if source_point[0] > x1 and source_point[0] < x2 and source_point[1] > y1 and source_point[1] < y2:
			src_box = (x1, x2, y1, y2)
			#visited_boxes.append(src_box)
		if destination_point[0] > x1 and destination_point[0] < x2 and destination_point[1] > y1 and destination_point[1] < y2:
			dst_box = (x1, x2, y1, y2)


	queue = [(0, src_box)]
	current_box = None
	#visited_boxes.append(src_box)
	prev[src_box] = None
	dist[src_box] = None
	detail_points[src_box] = source_point
	current_dist = None


	while queue:

		current_dist, current_box = heappop(queue)
		final_dist = sqrt(   (detail_points[current_box][0] - destination_point[0])*(detail_points[current_box][0] - destination_point[0]) + (detail_points[current_box][1] - destination_point[1])*(detail_points[current_box][1] - destination_point[1])     )
		current_dist = current_dist - final_dist

		if current_box == dst_box:
			visited_boxes.append(current_box)
			break

		for next_box in mesh['adj'][current_box]:
			if next_box not in visited_boxes:

				x, y = detail_points[current_box]
				x1, x2 = next_box[0], next_box[1]
				x_next = min(x2 - 1, max(x1, x))

				y1, y2 = next_box[2], next_box[3]
				y_next = min(y2 - 1, max(y1,y))

				detail_points[next_box] = (x_next, y_next)

				next_dist = sqrt( (x_next - detail_points[current_box][0])*(x_next - detail_points[current_box][0]) +  (y_next - detail_points[current_box][1])*(y_next - detail_points[current_box][1])     )

				final_dist = sqrt(  (x_next - destination_point[0])*(x_next - destination_point[0]) + (y_next - destination_point[1])*(y_next - destination_point[1])        )

				temp_dist = current_dist + next_dist
				if next_box not in dist or temp_dist < dist[next_box]:
					dist[next_box] = temp_dist
					prev[next_box] = current_box
					heappush(queue, ( temp_dist + final_dist, next_box )  )
		visited_boxes.append(current_box)



	if current_box == dst_box:
		detail_points[dst_box] = destination_point
		while prev[current_box]:
			path.append((     detail_points[current_box], detail_points[prev[current_box]]      ))
			current_box = prev[current_box]
		path.reverse()



	return path, visited_boxes
"""

from heapq import heappush, heappop
from math import sqrt

def find_path(source_point, destination_point, mesh):

	path = []
	visited_boxes = []
	src_box = None
	dst_box = None
	prev = {}
	dist = {}
	detail_points = {}

	for x1, x2, y1, y2 in mesh['boxes']:

		if source_point[0] > x1 and source_point[0] < x2 and source_point[1] > y1 and source_point[1] < y2:
			src_box = (x1, x2, y1, y2)
			#visited_boxes.append(src_box)
		if destination_point[0] > x1 and destination_point[0] < x2 and destination_point[1] > y1 and destination_point[1] < y2:
			dst_box = (x1, x2, y1, y2)


	queue = [(0, src_box)]
	current_box = None
	#visited_boxes.append(src_box)
	prev[src_box] = None
	dist[src_box] = None
	detail_points[src_box] = source_point
	current_dist = None


	while queue:

		current_dist, current_box = heappop(queue)
		final_dist = sqrt(   (detail_points[current_box][0] - destination_point[0])*(detail_points[current_box][0] - destination_point[0]) + (detail_points[current_box][1] - destination_point[1])*(detail_points[current_box][1] - destination_point[1])     )
		current_dist = current_dist - final_dist

		if current_box == dst_box:
			visited_boxes.append(current_box)
			break

		for next_box in mesh['adj'][current_box]:
			if next_box not in visited_boxes:

				x, y = detail_points[current_box]
				x1, x2 = next_box[0], next_box[1]
				x_next = min(x2 - 1, max(x1, x))

				y1, y2 = next_box[2], next_box[3]
				y_next = min(y2 - 1, max(y1,y))

				detail_points[next_box] = (x_next, y_next)

				next_dist = sqrt( (x_next - detail_points[current_box][0])*(x_next - detail_points[current_box][0]) +  (y_next - detail_points[current_box][1])*(y_next - detail_points[current_box][1])     )

				final_dist = sqrt(  (x_next - destination_point[0])*(x_next - destination_point[0]) + (y_next - destination_point[1])*(y_next - destination_point[1])        )

				temp_dist = current_dist + next_dist
				if next_box not in dist or temp_dist < dist[next_box]:
					dist[next_box] = temp_dist
					prev[next_box] = current_box
					heappush(queue, ( temp_dist + final_dist, next_box )  )
		visited_boxes.append(current_box)



	if current_box == dst_box:
		detail_points[dst_box] = destination_point
		while prev[current_box]:
			path.append((     detail_points[current_box], detail_points[prev[current_box]]      ))
			current_box = prev[current_box]
		path.reverse()



	return path, visited_boxes