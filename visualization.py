import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap

def visualizza_gridmap_pcolormesh(grid):
    """
    Visualizza la mappa a griglia utilizzando pcolormesh di Matplotlib.
    """
    np_grid = np.array(grid)
    rows, cols = np_grid.shape

    cmap = ListedColormap(['white', '#333399']) 
    fig, ax = plt.subplots()

    x_coords = np.arange(cols + 1)
    y_coords = np.arange(rows + 1)
    ax.pcolormesh(x_coords, y_coords, np_grid, cmap=cmap, edgecolors='black', linewidth=1)

    ax.set_title("Griglia iniziale")
    ax.set_aspect('equal')
    ax.invert_yaxis()
    ax.axis('off') 

    plt.show()

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