import pygame
from collections import deque
import random
import sys
from tkinter import filedialog

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

def expand_path(maze, space_width=0):
    if space_width==0:return maze
    height = len(maze)
    width = len(maze[0])

    new_width = width * (space_width + 1)
    new_height = height * (space_width + 1)

    def is_valid(row, col):
        return 0 <= row < height and 0 <= col < width

    new_maze = [[' ' for _ in range(new_width)] for _ in range(new_height)]

    for i in range(height):
        for j in range(width):
            new_maze[i * (space_width + 1)][j * (space_width + 1)] = maze[i][j]
    
    for i in range(new_height):
        for j in range(new_width):
            if new_maze[i][j] == '#' or new_maze[i][j] == 'E' or new_maze[i][j] == 'X' :
                if j+space_width+1<new_width:
                    if j+space_width+1<new_width and new_maze[i][j+space_width+1]=='#' or new_maze[i][j+space_width+1]=='E' or new_maze[i][j+space_width+1]=='X':
                        for k in range(space_width):
                            new_maze[i][j+k+1]='#'
                if i+space_width+1<new_height:
                    if i+space_width+1<new_height and new_maze[i+space_width+1][j]=='#' or new_maze[i+space_width+1][j]=='E' or new_maze[i+space_width+1][j]=='X':
                        for k in range(space_width):
                            new_maze[i+k+1][j]='#'

    return new_maze

# Maze dimensions


rows = 21
cols = 21
expand_map = 1
mainBlockSize=30
block_size = 30

block_size = mainBlockSize/(expand_map+1)
wait_period = 1
# Pygame setup
pygame.init()
screen_width = cols * block_size
screen_height = rows * block_size
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Maze Solver')
clock = pygame.time.Clock()

# Colors

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255,255,0)
PURBLE = (255,0,255)
GRAY = (180, 180, 180)

# Find entrance coordinates
entrance = None

exit_point = None



def draw_maze():
    
    for row_num, row in enumerate(maze):
        for col_num, cell in enumerate(row):
            if cell == '#':
                pygame.draw.rect(screen, BLACK, (col_num * block_size, row_num * block_size, block_size, block_size))
            elif cell == 'E':
                pygame.draw.rect(screen, GREEN, (col_num * block_size, row_num * block_size, block_size, block_size))
            elif cell == ' ':
                pygame.draw.rect(screen, WHITE, (col_num * block_size, row_num * block_size, block_size, block_size))
            elif cell == 'X':
                pygame.draw.rect(screen, RED, (col_num * block_size, row_num * block_size, block_size, block_size))
            elif cell == '.':
                pygame.draw.rect(screen, BLUE, (col_num * block_size, row_num * block_size, block_size, block_size))
            elif cell == 'V':
                pygame.draw.rect(screen, YELLOW, (col_num * block_size, row_num * block_size, block_size, block_size))
            elif cell == 'P':
                pygame.draw.rect(screen, PURBLE, (col_num * block_size, row_num * block_size, block_size, block_size))

def solve_mazeBFS(maze):
    height = len(maze)
    width = len(maze[0])
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    solved = False
    queue = deque([entrance])
    visited = set([entrance])
    parent = {entrance: None}
    reach = None
    while queue:
        current = queue.popleft()
        if maze[current[0]][current[1]] == 'X':
            reach=current
            solved = True
            break

        for dr, dc in directions:
            new_row, new_col = current[0] + dr, current[1] + dc
            if 0 <= new_row < height and 0 <= new_col < width and maze[new_row][new_col] != '#' and (new_row, new_col) not in visited:
                queue.append((new_row, new_col))
                visited.add((new_row, new_col))
                parent[(new_row, new_col)] = current

                # Pygame visualization - coloring visited cells
                draw_maze()
                for row_num, row in enumerate(maze):
                    for col_num, cell in enumerate(row):
                        if (row_num, col_num) in visited and maze[row_num][col_num]!='E'and maze[row_num][col_num]!='X':
                            maze[row_num][col_num]!='V'
                            pygame.draw.rect(screen, YELLOW, (col_num * block_size, row_num * block_size, block_size, block_size))
                pygame.display.update()
                pygame.time.wait(wait_period)

    # Reconstruct path from exit to entrance
    path = []
    if reach== current:
        while current:
            path.append(current)
            
            maze[current[0]][current[1]]='.'
            current = parent[current]
        path.reverse()
    draw_maze()
    return solved, path

