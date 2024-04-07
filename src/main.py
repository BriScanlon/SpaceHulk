import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Window Settings
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 640
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Hulk Game")

# Colors for drawing
BLACK = (0, 0, 0)
FLOOR_COLOR = (70, 50, 50)  # Floor tile color
GREY = (200, 200, 200)  # Grid line color

# Tile and Board Settings
TILE_SIZE = 20  # Pixel size of each tile
BOARD_SIZE = 32  # Size of the board in tiles

def can_place_tile(board, start_x, start_y, length, width, orientation):
    """
    Checks if a tile can be placed at a specified location without overlapping existing tiles
    and within the board boundaries.
    """
    # Check each cell in the proposed area for the new tile
    for i in range(start_y, min(start_y + width, BOARD_SIZE)):
        for j in range(start_x, min(start_x + length, BOARD_SIZE)):
            # If outside the board or overlaps an existing tile (1), return False
            if board[i][j] == 1:
                return False
    return True

def place_tile(board, start_x, start_y, length, width, orientation):
    """
    Places a tile on the board at the specified location.
    """
    # Ensure the placement is within the board's boundaries
    for i in range(max(0, start_y), min(BOARD_SIZE, start_y + width)):
        for j in range(max(0, start_x), min(BOARD_SIZE, start_x + length)):
            board[i][j] = 1  # Mark the tile's area as filled
            
def check_and_place_corridor(board, start_x, start_y, orientation):
    corridor_length = 4
    potential_starts = []

    # Strategy: Each entry in potential_starts includes the new orientation 
    # and the x, y coordinates where the corridor should start.

    # Check straight continuation
    if orientation == "horizontal" and can_place_tile(board, start_x + 1, start_y, corridor_length, 1, orientation):
        potential_starts.append((start_x + 1, start_y, "horizontal"))
    elif orientation == "vertical" and can_place_tile(board, start_x, start_y + 1, 1, corridor_length, orientation):
        potential_starts.append((start_x, start_y + 1, "vertical"))

    # Check right turn - Considering the board's orientation, "right" depends on the current orientation
    if orientation == "horizontal" and can_place_tile(board, start_x, start_y + 1, 1, corridor_length, "vertical"):
        potential_starts.append((start_x, start_y + 1, "vertical"))
    elif orientation == "vertical" and can_place_tile(board, start_x + 1, start_y, corridor_length, 1, "horizontal"):
        potential_starts.append((start_x + 1, start_y, "horizontal"))

    # Check left turn - This requires adjusting the start position based on the corridor length
    if orientation == "horizontal" and can_place_tile(board, start_x, start_y - corridor_length, 1, corridor_length, "vertical"):
        potential_starts.append((start_x, start_y - corridor_length + 1, "vertical"))
    elif orientation == "vertical" and can_place_tile(board, start_x - corridor_length, start_y, corridor_length, 1, "horizontal"):
        potential_starts.append((start_x - corridor_length + 1, start_y, "horizontal"))

    # Choose a potential start position randomly if available
    if potential_starts:
        new_x, new_y, new_orientation = random.choice(potential_starts)
        # Place the corridor based on the chosen orientation
        place_tile(board, new_x, new_y, corridor_length if new_orientation == "horizontal" else 1, 
                   corridor_length if new_orientation == "vertical" else 1, new_orientation)
        return (new_orientation, 
                new_x + (corridor_length if new_orientation == "horizontal" else 0), 
                new_y + (corridor_length if new_orientation == "vertical" else 0))

    # If no valid placement found, return the original orientation and positions
    return orientation, start_x, start_y

def generate_board():
    """
    Generates the game board by procedurally placing rooms and corridors. Ensures that
    corridors align with room entrances/exits and adhere to orientation changes.
    """
    board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    last_tile = "corridor"  # Start with placing a corridor
    orientation, start_x, start_y = "horizontal", 0, BOARD_SIZE // 2

    while start_x < BOARD_SIZE - 1 and start_y < BOARD_SIZE - 1:
        if last_tile == "corridor":
            # Decide on the next room size
            tile_type = random.choice(["small_room", "large_room"])
            length, width = (3, 3) if tile_type == "small_room" else (5, 5)

            # Place entrance and exit for rooms
            if orientation == "horizontal":
                place_tile(board, start_x, start_y, 1, 1, orientation)  # Entrance
                place_tile(board, start_x + length + 1, start_y, 1, 1, orientation)  # Exit
            else:  # Vertical orientation
                place_tile(board, start_x, start_y, 1, 1, orientation)  # Entrance
                place_tile(board, start_x, start_y + width + 1, 1, 1, orientation)  # Exit
            
            place_tile(board, start_x + 1, start_y, length, width, orientation)  # Room
            start_x += (length + 2) if orientation == "horizontal" else 0
            start_y += (width + 2) if orientation == "vertical" else 0
            last_tile = "room"
        else:
            # Attempt to place a corridor, checking for straight, left, or right orientations
            orientation, start_x, start_y = check_and_place_corridor(board, start_x, start_y, orientation)
            last_tile = "corridor"

    return board

def draw_board(board):
    """
    Draws the entire game board, including tiles and grid lines, to the Pygame window.
    """
    screen.fill(BLACK)
    for y, row in enumerate(board):
        for x, tile in enumerate(row):
            if tile == 1:  # Draw floor tiles
                pygame.draw.rect(screen, FLOOR_COLOR, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
    
    # Grid lines for visual separation of tiles
    for x in range(0, SCREEN_WIDTH, TILE_SIZE):
        pygame.draw.line(screen, GREY, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, TILE_SIZE):
        pygame.draw.line(screen, GREY, (0, y), (SCREEN_WIDTH, y))

def main():
    board = generate_board()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        draw_board(board)
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
