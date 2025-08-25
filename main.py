import numpy as np
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch

import grid_generator
import visualization
from data_structures import Grid
import closure_logic
import path_logic # Necessario per calcola_distanza_libera

def main_compito2():
    """
    Script principale per dimostrare le funzionalita del Compito 2:
    - Generazione di una griglia.
    - Calcolo di Contesto, Complemento e Frontiera per un'origine data.
    - Calcolo della distanza libera tra due punti.
    - Visualizzazione grafica dei risultati.
    """
    
    try:
        rows = int(input("Inserisci il numero di righe della griglia: "))
        cols = int(input("Inserisci il numero di colonne della griglia: "))
        obstacle_ratio_input = input("Inserisci la percentuale di ostacoli (default: 20%): ") or "20"
        obstacle_ratio = int(obstacle_ratio_input) / 100.0
        if not (0 <= obstacle_ratio <= 1):
            raise ValueError
    except ValueError:
        print("Input non valido. Utilizzo valori di default.")

    grid_data = grid_generator.generate_grid_map(rows=rows, cols=cols, obstacle_ratio=obstacle_ratio)
    grid = Grid.from_matrix(grid_data)
    print(f"\nGriglia {rows}x{cols} con {len(grid.adj)} celle attraversabili generata.")
    
    while True:
        try:
            o_input = input(f"Inserisci le coordinate dell'origine (riga,colonna): ").strip()
            O = tuple(map(int, o_input.split(',')))
            if not grid.is_traversable(O):
                print("ERRORE: La cella di origine non è attraversabile (è un ostacolo o fuori dai limiti). Riprova.")
                continue
            break
        except (ValueError, IndexError):
            print("ERRORE: Formato non valido. Usa 'riga,colonna'. Riprova.")

    while True:
        try:
            d_input = input(f"Inserisci le coordinate della destinazione (riga,colonna): ").strip()
            D = tuple(map(int, d_input.split(',')))
            if not grid.is_traversable(D):
                print("ERRORE: La cella di destinazione non è attraversabile. Riprova.")
                continue
            break
        except (ValueError, IndexError):
            print("ERRORE: Formato non valido. Usa 'riga,colonna'. Riprova.")
            
    print(f"\nOrigine scelta: O={O}, Destinazione scelta: D={D}")

    distanza_libera = path_logic.calcola_distanza_libera(O, D)
    print(f"\n1. Calcolo Distanza Libera (dlib):")
    print(f"   dlib(O, D) = {distanza_libera:.4f}")

    print("\n2. Calcolo di Contesto e Complemento per O...")
    contesto, complemento = closure_logic.calcola_contesto_e_complemento(grid, O)

    print(f"   -> Trovate {len(contesto)} celle nel Contesto di O.")
    print(f"   -> Trovate {len(complemento)} celle nel Complemento di O.")
       
    print("\nGenerazione della visualizzazione grafica in corso...")
    
    CELL_CONTESTO, CELL_COMPLEMENTO, CELL_ORIGINE, CELL_DESTINAZIONE = 2, 3, 4, 6
    
    valori_speciali = {}
    for r, c in contesto: valori_speciali[(r, c)] = CELL_CONTESTO
    for r, c in complemento: valori_speciali[(r, c)] = CELL_COMPLEMENTO
    
    valori_speciali[O] = CELL_ORIGINE
    valori_speciali[D] = CELL_DESTINAZIONE
    
    vis_grid = grid.to_matrix(custom_values=valori_speciali)

    # Preparazione legenda per il grafico
    color_map = {0:'white', 1:'#30307A', 2:'#90EE90', 3:'#FFD700', 4:'#FF0000', 5:'#006400', 6:'#800080'}
    label_map = {0:'Spazio Libero', 1:'Ostacolo', 2:'Contesto di O', 3:'Complemento di O', 4:'Origine O', 5:'Frontiera di O', 6:'Destinazione D'}
    cmap = ListedColormap([color_map.get(i) for i in sorted(color_map.keys())])
    legend_patches = [Patch(facecolor=color, edgecolor='black', label=label_map[key]) for key, color in color_map.items()]
    titolo = f"Analisi Spazio per O={O} (Compito 2)"
    
    visualization.visualizza_risultato_finale(vis_grid, cmap, legend_patches, titolo)
    print("\nVisualizzazione mostrata. Programma terminato.")


if __name__ == "__main__":
    main_compito2()