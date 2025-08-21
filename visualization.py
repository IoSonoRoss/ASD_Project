import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap

def visualizza_gridmap_pcolormesh(grid):
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

def visualizza_risultato_finale(grid_da_mostrare, cmap, legend_elements, titolo):
    """
    Funzione di visualizzazione che usa pcolormesh e aggiunge una legenda personalizzata.
    
    :param grid_da_mostrare: La griglia numerica da visualizzare.
    :param cmap: La mappa di colori (ListedColormap).
    :param legend_elements: Una lista di Patch per la legenda.
    :param titolo: Il titolo del grafico.
    """
    np_grid = np.array(grid_da_mostrare)
    
    fig, ax = plt.subplots(figsize=(14, 8)) # Aumentiamo le dimensioni per fare spazio alla legenda

    # Usiamo pcolormesh per disegnare sia i colori che i bordi
    ax.pcolormesh(np_grid, cmap=cmap, edgecolors='black', linewidth=0.5)

    ax.set_title(titolo, fontsize=16)
    ax.set_aspect('equal')
    ax.invert_yaxis()

    # Rimuoviamo gli assi numerici per una visualizzazione pulita
    ax.set_xticks([])
    ax.set_yticks([])
    
    # Aggiungi la legenda al grafico
    ax.legend(handles=legend_elements, bbox_to_anchor=(1.02, 1), loc='upper left')
    
    # Adatta il layout per assicurarsi che la legenda non venga tagliata
    plt.tight_layout()
    
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