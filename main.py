import pygame
import sys
from constants import *
from dijkstra import dijkstra
from a_star import a_star

window_height = 660
window_width = 660

pygame.init()
win = pygame.display.set_mode((window_height, window_width))
pygame.display.set_caption("Pathfinding Visualization")

grid = []
block_size = 20
rows = window_height // block_size
cols = window_width // block_size


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
        pygame.draw.rect(win, color, rect)
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
    win.fill(BLACK)
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
                if event.key == pygame.K_a and start and goal:
                    for row in grid:
                        for block in row:
                            block.add_neighbors()
                    a_star(start, goal, grid)

                elif event.key == pygame.K_d and start and goal:
                    for row in grid:
                        for block in row:
                            block.add_neighbors()
                    dijkstra(start, goal, grid)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    start = None
                    goal = None
                    draw_block()

                elif event.key == pygame.K_w:
                    for row in grid:
                        for block in row:
                            if block.color == GREEN or block.color == GOLDEN or block.color == FOREST_GREEN:
                                block.add_block(WHITE)

        pygame.display.update()


main()
