# File: grid_utils.py

import random
import math
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch

def generate_grid_map(rows=10, cols=20, obstacle_ratio=0.15):
    """
    Genera una mappa a griglia (matrice) con ostacoli casuali.
    """
    grid = [[0 for _ in range(cols)] for _ in range(rows)]
    num_obstacles = int(rows * cols * obstacle_ratio)
    placed_obstacles = 0
    while placed_obstacles < num_obstacles:
        r, c = random.randint(0, rows - 1), random.randint(0, cols - 1)
        # Assicura che non vengano piazzati ostacoli in posizioni chiave per il debug
        if grid[r][c] == 0:
            grid[r][c] = 1
            placed_obstacles += 1
    return grid

def print_grid_info(grid):
    """
    Stampa le caratteristiche della griglia.
    """
    rows = len(grid) if grid else 0
    cols = len(grid[0]) if rows > 0 else 0
    num_obstacles = sum(row.count(1) for row in grid)
    print(f"\n--- Caratteristiche della Grid Map ---")
    print(f"  Dimensioni: {rows} righe x {cols} colonne")
    print(f"  Ostacoli: {num_obstacles}")
    print("-" * 35)

def visualizza_gridmap_pcolormesh(grid):
    """
    Visualizza la griglia iniziale con solo gli ostacoli.
    """
    np_grid = np.array(grid)
    rows, cols = np_grid.shape
    cmap = ListedColormap(['white', '#30307A'])
    fig, ax = plt.subplots(figsize=(12, 6))
    
    x_coords = np.arange(cols + 1)
    y_coords = np.arange(rows + 1)
    
    ax.pcolormesh(x_coords, y_coords, np_grid, cmap=cmap, edgecolors='black', linewidth=0.5)
    ax.set_title("Griglia Iniziale con Ostacoli")
    ax.set_aspect('equal')
    ax.invert_yaxis()
    ax.axis('off')
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