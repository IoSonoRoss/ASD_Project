import random

def generate_grid_map(rows=10, cols=20, obstacle_ratio=0.15):
    """Genera una mappa a griglia con ostacoli casuali."""
    grid = [[0 for _ in range(cols)] for _ in range(rows)]
    num_obstacles = int(rows * cols * obstacle_ratio)
    placed_obstacles = 0
    while placed_obstacles < num_obstacles:
        r, c = random.randint(0, rows - 1), random.randint(0, cols - 1)
        if grid[r][c] == 0:
            grid[r][c] = 1
            placed_obstacles += 1
    return grid

def print_grid_info(grid):
    """Stampa le caratteristiche della griglia."""
    rows, cols = len(grid), len(grid[0])
    num_obstacles = sum(row.count(1) for row in grid)
    print(f"\n--- Caratteristiche della Grid Map ---")
    print(f"  Dimensioni: {rows} righe x {cols} colonne")
    print(f"  Ostacoli: {num_obstacles}")
    print("-" * 35)