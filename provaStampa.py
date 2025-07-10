import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap

def visualizza_gridmap_pcolormesh(grid, show_labels=True):
    """
    Visualizza una mappa a griglia usando Matplotlib.pcolormesh.
    Questo metodo disegna le celle correttamente allineate alla griglia.

    :param grid: Lista 2D o array NumPy che rappresenta la griglia (0: vuoto, 1: ostacolo).
    :param show_labels: Se True, mostra titoli e etichette degli assi.
    """
    # Converte la lista in un array NumPy per coerenza
    np_grid = np.array(grid)
    rows, cols = np_grid.shape

    # Crea una mappa di colori: 0 -> bianco, 1 -> blu scuro (o nero)
    # Puoi cambiare 'midnightblue' con 'black' se preferisci
    cmap = ListedColormap(['white', 'midnightblue'])

    # Crea la figura e gli assi
    fig, ax = plt.subplots()

    # Usa pcolormesh: disegna la griglia colorata.
    # edgecolors='black' disegna i bordi neri per ogni cella.
    ax.pcolormesh(np_grid, cmap=cmap, edgecolors='black', linewidth=0.5)

    # Imposta gli assi per avere una visualizzazione pulita
    ax.set_aspect('equal')  # Assicura che le celle siano quadrate
    ax.invert_yaxis()      # Porta l'origine (0,0) nell'angolo in alto a sinistra

    # Rimuove i "ticks" (le lineette) ma mantiene le etichette numeriche
    ax.tick_params(length=0)

    if show_labels:
        # Posiziona le etichette numeriche al centro delle celle
        ax.set_xticks(np.arange(cols) + 0.5)
        ax.set_yticks(np.arange(rows) + 0.5)
        # Assegna i valori numerici corretti alle etichette
        ax.set_xticklabels(np.arange(cols))
        ax.set_yticklabels(np.arange(rows))
        
        ax.set_title("Visualizzazione GridMap (ostacoli colorati)")
        ax.set_xlabel("Colonna")
        ax.set_ylabel("Riga")
    else:
        # Se non si vogliono le etichette, si nascondono gli assi
        ax.axis('off')

    plt.tight_layout() # Ottimizza lo spazio
    plt.show()


# --- Esempio di utilizzo ---

# La tua gridmap 5x5 originale
grid_5x5 = [
    [0, 0, 0, 0, 0],
    [0, 1, 1, 0, 0],
    [0, 0, 0, 1, 1],
    [0, 1, 1, 0, 0],
    [0, 0, 0, 1, 1]
]

# La gridmap più grande simile alla tua seconda immagine
grid_grande = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]


# 1. Visualizzazione della griglia piccola con etichette
print("Visualizzazione della griglia 5x5 (stile corretto):")
visualizza_gridmap_pcolormesh(grid_5x5, show_labels=True)

# 2. Visualizzazione della griglia grande senza etichette (come la tua immagine di esempio)
print("\nVisualizzazione della griglia grande senza etichette:")
visualizza_gridmap_pcolormesh(grid_grande, show_labels=False)