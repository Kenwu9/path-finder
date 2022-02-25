import pygame as p
import math
from queue import PriorityQueue

# GLOBAL
WIDTH = 800
SCREEN = p.display.set_mode((WIDTH, WIDTH))
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

class Square:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows
    
    def get_pos(self):
        return self.row, self.col
    
    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == TURQUOISE

    def reset(self):
        self.color = WHITE

    def make_start(self):
        self.color = ORANGE
    
    def make_end(self):
        self.color = TURQUOISE

    def make_barrier(self):
        self.color = BLACK

    def make_open(self):
        self.color = GREEN
    
    def make_closed(self):
        self.color = RED
    
    def make_path(self):
        self.color = PURPLE

    def draw(self, screen):
        p.draw.rect(screen, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # UP
            self.neighbors.append(grid[self.row - 1][self.col])
        
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])
 
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False

def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            square = Square(i, j, gap, rows)
            grid[i].append(square)

    return grid

    
# def draw():
#     for x in range(0, WIDTH, SIZE):
#         for y in range(0, WIDTH, SIZE):
#             rect = p.Rect(x, y, WIDTH, WIDTH)
#             p.draw.rect(screen, GREY, rect, 1) # screen, color, rect dimensions, border thickness

def draw_grid(screen, rows, width):
	gap = width // rows
	for i in range(rows):
		p.draw.line(screen, GREY, (0, i * gap), (width, i * gap))
		for j in range(rows):
			p.draw.line(screen, GREY, (j * gap, 0), (j * gap, width))

def draw(screen, grid, rows, width):
	screen.fill(WHITE)

	for row in grid:
		for square in row:
			square.draw(screen)

	draw_grid(screen, rows, width)
	p.display.update()

def draw_path(came_from, current, draw):
	while current in came_from:
		current = came_from[current]
		current.make_path()
		draw()

def h(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    return abs(x2 - x1) + abs(y2 - y1)


def algorithm(draw, grid, start_sq, end_sq):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start_sq))
    came_from = {}
    g_score = {square: float("inf") for row in grid for square in row}
    g_score[start_sq] = 0
    f_score = {square: float("inf") for row in grid for square in row}
    f_score[start_sq] = h(start_sq.get_pos(), end_sq.get_pos())

    open_set_hash = {start_sq}

    while not open_set.empty():
        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()
        
        current = open_set.get()[2] # this action both retreives and removes an item from the queue
        open_set_hash.remove(current)

        if current == end_sq:
            draw_path(came_from, end_sq, draw) ##########TODO
            end_sq.make_end()
            return True
        
        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end_sq.get_pos())

                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()
        
        draw()

        if current != start_sq:
            current.make_closed()

    return False

  
def get_clicked_pos(pos, rows, width):
	gap = width // rows
	y, x = pos

	row = y // gap
	col = x // gap

	return row, col      

def main(screen, width): 
    ROWS = 50
    SIZE = WIDTH // ROWS
    
    grid = make_grid(ROWS, width)

    start = False
    start_pos = None
    start_sq = None

    end = False
    end_pos = None
    end_sq = None

    started = False
    running = True
    p.init()
    screen.fill(WHITE)

    while running:
        draw(screen, grid, ROWS, WIDTH)
        for event in p.event.get():
            if event.type == p.QUIT:
                running = False
            
            if p.mouse.get_pressed()[0]: # LEFT
                pos = p.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                square = grid[row][col]
                if not start and square != end:
                    start_sq = square
                    start_sq.make_start()
                    start = True
                
                elif not end and square != start_sq:
                    end_sq = square
                    end_sq.make_end()
                    end = True
                
                elif square != start_sq and square != end_sq:
                    square.make_barrier()
    
            # elif start and end and p.mouse.get_pressed()[0]: #left click
            #     pos = p.mouse.get_pos()
            #     sq_pos = pos[0] // SIZE, pos[1] // SIZE
            #     if sq_pos != start_pos and sq_pos != end_pos:
            #         rect = p.Rect(sq_pos[0]*SIZE, sq_pos[1]*SIZE, 
            #                         SIZE, SIZE)
            #         p.draw.rect(screen, BLACK, rect)
            
            elif p.mouse.get_pressed()[2]: # right click
                pos = p.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                square = grid[row][col]
                if square == start_pos:
                    start = False
                    start_pos = None
                    start_sq = None
                elif square == end_pos:
                    end = False
                    start_pos = None
                    start_sq = None
            
            elif event.type == p.KEYDOWN: # for pressing 'space' to start path finder, or for pressing 'c' to clear the board
                if event.key == p.K_SPACE and start and end:
                    for row in grid:
                        for square in row:
                            square.update_neighbors(grid)
                    algorithm(lambda: draw(screen, grid, ROWS, width), grid, start_sq, end_sq) #TO BE WRITTTEN


                if event.key == p.K_c:
                    start = False
                    start_pos = None
                    start_sq = None
                    end = False
                    end_pos = None
                    end_sq = None

                    grid = make_grid(ROWS, width)
    p.quit()

if __name__ == "__main__":
    main(SCREEN, WIDTH)