def solve_maze_DFS(maze):
    height = len(maze)
    width = len(maze[0])
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    
    def dfs(row, col, path):
        if maze[row][col] == 'X':
            return True, path

        maze[row][col] = 'V'
        path.append((row, col))
        draw_maze()
        pygame.display.update()
        pygame.time.wait(wait_period)

        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < height and 0 <= new_col < width and maze[new_row][new_col] != '#' and maze[new_row][new_col] != 'V':
                found, new_path = dfs(new_row, new_col, path)
                if found:
                    return True, new_path

        path.pop()
        return False, path

    return dfs(entrance[0], entrance[1], [])

def solve_mazeGreedy(maze):
    def manhattan_distance(point1, point2):
        return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])

    def solve_maze_GBFS_mh(maze):
        height = len(maze)
        width = len(maze[0])
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        def is_valid(row, col):
            return 0 <= row < height and 0 <= col < width and maze[row][col] != '#' and maze[row][col] != 'V'
        
        queue = [(manhattan_distance(entrance, exit_point), entrance)]
        maze[entrance[0]][entrance[1]] = 'E'
        parent = {}
        while queue:
            queue.sort(reverse=True)
            _, current = queue.pop()
            draw_maze()
            pygame.display.update()
            pygame.time.wait(wait_period)
            if current == exit_point:
                path = []
                while current != entrance:
                    path.append(current)
                    current = parent[current]
                path.append(entrance)
                return True, path[::-1]
            
            maze[current[0]][current[1]] = 'V'

            for dr, dc in directions:
                new_row, new_col = current[0] + dr, current[1] + dc
                if is_valid(new_row, new_col):
                    if maze[new_row][new_col] != 'V' and maze[new_row][new_col] != '.':
                        parent[(new_row, new_col)] = current
                        queue.append((manhattan_distance((new_row, new_col), exit_point), (new_row, new_col)))
                        maze[new_row][new_col] = '.'
        return False, []

    maze[entrance[0]][entrance[1]] = 'E'
    maze[exit_point[0]][exit_point[1]] = 'X'
    return solve_maze_GBFS_mh(maze)

def solve_mazeAS(maze):
    def manhattan_distance(point1, point2):
        return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])

    def solve_maze_A_star(maze):
        height = len(maze)
        width = len(maze[0])
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        def is_valid(row, col):
            return 0 <= row < height and 0 <= col < width and maze[row][col] != '#' and maze[row][col] != 'V'

        g_costs = {entrance: 0}
        f_costs = {entrance: manhattan_distance(entrance, exit_point)}
        parent = {}
        open_set = {entrance}

        while open_set:
            current = min(open_set, key=lambda x: f_costs[x])

            if current == exit_point:
                path = []
                while current in parent:
                    path.append(current)
                    current = parent[current]
                path.append(entrance)
                return True, path[::-1]

            open_set.remove(current)
            maze[current[0]][current[1]] = 'V'
            draw_maze()
            pygame.display.update()
            pygame.time.wait(wait_period)
            
            for dr, dc in directions:
                new_row, new_col = current[0] + dr, current[1] + dc
                if is_valid(new_row, new_col):
                    tentative_g_cost = g_costs[current] + 1
                    if (new_row, new_col) not in g_costs or tentative_g_cost < g_costs[(new_row, new_col)]:
                        parent[(new_row, new_col)] = current
                        g_costs[(new_row, new_col)] = tentative_g_cost
                        f_costs[(new_row, new_col)] = tentative_g_cost + manhattan_distance((new_row, new_col), exit_point)
                        if (new_row, new_col) not in open_set:
                            open_set.add((new_row, new_col))
                            maze[new_row][new_col] = '.'

        return False, []
    
    maze[entrance[0]][entrance[1]] = 'E'
    maze[exit_point[0]][exit_point[1]] = 'X'
    return solve_maze_A_star(maze)
