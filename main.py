import numpy as np
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch

import grid_generator
import visualization
from data_structures import Grid
import closure_logic
import path_logic

def get_user_configuration():
    """
    Gestisce l'input dell'utente per la configurazione della griglia in modo robusto,
    con cicli di validazione per righe e colonne.
    """
    
    # --- Input Robusto per le Righe ---
    while True:
        try:
            rows_input = input("Inserisci il numero di righe della griglia: ")
            rows = int(rows_input)
            if rows > 0:
                break  # L'input e valido, esci dal ciclo
            else:
                print("ERRORE: Il numero di righe deve essere un intero positivo. Riprova.")
        except ValueError:
            print("ERRORE: Input non valido. Inserisci un numero intero. Riprova.")

    # --- Input Robusto per le Colonne ---
    while True:
        try:
            cols_input = input("Inserisci il numero di colonne della griglia: ")
            cols = int(cols_input)
            if cols > 0:
                break  # L'input e valido, esci dal ciclo
            else:
                print("ERRORE: Il numero di colonne deve essere un intero positivo. Riprova.")
        except ValueError:
            print("ERRORE: Input non valido. Inserisci un numero intero. Riprova.")

    # --- Input per gli Ostacoli (con default) ---
    # Questo mantiene il comportamento precedente, che va bene per un parametro non critico.
    try:
        obstacle_ratio_input = input("Inserisci la percentuale di ostacoli (da 0 a 100, default: 20): ") or "20"
        obstacle_ratio = int(obstacle_ratio_input) / 100.0
        if not (0 <= obstacle_ratio <= 1):
            print("Attenzione: Percentuale non valida. Verrà usato il 20%.")
            obstacle_ratio = 0.20
    except ValueError:
        print("Attenzione: Input per ostacoli non valido. Verrà usato il 20%.")
        obstacle_ratio = 0.20
        
    return rows, cols, obstacle_ratio

def main_compito2():
    """
    Script principale per dimostrare le funzionalita del Compito 2:
    - Generazione di una griglia.
    - Calcolo di Contesto e Complemento per un'origine data.
    - Calcolo della distanza libera tra due punti.
    - Visualizzazione grafica dei risultati.
    """
    
    rows, cols, obstacle_ratio = get_user_configuration()

    grid_data = grid_generator.generate_grid_map(rows=rows, cols=cols, obstacle_ratio=obstacle_ratio)
    grid = Grid.from_matrix(grid_data)

    print("Generazione completata.")
    
    num_obstacles = sum(row.count(1) for row in grid_data)
    total_cells = rows * cols
    actual_ratio = (num_obstacles / total_cells) * 100 if total_cells > 0 else 0

    print(f"\n--- Caratteristiche della Grid Map Generata ---")
    print(f"  Dimensioni: {rows} righe x {cols} colonne ({total_cells} celle totali)")
    print(f"  Ostacoli piazzati: {num_obstacles} (~{actual_ratio:.2f}%)")
    print(f"  Celle attraversabili (nodi del grafo): {len(grid.adj)}")
    print("-" * 45)
    
    print("\nVisualizzazione della mappa generata...")
    visualization.visualizza_gridmap_pcolormesh(grid_data)

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