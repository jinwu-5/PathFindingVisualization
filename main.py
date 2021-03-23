import pygame
import sys

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 128, 0)
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

    def add_block(self, color):
        rect = pygame.Rect(self.row * block_size, self.col * block_size, block_size - 1, block_size - 1)
        pygame.draw.rect(WINDOW, color, rect)
        self.color = color

    def add_neighbors(self):

        """append neighbor blocks (up, down, left, right) to neighbor array"""

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


def dijkstra(start, end):
    unvisited = [node for row in grid for node in row]
    distance = {node: INFINITY for row in grid for node in row}
    path = {}
    distance[start] = 0
    current = None

    while current != end:
        minimum = INFINITY

        for node in unvisited:
            if distance[node] < minimum:
                minimum = distance[node]

        for node in unvisited:
            if distance[node] == minimum:
                current = node
                unvisited.remove(current)
                break

        if current == end:
            construct_path(path, current)
            start.add_block(PURPLE)
            return True

        for neighbor in current.neighbors:
            if neighbor.is_wall():
                alt = INFINITY + distance[current]
            else:
                alt = 1 + distance[current]
            if alt < distance[neighbor]:
                distance[neighbor] = alt
                path[neighbor] = current

        current.add_block(GREEN)
        pygame.display.update()


def construct_path(path, current):
    while current in path:
        current = path[current]
        current.add_block(BLUE)


def main():
    draw_block()
    start, end = None, None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if pygame.mouse.get_pressed()[0]:  # Left Mouse Click
                mouse_pos = pygame.mouse.get_pos()
                row, col = clicked_pos(mouse_pos)
                block = grid[row][col]
                if not start and block != end:
                    start = block
                    start.add_block(PURPLE)
                elif not end and block != start:
                    end = block
                    end.add_block(ORANGE)
                elif block != start and block != end:
                    block.add_block(GREY)

            elif pygame.mouse.get_pressed()[2]:  # Right Mouse Click
                mouse_pos = pygame.mouse.get_pos()
                row, col = clicked_pos(mouse_pos)
                block = grid[row][col]
                block.add_block(WHITE)
                if block == start:
                    start = None
                elif block == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and start and end:
                    for row in grid:
                        for block in row:
                            block.add_neighbors()

                    dijkstra(start, end)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    start = None
                    end = None
                    draw_block()

        pygame.display.update()


main()