# Main loop

# Create the screen

def clearMap(maze):
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j]!='#':
                maze[i][j]=' '
    maze[entrance[0]][entrance[1]]='E'
    maze[exit_point[0]][exit_point[1]]='X'
# Font setup
font = pygame.font.SysFont(None, 20)

# Buttons
Load_button = pygame.Rect(25, 0, 100, 25)
maze_button = pygame.Rect(25, 25, 100, 25)
increaseSpace_button = pygame.Rect(125, 25, 25, 25)
Space_button = pygame.Rect(150, 25, 25, 25)
DecreaseSpace_button = pygame.Rect(175, 25, 25, 25)
bfs_button = pygame.Rect(25, 75, 100, 25)
dfs_button = pygame.Rect(25, 125, 100, 25)
greedy_button = pygame.Rect(25, 175, 100, 25)
a_star_button = pygame.Rect(25, 225, 100, 25)

# Texts
maze_text = font.render('Create Maze', True, BLACK)
Load_text = font.render('Load Maze', True, BLACK)
increaseSpace_text = font.render('+', True, BLACK)
Space_text = font.render(str(expand_map), True, BLACK)
DecreaseSpace_text = font.render('-', True, BLACK)
bfs_text = font.render('BFS', True, BLACK)
dfs_text = font.render('DFS', True, BLACK)
greedy_text = font.render('Greedy', True, BLACK)
a_star_text = font.render('A*', True, BLACK)

maze_drawn = False
running = True

solved =False
solved_path=[] 


