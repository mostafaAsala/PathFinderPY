import random
import pygame
from collections import deque


# Function to generate a maze using Depth-First Search (DFS)
def generate_maze(rows, cols):
    # Create a grid with all walls
    maze = [["#" for _ in range(cols)] for _ in range(rows)]

    # Function to check if a cell is within the maze borders
    def is_valid(x, y):
        return 0 <= x < rows-1 and 0 <= y < cols-1

    # Perform DFS to create the maze
    def dfs(x, y):
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        random.shuffle(directions)

        for dx, dy in directions:
            nx, ny = x + dx * 2, y + dy * 2

            if is_valid(nx, ny) and maze[nx][ny] == "#":
                maze[nx][ny] = " "
                maze[x + dx][y + dy] = " "
                dfs(nx, ny)

    # Mark entrance and exit
    entrance = random.choice([(0, i) for i in range(cols)])
    exit = random.choice([(rows - 1, i) for i in range(cols)])

    maze[entrance[0]][entrance[1]] = "E"  # Entrance
    maze[exit[0]][exit[1]] = "X"  # Exit

    # Start DFS from a random cell
    start_x, start_y = random.randrange(1, rows - 1, 2), random.randrange(1, cols - 1, 2)
    maze[start_x][start_y] = " "
    dfs(start_x, start_y)

    return maze


def print_maze(maze):
    for row in maze:
        print(' '.join(row))

# Example usage:
rows = 21
cols = 21

maze = generate_maze(rows, cols)
print_maze(maze)


# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0,255,0)
RED = (255,0,0)
YELLOW = (255,255,0)
def draw_maze(maze):
    pygame.init()

    # Set dimensions for the display
    rows = len(maze)
    cols = len(maze[0])
    cell_width = 20  # Adjust this value to change the size of cells
    width, height = cols * cell_width, rows * cell_width

    # Create the display window
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Maze')

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        screen.fill(WHITE)

        # Draw maze
        for i in range(rows):
            for j in range(cols):
                if maze[i][j] == '#':
                    pygame.draw.rect(screen, BLACK, (j * cell_width, i * cell_width, cell_width, cell_width))
                elif maze[i][j]=='E':
                    pygame.draw.rect(screen, RED, (j * cell_width, i * cell_width, cell_width, cell_width))
                elif maze[i][j]=='X':
                    pygame.draw.rect(screen, GREEN, (j * cell_width, i * cell_width, cell_width, cell_width))
                elif maze[i][j]=='.':
                    pygame.draw.rect(screen, YELLOW, (j * cell_width, i * cell_width, cell_width, cell_width))
        pygame.display.flip()
        clock.tick(60)



draw_maze(maze)


def solve_maze(maze):
    height = len(maze)
    width = len(maze[0])
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    # Find the entrance coordinates
    entrance = None
    for i in range(height):
        for j in range(width):
            if maze[i][j] == 'E':
                entrance = (i, j)
                break
        if entrance:
            break

    if not entrance:
        print("Entrance not found!")
        return []

    queue = deque([entrance])
    visited = set([entrance])
    parent = {entrance: None}
    dest = None
    while queue:
        current = queue.popleft()
        if maze[current[0]][current[1]] == 'X':
            dest = current
            break

        for dr, dc in directions:
            new_row, new_col = current[0] + dr, current[1] + dc
            
            if 0 <= new_row < height and 0 <= new_col < width and maze[new_row][new_col] != '#' and (new_row, new_col) not in visited:
                queue.append((new_row, new_col))
                visited.add((new_row, new_col))
                parent[(new_row, new_col)] = current
                print("(",(new_row, new_col),")", current)

    # Reconstruct path from exit to entrance
    out = dest  
    path =[]
    print((current[0],current[1]) , (out[0], out[1]))
    if (current[0],current[1]) == (out[0], out[1]):
        
        while current:
            path.append(current)
            current = parent[current]
        path.reverse()

    return path




path = solve_maze(maze)
solved_Map = maze
if not path:
    print("No path found.")
else:
    for row_num, row in enumerate(maze):
        for col_num, cell in enumerate(row):
            if (row_num, col_num) in path:
                print('.', end=' ')
                solved_Map[row_num][col_num]='.'
            else:
                print(cell, end=' ')
        print() 


draw_maze(solved_Map)














