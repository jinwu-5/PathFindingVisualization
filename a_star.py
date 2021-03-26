import pygame
from constants import *
from path import reconstruct_path


def h(current, goal):
    """heuristic function -> return the estimated distance from node n to the goal node"""

    x_1, y_1 = current.get_pos()
    x_2, y_2 = goal.get_pos()

    return abs(x_2 - x_1) + abs(y_2 - y_1)


def a_star(start, goal, grid):
    open_set = set()
    open_set.add(start)
    g_score = {node: INFINITY for row in grid for node in row}
    g_score[start] = 0
    f_score = {node: INFINITY for row in grid for node in row}
    f_score[start] = h(start, goal)
    came_from = {}
    current = start

    while open_set:

        minimum = INFINITY

        for node in f_score:
            if f_score[node] < minimum:
                minimum = f_score[node]

        for node in f_score:
            if f_score[node] == minimum:
                current = node
                open_set.remove(current)
                del f_score[current]
                break

        if current == goal:
            reconstruct_path(start, current, came_from)
            return True

        for neighbor in current.neighbors:
            tentative_g_score = g_score[current] + 1

            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + h(neighbor, goal)

                if neighbor not in open_set:
                    open_set.add(neighbor)
                    if neighbor != goal:
                        neighbor.add_block(FOREST_GREEN)

        if current != start:
            current.add_block(GREEN)
        pygame.display.update()

    return False

    #  A* search algorithm - steps break down
    #  1. Create an open_set and add the initial node to the open_set.
    #  2. Set g_score of the initial node to zero and to infinity for all other nodes.
    #  3. Set f_score of the initial node to heuristic cost between the initial node and end node,
    #     and set f_score to infinity for all other nodes.
    #  4. Have the current node being the node with the lowest f_score and remove
    #     this node from the f_score and the open_set.
    #  5. For the current node, calculate its tentative_g_Score distances by adding one to its
    #     current g_score (since all the edges are one). Consider all of its neighbors and compare
    #     the newly calculated tentative_g_score to the assigned value and assign the smaller one.
    #     If a better path is found, store the neighbor and its current (the node that leads to
    #     neighbor) into the came_from. Add neighbor to open_set if it wasn't already in the set.
    #  6. If the current node is the destination node or if open_set is empty but goal was never
    #     reached, then stop. The algorithm has finished.
    #  7. Otherwise, go back to step 4.