step = 0
while running:
    screen.fill(WHITE)
    if maze_drawn:
            draw_maze()
    # Draw buttons
    pygame.draw.rect(screen, GRAY, maze_button)
    pygame.draw.rect(screen, GRAY, Load_button)
    pygame.draw.rect(screen, GRAY, increaseSpace_button)
    pygame.draw.rect(screen, GRAY, Space_button)
    pygame.draw.rect(screen, GRAY, DecreaseSpace_button)
    pygame.draw.rect(screen, GRAY, bfs_button)
    pygame.draw.rect(screen, GRAY, dfs_button)
    pygame.draw.rect(screen, GRAY, greedy_button)
    pygame.draw.rect(screen, GRAY, a_star_button)

    # Draw texts
    screen.blit(maze_text, (maze_button.x + 20, maze_button.y + 10))
    screen.blit(Load_text, (Load_button.x + 20, Load_button.y + 10))
    screen.blit(increaseSpace_text, (increaseSpace_button.x + 20, increaseSpace_button.y + 10))
    screen.blit(Space_text, (Space_button.x + 20, Space_button.y + 10))
    screen.blit(DecreaseSpace_text, (DecreaseSpace_button.x + 20, DecreaseSpace_button.y + 10))
    screen.blit(bfs_text, (bfs_button.x + 20, bfs_button.y + 10))
    screen.blit(dfs_text, (dfs_button.x + 20, dfs_button.y + 10))
    screen.blit(greedy_text, (greedy_button.x + 20, greedy_button.y + 10))
    screen.blit(a_star_text, (a_star_button.x + 20, a_star_button.y + 10))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if maze_button.collidepoint(mouse_pos):
                maze = generate_maze(rows, cols)
                maze = expand_path(maze,expand_map)
                                
                for row in maze:
                    print(''.join(row))
                print("--------------------------------------------")
            
                for i in range(len(maze)):
                    for j in range(len(maze[0])):
                        if maze[i][j] == 'E':
                            entrance = (i, j)
                        elif maze[i][j] == 'X':
                            exit_point = (i, j)

                if not (entrance and exit_point):
                    print("Entrance not found!")
                    pygame.quit()
                    exit()
                maze_drawn =True  
                                
                screen_width = len(maze) * block_size
                screen_height = len(maze[0]) * block_size        
                screen = pygame.display.set_mode((screen_width, screen_height))
                draw_maze()
                pygame.display.update()
                
            elif Load_button.collidepoint(mouse_pos):
                path = filedialog.askopenfilename()
                if path!="":
                    
                    # Load the maze image
                    maze_image = pygame.image.load(path)
                    # Get the dimensions of the maze image
                    width, height = maze_image.get_size()

                    # Convert image to grayscale function
                    def convert_to_grayscale(image):
                        for y in range(height):
                            for x in range(width):
                                color = image.get_at((x, y))
                                grayscale = sum(color[:3]) // 3  # Calculate average RGB value for grayscale
                                image.set_at((x, y), (grayscale, grayscale, grayscale))  # Set grayscale color
                        return image
                    
                    # Convert maze image to grayscale
                    #maze_image = convert_to_grayscale(maze_image)

                    # Set the lowest resolution (adjust as needed)
                    lowest_resolution = (50, 50)  # Change the values to your desired resolution

                    # Downscale the image
                    maze_image = pygame.transform.scale(maze_image, lowest_resolution)
                    width, height = maze_image.get_size()
                    
                    # Set up the maze grid
                    maze = [['' for _ in range(width)] for _ in range(height)]

                    # Function to convert RGB values to maze elements
                    def convert_color_to_maze(color):
                        # Define colors for walls and paths (adjust these based on your image)
                        
                        # Check if the color matches a wall or a path
                        if color ==(255,255,255):
                            return ' '
                        else:
                            return '#'  # Adjust this to handle other colors if needed

                    # Convert the image to maze representation
                    for y in range(height):
                        for x in range(width):
                            color = maze_image.get_at((x, y))[:3]  # Get RGB values
                            
                            maze[y][x] = convert_color_to_maze(color)

                    # Example: Print the maze representation
                    for row in maze:
                        print(''.join(row))
                    
                    
                    # Example: Draw the maze on a Pygame window
                    screen = pygame.display.set_mode((width*block_size, height*block_size))
                    maze[0][1] = 'E'
                    maze[-1][-2] = 'X'
                    entrance = (0,1)
                    exit_point=(len(maze)-1 ,len(maze[0])-2  )
                    maze_drawn =True
                    draw_maze()
                    pygame.display.update()

                pass
            elif bfs_button.collidepoint(mouse_pos):
                clearMap(maze)
                original_Maze = maze
                solved , solved_path = solve_mazeBFS(original_Maze)
                # Logic for BFS algorithm
                pass
            elif dfs_button.collidepoint(mouse_pos):
                clearMap(maze)
                original_Maze = maze
                solved , solved_path = solve_maze_DFS(original_Maze)
                # Logic for DFS algorithm
                pass
            elif greedy_button.collidepoint(mouse_pos):
                clearMap(maze)
                original_Maze = maze
                solved , solved_path = solve_mazeGreedy(original_Maze)
                # Logic for Greedy algorithm
                pass
            elif a_star_button.collidepoint(mouse_pos):
                clearMap(maze)
                original_Maze = maze
                solved , solved_path = solve_mazeAS(original_Maze)
                # Logic for A* algorithm
                pass
            elif increaseSpace_button.collidepoint(mouse_pos):
                
                expand_map += 1
                block_size = mainBlockSize/(expand_map+1)
                expand_map = 10 if expand_map>10 else expand_map
                Space_text = font.render(str(expand_map), True, BLACK)
                pass
           
            elif DecreaseSpace_button.collidepoint(mouse_pos):
                expand_map -= 1
                block_size = mainBlockSize/(expand_map+1)
                expand_map = 0 if expand_map<0 else expand_map
                Space_text = font.render(str(expand_map), True, BLACK)
                pass
    if solved==True:
        if step < len(solved_path):
            row, col = solved_path[step]
            maze[row][col] = 'P'
            draw_maze()
            pygame.draw.rect(screen, WHITE, (col * block_size, row * block_size, block_size, block_size))
            pygame.display.update()
            step += 1
            pygame.time.wait(wait_period)
            if (row,col)==exit_point:
                solved = False
                step=0
                print("solved")
        else:
            solved = False
            step=0
            print("solved")

    pygame.display.update()
    clock.tick(60)

pygame.quit()
