import pygame
from constants import *
from path import reconstruct_path


def dijkstra(start, goal, grid):
    unvisited = [node for row in grid for node in row]
    distance = {node: INFINITY for row in grid for node in row}
    distance[start] = 0
    came_from = {}
    current = start

    while unvisited:

        minimum = INFINITY

        for node in unvisited:
            if distance[node] < minimum:
                minimum = distance[node]

        for node in unvisited:
            if distance[node] == minimum:
                current = node
                unvisited.remove(current)
                break

        if current == goal:
            reconstruct_path(start, current, came_from)
            return True

        for neighbor in current.neighbors:
            alt = distance[current] + 1
            if alt < distance[neighbor]:
                distance[neighbor] = alt
                came_from[neighbor] = current

        if current != start:
            current.add_block(GREEN)
        pygame.display.update()

    return False

# Dijkstra's algorithm - steps break down
# 1. Create a list of all the unvisited nodes called the unvisited set.
# 2. Set distance of the initial node to zero and to to infinity for all other nodes.
# 3. Have the current node being the node with the shortest distance in the list of
#    unvisited nodes and remove this node from the list.
# 4. For the current node, consider all of its unvisited neighbors and calculate their
#    tentative distances through the current node. Compare the newly calculated tentative
#    distance to the current assigned value and assign the smaller one. If a better path
#    is found, store the neighbor and its current (the node that leads to neighbor) into
#    the came_from.
# 5. If the current node is the destination node or if the smallest tentative distance
#    among the nodes in the unvisited set is infinity (occurs when there is no connection
#    between the initial node and remaining unvisited nodes), then stop. The algorithm has
#    finished.
# 6. Otherwise, go back to step 3.
