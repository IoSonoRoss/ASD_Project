import random

def generate_grid_map(rows=10, cols=20, obstacle_ratio=0.2, num_obstacles=None):
    """
    [Versione Corretta] Genera una mappa a griglia con ostacoli.
    Se 'num_obstacles' è specificato, usa quel valore.
    Altrimenti, calcola il numero di ostacoli usando 'obstacle_ratio'.
    """
    grid = [[0 for _ in range(cols)] for _ in range(rows)]
    
    # Determina il numero di ostacoli da piazzare
    if num_obstacles is None:
        total_cells = rows * cols
        num_obstacles_to_place = int(total_cells * obstacle_ratio)
    else:
        num_obstacles_to_place = num_obstacles

    # Assicurati di non tentare di piazzare più ostacoli delle celle disponibili
    if num_obstacles_to_place >= rows * cols:
        print("Attenzione: il numero di ostacoli è maggiore o uguale al numero di celle. La griglia sarà piena.")
        return [[1 for _ in range(cols)] for _ in range(rows)]
        
    placed_obstacles = 0
    while placed_obstacles < num_obstacles_to_place:
        r = random.randint(0, rows - 1)
        c = random.randint(0, cols - 1)
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