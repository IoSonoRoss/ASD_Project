import random
import math
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch

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

def visualizza_gridmap_pcolormesh(grid):
    np_grid = np.array(grid)
    rows, cols = np_grid.shape

    cmap = ListedColormap(['white', '#333399']) # Un blu facile da vedere
    fig, ax = plt.subplots()

    # La logica corretta per pcolormesh
    x_coords = np.arange(cols + 1)
    y_coords = np.arange(rows + 1)
    ax.pcolormesh(x_coords, y_coords, np_grid, cmap=cmap, edgecolors='black', linewidth=1)

    ax.set_title("Griglia iniziale con ostacoli")
    ax.set_aspect('equal')
    ax.invert_yaxis()
    ax.axis('off') # Rimuoviamo gli assi per chiarezza

    plt.show()

def visualizza_risultato_finale(vis_grid, cmap, legend_patches, titolo):
    """
    Funzione di visualizzazione generica che usa pcolormesh
    per un output pulito con bordi neri per ogni cella.
    """
    np_grid = np.array(vis_grid)
    
    fig, ax = plt.subplots(figsize=(16, 9))
    
    ax.pcolormesh(np_grid, cmap=cmap, edgecolors='black', linewidth=0.5)
    
    ax.set_title(titolo, fontsize=16)
    ax.set_aspect('equal')
    ax.invert_yaxis()
    
    ax.set_xticks([])
    ax.set_yticks([])
    
    ax.legend(handles=legend_patches, bbox_to_anchor=(1.02, 1), loc='upper left')
    
    plt.tight_layout()
    plt.show()

    # --- da vedere se servono o meno ---

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

def definisci_quadranti(grid, start_pos):
    """
    Data una griglia e un punto di origine, classifica tutti gli ostacoli (valore 1)
    nei quattro quadranti standard. Gli ostacoli sugli assi non appartengono a nessun quadrante.

    Convenzione dei quadranti (come da immagine):
    - I  : in alto a destra
    - II : in alto a sinistra
    - III: in basso a sinistra
    - IV : in basso a destra

    :param grid: La griglia 2D (lista di liste o array NumPy).
    :param start_pos: Una tupla (start_row, start_col) per le coordinate dell'origine.
    :return: 4 liste, una per ogni quadrante, contenenti le coordinate (row, col) degli ostacoli.
    """
    start_row, start_col = start_pos
    num_rows = len(grid)
    num_cols = len(grid[0])

    # Liste per contenere le coordinate degli ostacoli in ogni quadrante
    primo_quadrante = []   
    secondo_quadrante = [] 
    terzo_quadrante = []   
    quarto_quadrante = []  

    # Scansiona ogni cella della griglia
    for row in range(num_rows):
        for col in range(num_cols):
                # Confronta le coordinate con quelle dell'origine
                
                # Quadrante I (in alto a destra)
                if row < start_row and col > start_col:
                    primo_quadrante.append((row, col))
                    
                # Quadrante II (in alto a sinistra)
                elif row < start_row and col < start_col:
                    secondo_quadrante.append((row, col))
                    
                # Quadrante III (in basso a sinistra)
                elif row > start_row and col < start_col:
                    terzo_quadrante.append((row, col))
                    
                # Quadrante IV (in basso a destra)
                elif row > start_row and col > start_col:
                    quarto_quadrante.append((row, col))
    
    return primo_quadrante, secondo_quadrante, terzo_quadrante, quarto_quadrante

def is_region_free(grid, origin, destination):
    """
    Verifica se l'intera regione rettangolare delimitata dai percorsi di
    Tipo 1 e Tipo 2 è libera da ostacoli.
    Questo implementa il vincolo di "raggiungibilità reciproca".
    """
    r_o, c_o = origin
    r_d, c_d = destination

    # Determina le coordinate minime e massime per righe e colonne,
    # definendo così il rettangolo di delimitazione.
    min_r, max_r = min(r_o, r_d), max(r_o, r_d)
    min_c, max_c = min(c_o, c_d), max(c_o, c_d)

    # Scansiona ogni cella all'interno di questo rettangolo
    for r in range(min_r, max_r + 1):
        for c in range(min_c, max_c + 1):
            if grid[r][c] == 1:
                return False  # Trovato un ostacolo nella regione
                
    return True # La regione è completamente libera
