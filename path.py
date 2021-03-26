import pygame
from constants import GOLDEN


def reconstruct_path(start, current, came_from):
    """
    The current node starts at end node, the goal is to traverse the end node back to the
    start node. The current node will be equal to whatever last node came from until the
    start node is reached."
    """

    while current in came_from:
        current = came_from[current]
        if current != start:
            current.add_block(GOLDEN)
        pygame.display.update()
