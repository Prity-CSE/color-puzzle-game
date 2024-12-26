import pygame
import random
import time

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 400

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (169, 169, 169)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
CYAN = (0, 255, 255)

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Memory Puzzle")

# Clock for controlling game speed
clock = pygame.time.Clock()

# Font styles
font = pygame.font.SysFont("comicsansms", 32)

# Tile settings
TILE_SIZE = 100
TILE_GAP = 10

# Colors for the tiles
TILE_COLORS = [RED, GREEN, BLUE, YELLOW, PURPLE, CYAN]

# Grid settings
GRID_COLS = 4
GRID_ROWS = 3
GRID_WIDTH = GRID_COLS * TILE_SIZE + (GRID_COLS - 1) * TILE_GAP
GRID_HEIGHT = GRID_ROWS * TILE_SIZE + (GRID_ROWS - 1) * TILE_GAP

# Center grid
GRID_X = (WIDTH - GRID_WIDTH) // 2
GRID_Y = (HEIGHT - GRID_HEIGHT) // 2


# Function to generate shuffled pairs of colors
def generate_tiles(rows, cols):
    num_tiles = rows * cols
    colors = TILE_COLORS * (num_tiles // len(TILE_COLORS)) + TILE_COLORS[:num_tiles % len(TILE_COLORS)]
    random.shuffle(colors)
    return [colors[i:i + cols] for i in range(0, len(colors), cols)]


# Function to draw a tile
def draw_tile(x, y, color, visible):
    if visible:
        pygame.draw.rect(screen, color, (x, y, TILE_SIZE, TILE_SIZE))
    else:
        pygame.draw.rect(screen, GRAY, (x, y, TILE_SIZE, TILE_SIZE))
    pygame.draw.rect(screen, BLACK, (x, y, TILE_SIZE, TILE_SIZE), 2)


# Function to get tile position from mouse coordinates
def get_tile_pos(x, y):
    col = (x - GRID_X) // (TILE_SIZE + TILE_GAP)
    row = (y - GRID_Y) // (TILE_SIZE + TILE_GAP)
    if 0 <= col < GRID_COLS and 0 <= row < GRID_ROWS:
        return row, col
    return None, None


def memory_puzzle():
    tiles = generate_tiles(GRID_ROWS, GRID_COLS)
    visible_tiles = [[False for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]
    first_tile = None
    matched_tiles = 0
    game_over = False

    while not game_over:
        screen.fill(WHITE)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not first_tile:
                    row, col = get_tile_pos(event.pos[0], event.pos[1])
                    if row is not None and not visible_tiles[row][col]:
                        visible_tiles[row][col] = True
                        first_tile = (row, col)
                else:
                    row, col = get_tile_pos(event.pos[0], event.pos[1])
                    if row is not None and not visible_tiles[row][col]:
                        visible_tiles[row][col] = True
                        pygame.display.update()
                        time.sleep(0.5)
                        if tiles[row][col] == tiles[first_tile[0]][first_tile[1]]:
                            matched_tiles += 2
                        else:
                            visible_tiles[row][col] = False
                            visible_tiles[first_tile[0]][first_tile[1]] = False
                        first_tile = None

        # Draw all tiles
        for r in range(GRID_ROWS):
            for c in range(GRID_COLS):
                x = GRID_X + c * (TILE_SIZE + TILE_GAP)
                y = GRID_Y + r * (TILE_SIZE + TILE_GAP)
                draw_tile(x, y, tiles[r][c], visible_tiles[r][c])

        # Check for game over
        if matched_tiles == GRID_ROWS * GRID_COLS:
            game_over = True
            screen.fill(WHITE)
            message = font.render("You Win!", True, GREEN)
            screen.blit(message, (WIDTH // 2 - message.get_width() // 2, HEIGHT // 2 - message.get_height() // 2))
            pygame.display.update()
            time.sleep(3)

        pygame.display.update()
        clock.tick(30)


if __name__ == "__main__":
    memory_puzzle()
