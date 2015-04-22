"""
__author__ = 'Kevin'

from math import *
from heapq import heappush, heappop


def find_path(src_point, dst_point, mesh):
    path = []
    visited_boxes = []

    curr_dist = {}
    prev_dist = {}

    dst_box = None
    src_box = None

    queue = []

    detail_points = {}

    for x1, x2, y1, y2 in mesh['boxes']:

        if x1 < src_point[0] < x2 and y1 < src_point[1] < y2:
            src_box = (x1, x2, y1, y2)
            visited_boxes.append(src_box)

        if x1 < dst_point[0] < x2 and y1 < dst_point[1] < y2:
            dst_box = (x1, x2, y1, y2)

    curr_dist[src_box] = 0
    prev_dist[src_box] = None

    heappush(queue, (0, src_box))
    detail_points[src_box] = src_point

    while not len(queue) == 0:

        distance, curr_box = heappop(queue)  # pop lowest out of queue

        final_dist = sqrt(pow((detail_points[curr_box][0] - dst_point[0]), 2) + pow((detail_points[curr_box][1] - dst_point[1]), 2))
        distance = distance - final_dist

        if curr_box == dst_box or src_box is None or dst_box is None:
            visited_boxes.append(curr_box)
            break

        for adj_box in mesh['adj'][curr_box]:
            if adj_box not in visited_boxes:
                x, y = detail_points[curr_box]
                adj_dist, final_dist, detail_points[adj_box] = calculate_box_points(x, y, dst_point, adj_box)

                path_len = distance + adj_dist

                if adj_box not in curr_dist or path_len < curr_dist[adj_box]:

                    curr_dist[adj_box] = path_len
                    prev_dist[adj_box] = curr_box

                    heappush(queue, (path_len + final_dist, adj_box))
        visited_boxes.append(curr_box)

    if curr_box == dst_box:
        detail_points[dst_box] = dst_point
        while curr_box and prev_dist[curr_box]:
            path.append((detail_points[curr_box], detail_points[prev_dist[curr_box]]))
            curr_box = prev_dist[curr_box]

        path.reverse()
    else:
        print "No path found. =("

    return path, visited_boxes


def calculate_box_points(x, y, dst_point, adj_box):

    x1, x2 = adj_box[0], adj_box[1]
    x_next = min(x2 - 1, max(x1, x))

    y1, y2 = adj_box[2], adj_box[3]
    y_next = min(y2 - 1, max(y1, y))

    dist = sqrt(pow((x_next - x), 2) + pow((y_next - y), 2))

    final_dist = sqrt(pow((x_next - dst_point[0]), 2) + pow((y_next - dst_point[1]), 2))

    return dist, final_dist, (x_next, y_next)





"""

__author__ = 'Kevin'

from math import *
from heapq import heappush, heappop


def find_path(src_point, dst_point, mesh):
    path = []
    visited_boxes = []

    curr_dist_foward = {}
    prev_dist_foward = {}
    curr_dist_backward = {}
    prev_dist_backward = {}

    path_found = False

    dst_box = None
    src_box = None

    last_foward_box = None
    last_backward_box = None

    queue = []

    detail_points = {}

    for x1, x2, y1, y2 in mesh['boxes']:

        if x1 < src_point[0] < x2 and y1 < src_point[1] < y2:
            src_box = (x1, x2, y1, y2)
            visited_boxes.append(src_box)

        if x1 < dst_point[0] < x2 and y1 < dst_point[1] < y2:
            dst_box = (x1, x2, y1, y2)

    curr_dist_foward[src_box] = 0
    prev_dist_foward[src_box] = None

    curr_dist_backward[dst_box] = 0
    prev_dist_backward[dst_box] = None

    heappush(queue, (0, src_box, dst_box))
    heappush(queue, (0, dst_box, src_box))
    detail_points[src_box] = src_point
    detail_points[dst_box] = dst_point

    while not len(queue) == 0:

        distance, curr_box, curr_goal = heappop(queue)  # pop lowest out of queue

        if curr_goal == dst_box:

            final_dist = sqrt(pow((detail_points[curr_box][0] - dst_point[0]), 2) + pow((detail_points[curr_box][1] - dst_point[1]), 2))
            distance = distance - final_dist

            if curr_box == dst_box or src_box is None or dst_box is None or curr_box in curr_dist_backward:
                visited_boxes.append(curr_box)
                path_found = True
                last_box = curr_box
                break

        if curr_goal == src_box:

            final_dist = sqrt(pow((detail_points[curr_box][0] - src_point[0]), 2) + pow((detail_points[curr_box][1] - src_point[1]), 2))
            distance = distance - final_dist

            if curr_box == src_box or dst_box is None or src_box is None or curr_box in curr_dist_foward:
                visited_boxes.append(curr_box)
                path_found = True
                last_box = curr_box
                break

        for adj_box in mesh['adj'][curr_box]:
            if adj_box not in visited_boxes:
                x, y = detail_points[curr_box]

                if curr_goal == dst_box:
                    adj_dist, final_dist, detail_points[adj_box] = calculate_box_points(x, y, dst_point, adj_box)

                if curr_goal == src_box:
                    adj_dist, final_dist, detail_points[adj_box] = calculate_box_points(x, y, src_point, adj_box)

                path_len = distance + adj_dist


                if curr_goal == dst_box:
                    if adj_box not in curr_dist_foward or path_len < curr_dist_foward[adj_box]:

                        curr_dist_foward[adj_box] = path_len
                        prev_dist_foward[adj_box] = curr_box

                        heappush(queue, (path_len + final_dist, adj_box, dst_box))
                        last_box = curr_box

                if curr_goal == src_box:
                    if adj_box not in curr_dist_backward or path_len < curr_dist_backward[adj_box]:

                        curr_dist_backward[adj_box] = path_len
                        prev_dist_backward[adj_box] = curr_box

                        heappush(queue, (path_len + final_dist, adj_box, src_box))
                        last_box = curr_box

        visited_boxes.append(curr_box)



    if path_found:
        curr_foward_box = last_box
        while curr_foward_box and prev_dist_foward[curr_foward_box]:
            path.append((detail_points[curr_foward_box], detail_points[prev_dist_foward[curr_foward_box]]))
            curr_foward_box = prev_dist_foward[curr_foward_box]

        curr_backward_box = last_box
        while curr_backward_box and prev_dist_backward[curr_backward_box]:
            path.append((detail_points[curr_backward_box], detail_points[prev_dist_backward[curr_backward_box]]))
            curr_backward_box = prev_dist_backward[curr_backward_box]



    else:
        print "No path found. =("

    return path, visited_boxes


def calculate_box_points(x, y, dst_point, adj_box):

    x1, x2 = adj_box[0], adj_box[1]
    x_next = min(x2 - 1, max(x1, x))

    y1, y2 = adj_box[2], adj_box[3]
    y_next = min(y2 - 1, max(y1, y))

    dist = sqrt(pow((x_next - x), 2) + pow((y_next - y), 2))

    final_dist = sqrt(pow((x_next - dst_point[0]), 2) + pow((y_next - dst_point[1]), 2))

    return dist, final_dist, (x_next, y_next)
