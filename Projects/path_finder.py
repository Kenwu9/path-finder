import pygame as p
import math
from queue import PriorityQueue

# GLOBAL
WIDTH = 800
ROWS = 50
SIZE = WIDTH // ROWS
screen = p.display.set_mode((WIDTH, WIDTH))
p.display.set_caption("pathfinder.io")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

class square:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows


    def is_barrier(self, color):
        if color == BLACK:
            return True
        return False

    def grid(row, col, width):
        pass

    # def update_neighbors(self, grid):
	#     self.neighbors = []
    #     if self.row < ROWS - 1 and not grid[self.row + 1][self.col].is_barrier(): # DOWN
	#         self.neighbors.append(grid[self.row + 1][self.col])

	#     if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # UP
	#         self.neighbors.append(grid[self.row - 1][self.col])

	#     if self.col < ROWS - 1 and not grid[self.row][self.col + 1].is_barrier(): # RIGHT
	#         self.neighbors.append(grid[self.row][self.col + 1])

	#     if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # LEFT
	#         self.neighbors.append(grid[self.row][self.col - 1])

# def make_grid(rows, width):
# # from astar.py. need to change
# 	grid = []
# 	gap = width // rows
# 	for i in range(rows):
# 		grid.append([])
# 		for j in range(rows):
# 			spot = Spot(i, j, gap, rows)
# 			grid[i].append(spot)

def draw():
    for x in range(0, WIDTH, SIZE):
        for y in range(0, WIDTH, SIZE):
            rect = p.Rect(x, y, WIDTH, WIDTH)
            p.draw.rect(screen, GREY, rect, 1) # screen, color, rect dimensions, border thickness

def makepos(sq_pos, color):
    rect = p.Rect(sq_pos[0]*SIZE, sq_pos[1]*SIZE, SIZE, SIZE)
    p.draw.rect(screen, color, rect)



def main(): 
    start = False
    sq_pos1 = None
    end = False
    sq_pos2 = None
    started = False
    running = True
    p.init()
    screen.fill(WHITE)

    while running:
        draw()
        for event in p.event.get():
            if event.type == p.QUIT:
                running = False
            
            if event.type == p.MOUSEBUTTONDOWN:
                if event.button == 1: #left click
                    if not start:
                        start_pos = p.mouse.get_pos()
                        sq_pos1 = start_pos[0] // SIZE, start_pos[1] // SIZE
                        color = GREEN
                        makepos(sq_pos1, color)
                        start = True
                    if start and not end:
                        end_pos = p.mouse.get_pos()
                        sq_pos2 = end_pos[0] // SIZE, end_pos[1] // SIZE
                        if sq_pos1 != sq_pos2:
                            color = ORANGE
                            makepos(sq_pos2, color)
                            end = True
    
            elif start and end and p.mouse.get_pressed()[0]: #left click
                pos = p.mouse.get_pos()
                sq_pos = pos[0] // SIZE, pos[1] // SIZE
                if sq_pos != sq_pos1 and sq_pos != sq_pos2:
                    rect = p.Rect(sq_pos[0]*SIZE, sq_pos[1]*SIZE, 
                                    SIZE, SIZE)
                    p.draw.rect(screen, BLACK, rect)
            
            elif p.mouse.get_pressed()[2]: # right click
                pos = p.mouse.get_pos()
                sq_pos = pos[0] // SIZE, pos[1] // SIZE
                rect = p.Rect(sq_pos[0]*SIZE, sq_pos[1]*SIZE, 
                                SIZE, SIZE)
                p.draw.rect(screen, WHITE, rect)
                if sq_pos == sq_pos1:
                    start = False
                elif sq_pos == sq_pos2:
                    end = False
            
            elif event.type == p.KEYDOWN: # for pressing 'space' to start path finder, or for pressing 'c' to clear the board
                if event.key == p.K_SPACE:
                    pass
                if event.key == p.K_c:
                    pass
                    

        p.display.update()
    p.quit()

if __name__ == "__main__":
    main()