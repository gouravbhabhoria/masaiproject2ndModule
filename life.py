
import argparse
import sys
import random
import pygame

def parse_args():
    """Parse command-line arguments for width, height, and FPS."""
    parser = argparse.ArgumentParser(description="Conway's Game of Life")
    parser.add_argument('--width', type=int, default=50, help='Width of the board (number of cells)')
    parser.add_argument('--height', type=int, default=30, help='Height of the board (number of cells)')
    parser.add_argument('--fps', type=int, default=10, help='Frames per second for the simulation')
    return parser.parse_args()

def next_gen(live_cells, width, height):
    """
    Compute the next generation of live cells without mutating the original set.
    Uses Conway's Game of Life rules:
      - Any live cell with two or three live neighbours survives.
      - Any dead cell with exactly three live neighbours becomes a live cell.
      - All other live cells die in the next generation. Similarly, all other dead cells stay dead.
    """
    new_live = set()
    neighbor_counts = {}

    # Count neighbors for each live cell and its neighbors
    for (x, y) in live_cells:
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                # Only consider neighbors within the board bounds
                if 0 <= nx < width and 0 <= ny < height:
                    neighbor_counts[(nx, ny)] = neighbor_counts.get((nx, ny), 0) + 1

    # Apply the rules to determine which cells live in the next generation
    for cell, count in neighbor_counts.items():
        if cell in live_cells:
            # Current live cell survives if it has 2 or 3 neighbors
            if count == 2 or count == 3:
                new_live.add(cell)
        else:
            # Dead cell becomes alive if it has exactly 3 neighbors
            if count == 3:
                new_live.add(cell)
    return new_live

def save_pattern(file_path, live_cells):
    """Save the current live cell coordinates to a file."""
    try:
        with open(file_path, 'w') as f:
            for (x, y) in sorted(live_cells):
                f.write(f"{x},{y}\n")
        print(f"Pattern saved to {file_path}")
    except IOError as e:
        print(f"Error saving pattern to {file_path}: {e}")

def load_pattern(file_path, width, height):
    """Load live cell coordinates from a file and return as a set."""
    live_cells = set()
    try:
        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(',')
                if len(parts) != 2:
                    continue
                try:
                    x, y = int(parts[0]), int(parts[1])
                except ValueError:
                    continue
                # Only add coordinates that fit on the board
                if 0 <= x < width and 0 <= y < height:
                    live_cells.add((x, y))
        print(f"Pattern loaded from {file_path}")
    except FileNotFoundError:
        print(f"Pattern file {file_path} not found.")
    return live_cells

def random_fill(width, height):
    """Generate a random set of live cells."""
    live_cells = set()
    for x in range(width):
        for y in range(height):
            if random.random() < 0.2:  # 20% chance cell is alive
                live_cells.add((x, y))
    return live_cells

def main():
    args = parse_args()
    width, height = args.width, args.height
    fps = args.fps
    cell_size = 10  # size of each cell in pixels

    # Initialize Pygame
    pygame.init()
    window_width = width * cell_size
    window_height = height * cell_size
    screen = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Conway's Game of Life")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 24)

    # Colors
    BG_COLOR = (10, 10, 10)        # Background color
    GRID_COLOR = (40, 40, 40)      # Grid line color
    ALIVE_COLOR = (255, 255, 255)  # Alive cell color
    TEXT_COLOR = (200, 200, 200)   # Text color

    live_cells = set()
    paused = True  # Start in paused state

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
                elif event.key == pygame.K_n:
                    # Advance one generation and pause
                    live_cells = next_gen(live_cells, width, height)
                    paused = True
                elif event.key == pygame.K_c:
                    # Clear the board
                    live_cells.clear()
                elif event.key == pygame.K_r:
                    # Randomly fill the board
                    live_cells = random_fill(width, height)
                elif event.key == pygame.K_s:
                    # Save pattern to file
                    save_pattern('patterns.txt', live_cells)
                elif event.key == pygame.K_l:
                    # Load pattern from file
                    live_cells = load_pattern('patterns.txt', width, height)

        # Update the game state
        if not paused:
            live_cells = next_gen(live_cells, width, height)

        # Draw the board
        screen.fill(BG_COLOR)

        # Draw alive cells
        for (x, y) in live_cells:
            rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, ALIVE_COLOR, rect)

        # Draw grid lines (optional)
        for x in range(width):
            pygame.draw.line(screen, GRID_COLOR, (x * cell_size, 0), (x * cell_size, window_height))
        for y in range(height):
            pygame.draw.line(screen, GRID_COLOR, (0, y * cell_size), (window_width, y * cell_size))

        # Display FPS and live cell count
        fps_text = font.render(f"FPS: {int(clock.get_fps())}", True, TEXT_COLOR)
        cell_text = font.render(f"Cells: {len(live_cells)}", True, TEXT_COLOR)
        screen.blit(fps_text, (5, 5))
        screen.blit(cell_text, (5, 25))

        # Display instructions
        instructions = font.render("Space:Play/Pause  N:Next  C:Clear  R:Random  S:Save  L:Load", True, TEXT_COLOR)
        screen.blit(instructions, (5, window_height - 30))

        # Update display and tick clock
        pygame.display.flip()
        clock.tick(fps)

if __name__ == "__main__":
    main()
