from matplotlib import pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch
import numpy as np
import grid_utils_new
import path_utils_new 

def main():
    #grid_test = [
    #    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #    [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
    #    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    #    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    #    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    #    [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    #    [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #]

    #grid_test = [
    #    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #    [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
    #    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    #    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1],
    #    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0],
    #    [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    #    [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #]

    rows = int(input("Inserisci il numero di righe della gridmap: "))
    cols = int(input("Inserisci il numero di colonne della gridmap: "))
    num_obstacles_input = input("Inserisci il numero di ostacoli (premi invio per usare la percentuale predefinita): ")
    if num_obstacles_input.strip() == "":
        grid_test = grid_utils_new.generate_grid_map(rows, cols)
    else:
        num_obstacles = int(num_obstacles_input)
        grid_test = grid_utils_new.generate_grid_map(rows, cols, num_obstacles=num_obstacles)
    grid_utils_new.print_grid(grid_test)

    #O = (4, 6)
    #D = (8, 19)
    #print(f"Origine: {O}, Destinazione: {D}\n")

    grid_utils_new.visualizza_gridmap_pcolormesh(grid_test)

    while True:
        try:
            O = tuple(map(int, input("Inserisci le coordinate dell'origine (riga,colonna): ").strip().split(',')))
            if grid_test[O[0]][O[1]] == 1:
                print("La cella di origine è un ostacolo. Riprova.")
                continue
            break
        except (ValueError, IndexError):
            print("Input non valido o coordinate fuori dalla griglia. Riprova.")

    while True:
        try:
            D = tuple(map(int, input("Inserisci le coordinate della destinazione (riga,colonna): ").strip().split(',')))
            if grid_test[D[0]][D[1]] == 1:
                print("La cella di destinazione è un ostacolo. Riprova.")
                continue
            break
        except (ValueError, IndexError):
            print("Input non valido o coordinate fuori dalla griglia. Riprova.")

    #grid_utils_new.visualizza_gridmap_pcolormesh(grid_test)

    paths_with_types = path_utils_new.find_free_paths(grid_test, O, D)

    if not paths_with_types:
        print("Nessun cammino libero trovato.")
    else:
        print(f"Trovati {len(paths_with_types)} cammini liberi:")
        # Cicla sulla lista di tuple e "spacchetta" tipo e percorso
        for path_type, path_coords in paths_with_types:
            print(f"Cammino di {path_type}: {path_coords}")
    
    print(f"\nGenerazione del cammino minimo ideale (giallo) da {O} a {D}...\n")

    # Genera il percorso
    path_giallo = path_utils_new.generate_ideal_minimum_path(O, D)

    print("\nCammino 'giallo' trovato:\n")
    print(path_giallo)

    print(f"Calcolo del Contesto e Complemento per l'origine O={O}...")
    contesto, complemento = path_utils_new.calcola_contesto_e_complemento(grid_test, O)

    print(f"\n--- Contesto di O ---")
    print(f"Trovate {len(contesto)} celle.")

    print(f"\n--- Complemento di O ---")
    print(f"Trovate {len(complemento)} celle.")

    print(f"\nCalcolo della Frontiera di O...")
    frontiera = path_utils_new.calcola_frontiera(grid_test, O, contesto, complemento)
    print(f"Trovate {len(frontiera)} celle di frontiera.")
    
    # --- VISUALIZZAZIONE 2: CHIUSURA, FRONTIERA E COLORI ---
    print("\nVisualizzazione della chiusura e frontiera di O...")
    vis_grid = np.array(grid_test, dtype=int)
    for r, c in contesto: vis_grid[r, c] = 2
    for r, c in complemento: vis_grid[r, c] = 3
    
    # --- CICLO CORRETTO CHE EVITA L'INDEXERROR ---
    for (r, c), _ in frontiera:
        vis_grid[r, c] = 5
        
    vis_grid[O[0], O[1]] = 4
    vis_grid[D[0], D[1]] = 6

    color_map = {0:'white', 1:'#30307A', 2:'#90EE90', 3:'#FFD700', 4:'#FF0000', 5:'#006400', 6:'#800080'}
    label_map = {0:'Spazio Libero', 1:'Ostacolo', 2:'Contesto di O', 3:'Complemento di O', 4:'Origine O', 5:'Frontiera di O', 6:'Destinazione D'}
    cmap = ListedColormap([color_map.get(i) for i in sorted(color_map.keys())])
    legend_patches = [Patch(facecolor=color, edgecolor='black', label=label_map[key]) for key, color in color_map.items()]
    titolo = f"Chiusura e Frontiera di O={O}"
    grid_utils_new.visualizza_risultato_finale(vis_grid, cmap, legend_patches, titolo)

    # --- ESECUZIONE DI CAMMINOMIN ---
    print(f"--- Esecuzione Procedura CAMMINOMIN da O={O} a D={D} ---")
    
    # 1. Crea un'istanza del gestore di etichette da path_utils_new
    label_manager = path_utils_new.LabelManager()
    
    # 2. Pulisci la cache e chiama la procedura, passando il gestore
    path_utils_new.memoization_cache = {}
    lunghezza, sequenza_landmark = path_utils_new.procedura_cammino_min(O, D, grid_test, label_manager)

    # --- STAMPA E VISUALIZZAZIONE DEL RISULTATO ---
    if lunghezza == float('inf'):
        print("\nRISULTATO: La destinazione D non è raggiungibile da O.")
    else:
        print(f"\nRISULTATO:")
        print(f"  Lunghezza del cammino minimo: {lunghezza:.4f}")
        
        # 3. Ottieni la mappa finale completa dal gestore
        mappa_finale = label_manager.mappa_coord_etichetta
        
        # Stampa di debug per verificare l'unicità e la completezza
        print("\n--- DEBUG: Mappa Etichette Globale Creata ---")
        # Ordina per coordinata (riga, colonna)
        for coord, label in sorted(mappa_finale.items()):
            print(f"  {coord} -> '{label}'")
        print("---------------------------------------------")

        # 4. Stampa la sequenza di landmark usando la mappa
        output_str = "<"
        for i, (lm_coords, tipo) in enumerate(sequenza_landmark):
            # Assegna etichette speciali a O e D, per gli altri cerca nella mappa
            label = "O" if lm_coords == O else "D" if lm_coords == D else mappa_finale.get(lm_coords, str(lm_coords))
            output_str += f"({label}, {tipo}) "
        print(f"\n  Sequenza di landmark: {output_str.strip()}>")

if __name__ == "__main__":
    main()