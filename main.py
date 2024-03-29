from tkinter import messagebox, Tk
import pygame
import sys

window_width = 500
window_height = 500
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Dijkstra's algorithm")

rows = 25
columns = 25

box_width = window_width/columns
box_heigth = window_height/rows

grid = []
queue = []
path = []

class Box:
    def __init__(self, i, j) -> None:
        self.x = i
        self.y = j
        self.start = False
        self.wall = False
        self.target = False
        self.queued = False
        self.visited = False
        self.neighbours = []
        self.prior = None
    def draw(self, win, color):
        pygame.draw.rect(win, color, (self.x * box_width, self.y * box_heigth, box_width - 2, box_heigth - 2))
    def set_neighbours(self):
        if self.x > 0:
            self.neighbours.append(grid[self.x - 1][self.y])
        if self.x < columns - 1:
            self.neighbours.append(grid[self.x + 1][self.y])
        if self.y > 0:
            self.neighbours.append(grid[self.x][self.y - 1])
        if self.y < rows - 1:
            self.neighbours.append(grid[self.x][self.y + 1])

#create grid
for i in range(columns):
    arr = []
    for j in range(rows):
        arr.append(Box(i,j))
    grid.append(arr)

#set neighbours
for i in range(columns):
    for j in range(rows):
        grid[i][j].set_neighbours()

start_box = grid[0][0]
start_box.start = True
start_box.visited = True
queue.append(start_box)

def main():
    begin_search = False
    target_box_set = False
    searching = True
    target_box = None
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEMOTION: #mouse controls
                x = pygame.mouse.get_pos()[0]
                y = pygame.mouse.get_pos()[1]
                i = int(x // box_width)
                j = int(y // box_heigth)
                if event.buttons[0]: #draw wall when left clicked
                    grid[i][j].wall = True
                if event.buttons[2] and not target_box_set: #draw target box when right clicked and there hasn't been a target already
                    target_box = grid[i][j]
                    target_box.target = True
                    target_box_set = True
            if event.type == pygame.KEYDOWN and target_box_set: #start algorithm
                begin_search = True
        if begin_search:
            if len(queue) > 0 and searching:
                current_box = queue.pop(0)
                current_box.visited = True
                if current_box == target_box:
                    searching = False
                    while current_box.prior != start_box:
                        path.append(current_box.prior)
                        current_box = current_box.prior
                else:
                    for neighbour in current_box.neighbours: #iterate over all neighbours and append the ones that aren't a wall
                        if not neighbour.queued and not neighbour.wall:
                            neighbour.queued = True
                            neighbour.prior = current_box
                            queue.append(neighbour)
            else:
                if searching:
                    Tk().wm_withdraw()
                    messagebox.showinfo("No solution", "There's no solution for this problem")
                    searching = False
                
        window.fill((0, 0, 0)) #this is RGB[A]
        for i in range(columns):
            for j in range(rows):
                box = grid[i][j]
                box.draw(window, (60,60,60))
                if box.queued:
                    box.draw(window, (200,0,0))
                if box.visited:
                    box.draw(window, (0, 200, 0))
                if box in path:
                    box.draw(window, (0, 0, 200))
                if box.start:
                    box.draw(window, (0,200,200))
                if box.wall:
                    box.draw(window, (255,255,255))
                if box.target:
                    box.draw(window, (200,200,0))

        pygame.display.flip()


if __name__ == "__main__":
    main()