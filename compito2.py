from matplotlib import pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch
import numpy as np
import grid_utils

def main():

    grid_5x5 = [
    [0, 0, 1, 1],
    [1, 0, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 0, 1]
]

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
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
]
    
    grid_test = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]

    grid_utils.visualizza_gridmap_pcolormesh(grid_test)

    # Definisci origine e destinazione
    O = (4, 6)
    # D = (8, 14) 
    D = (7, 17)

    print(f"Controllo valore: {grid_test[0][0]}")

    print(f"Origine: {O}, Destinazione: {D}\n")

    paths_with_types = grid_utils.find_free_paths(grid_test, O, D)

    if not paths_with_types:
        print("Nessun cammino libero trovato.")
    else:
        print(f"Trovati {len(paths_with_types)} cammini liberi:")
        # Cicla sulla lista di tuple e "spacchetta" tipo e percorso
        for path_type, path_coords in paths_with_types:
            print(f"Cammino di {path_type}: {path_coords}")
    
    print(f"\nGenerazione del cammino minimo ideale (giallo) da {O} a {D}...\n")

    # Genera il percorso
    path_giallo = grid_utils.generate_ideal_minimum_path(O, D)

    print("\nCammino 'giallo' trovato:\n")
    print(path_giallo)

    print(f"Calcolo del Contesto e Complemento per l'origine O={O}...")
    contesto, complemento = grid_utils.calcola_contesto_e_complemento(grid_test, O)

    print(f"\n--- Contesto di O ---")
    print(f"Trovate {len(contesto)} celle.")

    print(f"\n--- Complemento di O ---")
    print(f"Trovate {len(complemento)} celle.")
    
    # 4. Prepara la griglia per la visualizzazione
    vis_grid = np.array(grid_test, dtype=int)
    for r, c in contesto:
        vis_grid[r, c] = 2  # Valore per il Contesto
    for r, c in complemento:
        vis_grid[r, c] = 3  # Valore per il Complemento
    vis_grid[O[0], O[1]] = 4  # Valore per l'Origine

    # 1. Definisci i colori e le etichette per la legenda
    color_map = {
        0: 'white',        
        1: '#30307A',       
        2: '#90EE90',       
        3: '#FFD700',      
        4: '#FF0000'        
    }
    label_map = {
        0: 'Spazio Libero',
        1: 'Ostacolo',
        2: 'Contesto di O',
        3: 'Complemento di O',
        4: 'Origine O'
    }

    # 2. Crea la Colormap di Matplotlib
    cmap = ListedColormap([color_map[i] for i in sorted(color_map.keys())])

    # 3. Crea gli elementi della legenda (le "Patch" colorate)
    legend_patches = [Patch(facecolor=color, edgecolor='black', label=label) 
                      for color, label in zip(color_map.values(), label_map.values())]

    # 4. Chiama la funzione di visualizzazione, passando anche gli elementi della legenda
    titolo = f"Contesto e Complemento di O={O}"
    grid_utils.visualizza_risultato_finale(vis_grid, cmap, legend_patches, titolo)

    distanza_calcolata = grid_utils.calcola_distanza_libera(O, D)
    print(f"\nDistanza calcolata tra O e D: {distanza_calcolata}")

if __name__ == "__main__":
    main()