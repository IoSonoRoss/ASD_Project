import random

def generate_grid_map(rows=10, cols=20, obstacle_ratio=0.2):
    """
    Genera una mappa a griglia con ostacoli,
    basandosi esclusivamente su una percentuale.
    """

    grid = [[0 for _ in range(cols)] for _ in range(rows)]
    
    # Calcola il numero di ostacoli da piazzare basandosi solo sul rapporto
    total_cells = rows * cols
    num_obstacles_to_place = int(total_cells * obstacle_ratio)

    # Assicurati di non tentare di piazzare più ostacoli delle celle disponibili
    if num_obstacles_to_place >= total_cells:
        # Se il rapporto è 1.0 o più, restituisci una griglia piena
        return [[1 for _ in range(cols)] for _ in range(rows)]
        
    placed_obstacles = 0
    # Evita un ciclo infinito se la griglia è quasi piena
    max_attempts = total_cells * 3
    attempts = 0
    while placed_obstacles < num_obstacles_to_place and attempts < max_attempts:
        r = random.randint(0, rows - 1)
        c = random.randint(0, cols - 1)
        if grid[r][c] == 0:
            grid[r][c] = 1
            placed_obstacles += 1
        attempts += 1
    
    # Se il ciclo si interrompe per troppi tentativi, avvisa l'utente
    if attempts >= max_attempts:
        print(f"Attenzione: non è stato possibile piazzare tutti i {num_obstacles_to_place} ostacoli richiesti.")
        print(f"Ostacoli piazzati: {placed_obstacles}")
            
    return grid

def print_grid_info(grid):
    """Stampa le caratteristiche della griglia."""
    rows = len(grid) if grid else 0
    cols = len(grid[0]) if rows > 0 else 0
    num_obstacles = sum(row.count(1) for row in grid)
    print(f"\n--- Caratteristiche della Grid Map ---")
    print(f"  Dimensioni: {rows} righe x {cols} colonne")
    print(f"  Ostacoli: {num_obstacles} ({ (num_obstacles / (rows*cols))*100 :.2f}%)")
    print("-" * 35)