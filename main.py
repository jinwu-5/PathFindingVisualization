import pygame
import sys

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 128, 0)
PURPLE = (128, 0, 255)
GREY = (114, 114, 114)

WINDOW_HEIGHT = 800
WINDOW_WIDTH = 800

pygame.init()
WINDOW = pygame.display.set_mode((WINDOW_HEIGHT, WINDOW_WIDTH))
pygame.display.set_caption("Pathfinding Visualization")

grid = []
block_size = 16
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

    def get_color(self):
        return self.color

    def make_block(self, color):
        rect = pygame.Rect(self.row * block_size, self.col * block_size, block_size - 1, block_size - 1)
        pygame.draw.rect(WINDOW, color, rect)
        self.color = color

    def update_neighbors(self):
        self.neighbors = []
        if self.row < rows - 1 and not grid[self.row + 1][self.col].is_wall():
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_wall():
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < cols - 1 and not grid[self.row][self.col + 1].is_wall():
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_wall():
            self.neighbors.append(grid[self.row][self.col - 1])

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
            block.make_block(WHITE)
    pygame.display.update()


def clicked_pos(pos):
    x, y = pos

    row = x // block_size
    col = y // block_size

    return row, col


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
                    start.make_block(PURPLE)
                elif not end and block != start:
                    end = block
                    end.make_block(ORANGE)
                elif block != start and block != end:
                    block.make_block(GREY)

            elif pygame.mouse.get_pressed()[2]:  # Right Mouse Click
                mouse_pos = pygame.mouse.get_pos()
                row, col = clicked_pos(mouse_pos)
                block = grid[row][col]
                block.make_block(WHITE)
                if block == start:
                    start = None
                elif block == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for block in row:
                            block.update_neighbors()

        pygame.display.update()


main()
