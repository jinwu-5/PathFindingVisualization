import pygame
import sys

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GOLDEN = (255, 215, 0)
ORANGE = (255, 140, 0)
PURPLE = (128, 0, 255)
GREY = (108, 108, 108)

WINDOW_HEIGHT = 660
WINDOW_WIDTH = 660
INFINITY = float("inf")

pygame.init()
WINDOW = pygame.display.set_mode((WINDOW_HEIGHT, WINDOW_WIDTH))
pygame.display.set_caption("Pathfinding Visualization")

grid = []
block_size = 20
rows = WINDOW_WIDTH // block_size
cols = WINDOW_HEIGHT // block_size


class Block:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.color = WHITE
        self.neighbors = []

    def is_wall(self):
        return self.color == GREY

    def get_pos(self):
        return self.row, self.col

    def add_block(self, color):
        rect = pygame.Rect(self.row * block_size, self.col * block_size, block_size - 1, block_size - 1)
        pygame.draw.rect(WINDOW, color, rect)
        self.color = color

    def add_neighbors(self):

        """append neighbor blocks (up, down, left, right) to neighbor list"""

        self.neighbors = []

        if self.row > 0 and not grid[self.row - 1][self.col].is_wall():
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.row < rows - 1 and not grid[self.row + 1][self.col].is_wall():
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.col > 0 and not grid[self.row][self.col - 1].is_wall():
            self.neighbors.append(grid[self.row][self.col - 1])

        if self.col < cols - 1 and not grid[self.row][self.col + 1].is_wall():
            self.neighbors.append(grid[self.row][self.col + 1])

        return self.neighbors


def make_grid():
    for i in range(rows):
        arr = []
        for j in range(cols):
            arr.append(Block(i, j))
        grid.append(arr)


def draw_block():
    WINDOW.fill(BLACK)
    make_grid()
    for i in range(rows):
        for j in range(cols):
            block = grid[i][j]
            block.add_block(WHITE)
    pygame.display.update()


def clicked_pos(pos):
    x, y = pos

    row = x // block_size
    col = y // block_size

    return row, col


def dijkstra(start, goal):
    """
     Dijkstra's algorithm - steps break down
     1. Create a list of all the unvisited nodes called the unvisited set.
     2. Set distance of the initial node to zero and to to infinity for all other nodes.
     3. Set the initial node as current.
     4. Have the current node being the node with the shortest distance in the list of
        unvisited nodes and remove this node from the list.
     5. For the current node, consider all of its unvisited neighbours and calculate their
        tentative distances through the current node. Compare the newly calculated tentative
        distance to the current assigned value and assign the smaller one. Store the neighbour
        and its current (the node that leads to neighbor) into the came_from.
     6. If the current node is the destination node or if the smallest tentative distance
        among the nodes in the unvisited set is infinity (occurs when there is no connection
        between the initial node and remaining unvisited nodes), hen step. The algorithm has
        finished.
     7. Otherwise, go back to step 4.
    """

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


def main():
    draw_block()
    start, goal = None, None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if pygame.mouse.get_pressed()[0]:  # Left Mouse Click
                mouse_pos = pygame.mouse.get_pos()
                row, col = clicked_pos(mouse_pos)
                block = grid[row][col]
                if not start and block != goal:
                    start = block
                    start.add_block(PURPLE)
                elif not goal and block != start:
                    goal = block
                    goal.add_block(ORANGE)
                elif block != start and block != goal:
                    block.add_block(GREY)

            elif pygame.mouse.get_pressed()[2]:  # Right Mouse Click
                mouse_pos = pygame.mouse.get_pos()
                row, col = clicked_pos(mouse_pos)
                block = grid[row][col]
                block.add_block(WHITE)
                if block == start:
                    start = None
                elif block == goal:
                    goal = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d and start and goal:
                    for row in grid:
                        for block in row:
                            block.add_neighbors()

                    dijkstra(start, goal)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    start = None
                    goal = None
                    draw_block()
                elif event.key == pygame.K_w:
                    for row in grid:
                        for block in row:
                            if block.color == GREEN or block.color == GOLDEN:
                                block.add_block(WHITE)

        pygame.display.update()


main()