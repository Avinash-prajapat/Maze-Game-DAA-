import pygame
import random
import heapq
import time

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 600
TILE_SIZE = 20  # Each block size
cols, rows = WIDTH // TILE_SIZE, HEIGHT // TILE_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Pygame setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Game")

# Maze Generation using Recursive Backtracking
def generate_maze(cols, rows):
    maze = [['#'] * cols for _ in range(rows)]

    def carve(x, y):
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        random.shuffle(directions)

        for dx, dy in directions:
            nx, ny = x + 2 * dx, y + 2 * dy
            if 0 <= nx < cols and 0 <= ny < rows and maze[ny][nx] == '#':
                maze[y + dy][x + dx] = ' '
                maze[ny][nx] = ' '
                carve(nx, ny)

    maze[1][1] = ' '  # Start point
    carve(1, 1)
    return maze

maze = generate_maze(cols, rows)

# A* Algorithm for Pathfinding
def a_star(maze, start, end):
    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == end:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            return path[::-1]

        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            neighbor = (current[0] + dx, current[1] + dy)
            if 0 <= neighbor[0] < cols and 0 <= neighbor[1] < rows and maze[neighbor[1]][neighbor[0]] != '#':
                temp_g_score = g_score[current] + 1
                if temp_g_score < g_score.get(neighbor, float('inf')):
                    came_from[neighbor] = current
                    g_score[neighbor] = temp_g_score
                    heapq.heappush(open_set, (temp_g_score + heuristic(neighbor, end), neighbor))
    return []

# Draw Maze on the Screen
def draw_maze(maze):
    for y in range(rows):
        for x in range(cols):
            color = WHITE if maze[y][x] == ' ' else BLACK
            pygame.draw.rect(screen, color, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

# Game Loop
def game_loop():
    clock = pygame.time.Clock()
    start = (1, 1)
    end = (cols - 2, rows - 2)
    path = a_star(maze, start, end)  # Get the optimal path

    running = True
    player_pos = list(start)

    while running:
        screen.fill(BLACK)
        draw_maze(maze)

        # Draw the path found by A* (optional, can be removed)
        for (x, y) in path:
            pygame.draw.rect(screen, GREEN, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

        # Draw player and goal
        pygame.draw.rect(screen, RED, (player_pos[0] * TILE_SIZE, player_pos[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE))
        pygame.draw.rect(screen, GREEN, (end[0] * TILE_SIZE, end[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Handle player movement
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and maze[player_pos[1] - 1][player_pos[0]] == ' ':
                    player_pos[1] -= 1
                elif event.key == pygame.K_DOWN and maze[player_pos[1] + 1][player_pos[0]] == ' ':
                    player_pos[1] += 1
                elif event.key == pygame.K_LEFT and maze[player_pos[1]][player_pos[0] - 1] == ' ':
                    player_pos[0] -= 1
                elif event.key == pygame.K_RIGHT and maze[player_pos[1]][player_pos[0] + 1] == ' ':
                    player_pos[0] += 1

        # Check if player reached the goal
        if tuple(player_pos) == end:
            print("You reached the goal!")
            running = False

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

# Run the game
if __name__ == "__main__":
    game_loop()
