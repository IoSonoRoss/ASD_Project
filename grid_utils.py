import random
import math
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap

def generate_grid_map(rows=10, cols=10, num_obstacles=None, obstacle_ratio=0.2):
    """
    Genera una mappa a griglia (matrice) con ostacoli casuali.
    :param rows: Numero di righe nella griglia.
    :param cols: Numero di colonne nella griglia.
    :param num_obstacles: Numero di celle ostacolo (se None, usa obstacle_ratio).
    :param obstacle_ratio: Percentuale predefinita di ostacoli se num_obstacles non è specificato.
    :return: Lista 2D che rappresenta la griglia (0: vuoto, 1: ostacolo).
    """
    grid = [[0 for _ in range(cols)] for _ in range(rows)]
    total_cells = rows * cols
    if num_obstacles is None:
        num_obstacles = int(obstacle_ratio * total_cells)
    placed = 0
    while placed < num_obstacles:
        x, y = random.randint(0, rows - 1), random.randint(0, cols - 1)
        if grid[x][y] == 0:
            grid[x][y] = 1
            placed += 1
    return grid

def print_grid(grid):
    """
    Stampa la mappa a griglia e le sue caratteristiche.
    """
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    total_cells = rows * cols
    num_obstacles = sum(cell for row in grid for cell in row)
    print(f"\nCaratteristiche della grid map:")
    print(f"  Righe: {rows}")
    print(f"  Colonne: {cols}")
    print(f"  Celle totali: {total_cells}")
    print(f"  Numero di ostacoli: {num_obstacles}")
    print("Grid map:")
    for row in grid:
        print(' '.join(str(cell) for cell in row))
    print()

def is_within_bounds(x, y, grid):
    """
    Verifica se la posizione (x, y) è dentro i limiti della gridmap.
    """
    return 0 <= x < len(grid) and 0 <= y < len(grid[0])

def is_obstacle(x, y, grid):
    """
    Verifica se la cella (x, y) non è un ostacolo.
    """
    return grid[x][y] == 0

def move(x, y, direction, grid):
    """
    Muove la posizione (x, y) in una direzione specificata se possibile.
    :param x: Coordinata x corrente.
    :param y: Coordinata y corrente.
    :param direction: Direzione in cui muoversi ('N', 'S', 'E', 'O', 'NE', 'NO', 'SE', 'SO').
    :param grid: La griglia su cui muoversi.
    :return: (nuova_x, nuova_y, costo) o None se il movimento non è possibile.
    """
    directions = {
        'N':  (-1,  0, 1),
        'S':  ( 1,  0, 1),
        'E':  ( 0,  1, 1),
        'O':  ( 0, -1, 1),
        'NE': (-1,  1, math.sqrt(2)),
        'NO': (-1, -1, math.sqrt(2)),
        'SE': ( 1,  1, math.sqrt(2)),
        'SO': ( 1, -1, math.sqrt(2)),
    }

    if direction not in directions:
        return None
    
    dx, dy, cost = directions[direction]
    new_x, new_y = x + dx, y + dy
    
    if is_within_bounds(new_x, new_y, grid) and is_obstacle(new_x, new_y, grid):
        return (new_x, new_y, cost)
    return None

def visualizza_gridmap_pcolormesh_corretto(grid):
    np_grid = np.array(grid)
    rows, cols = np_grid.shape

    cmap = ListedColormap(['white', '#333399']) # Un blu facile da vedere
    fig, ax = plt.subplots()

    # La logica corretta per pcolormesh
    x_coords = np.arange(cols + 1)
    y_coords = np.arange(rows + 1)
    ax.pcolormesh(x_coords, y_coords, np_grid, cmap=cmap, edgecolors='black', linewidth=1)

    ax.set_title("Test di Isolamento: Dovresti vedere TUTTI i bordi")
    ax.set_aspect('equal')
    ax.invert_yaxis()
    ax.axis('off') # Rimuoviamo gli assi per chiarezza

    plt.show()

def print_grid_matplotlib_full_obstacles(grid):
    """
    Visualizza la mappa a griglia usando Matplotlib, colorando di nero l'intera cella se è un ostacolo.
    :param grid: Lista 2D che rappresenta la griglia (0: vuoto, 1: ostacolo).
    """
    np_grid = np.array(grid)
    # Usa ListedColormap per forzare 0=bianco, 1=nero
    cmap = ListedColormap(['white', 'black'])

    plt.imshow(np_grid, cmap=cmap, interpolation='none', origin='upper')

    # Griglia sottile per separare le celle
    plt.grid(True, which='both', color='lightgray', linewidth=0.5)
    plt.xticks(np.arange(0, np_grid.shape[1]), np.arange(0, np_grid.shape[1]))
    plt.yticks(np.arange(0, np_grid.shape[0]), np.arange(0, np_grid.shape[0]))
    plt.title("Visualizzazione GridMap (ostacoli neri)")
    plt.xlabel("Colonna")
    plt.ylabel("Riga")
    plt.show()


if __name__ == "__main__":
    try:
        rows = int(input("Inserisci il numero di righe della gridmap: "))
        cols = int(input("Inserisci il numero di colonne della gridmap: "))
        num_obstacles_input = input("Inserisci il numero di ostacoli (premi invio per usare la percentuale predefinita): ")
        if num_obstacles_input.strip() == "":
            grid = generate_grid_map(rows, cols)
        else:
            num_obstacles = int(num_obstacles_input)
            grid = generate_grid_map(rows, cols, num_obstacles=num_obstacles)
        print_grid(grid)

        # print_grid_matplotlib_full_obstacles(grid)  <-- Commentato per evitare conflitti con visualizza_gridmap_pcolormesh
        visualizza_gridmap_pcolormesh(grid)
    except Exception as e:
        print(f"Errore nell'input: {e}")
