import pygame
import sys

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 128, 0)
PURPLE = (128, 0, 255)
GREY = (143, 143, 143)

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

    def draw_block(self):
        rect = pygame.Rect(self.row * block_size, self.col * block_size, block_size, block_size)
        pygame.draw.rect(WINDOW, WHITE, rect)


def make_grid():
    for i in range(rows):
        arr = []
        for j in range(cols):
            arr.append(Block(i, j))
        grid.append(arr)


def draw_grid():
    for i in range(rows):
        pygame.draw.line(WINDOW, GREY, (0, i * block_size), (WINDOW_WIDTH, i * block_size))  # draw horizontal lines
        for j in range(cols):
            pygame.draw.line(WINDOW, GREY, (j * block_size, 0), (j * block_size, WINDOW_HEIGHT))  # draw vertical lines


def draw_block():
    WINDOW.fill(BLACK)
    make_grid()
    for i in range(rows):
        for j in range(cols):
            block = grid[i][j]
            block.draw_block()
    draw_grid()
    pygame.display.update()


def main():
    draw_block()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


main()
