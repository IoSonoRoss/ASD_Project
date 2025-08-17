from matplotlib import pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch
import numpy as np
import grid_utils_new as grid_utils
import path_utils_new as path_utils
import solver # Importa la nuova classe

def main():
    # --- 1. CREAZIONE DELLA GRIGLIA E INPUT UTENTE ---
    rows = int(input("Inserisci il numero di righe della gridmap: "))
    cols = int(input("Inserisci il numero di colonne della gridmap: "))
    num_obstacles_input = input("Inserisci il numero di ostacoli (premi invio per usare il 20%): ")
    
    if num_obstacles_input.strip() == "":
        grid_test = grid_utils.generate_grid_map(rows, cols, obstacle_ratio=0.2)
    else:
        num_obstacles = int(num_obstacles_input)
        grid_test = grid_utils.generate_grid_map(rows, cols, num_obstacles=num_obstacles)
    
    grid_utils.print_grid(grid_test)
    grid_utils.visualizza_gridmap_pcolormesh(grid_test)

    # Input Origine e Destinazione con validazione
    while True:
        try:
            O_input = input("Inserisci le coordinate dell'origine (riga,colonna): ").strip()
            O = tuple(map(int, O_input.split(',')))
            if grid_test[O[0]][O[1]] == 1:
                print("ERRORE: La cella di origine è un ostacolo. Riprova.")
                continue
            break
        except (ValueError, IndexError):
            print("ERRORE: Input non valido o coordinate fuori dalla griglia. Riprova.")

    while True:
        try:
            D_input = input("Inserisci le coordinate della destinazione (riga,colonna): ").strip()
            D = tuple(map(int, D_input.split(',')))
            if grid_test[D[0]][D[1]] == 1:
                print("ERRORE: La cella di destinazione è un ostacolo. Riprova.")
                continue
            break
        except (ValueError, IndexError):
            print("ERRORE: Input non valido o coordinate fuori dalla griglia. Riprova.")
    
    print(f"\nOrigine scelta: {O}, Destinazione scelta: {D}\n")

    # --- 2. CALCOLI PRELIMINARI E VISUALIZZAZIONE CHIUSURA ---
    print(f"Calcolo della chiusura e frontiera per l'origine O={O}...")
    contesto, complemento = path_utils.calcola_contesto_e_complemento(grid_test, O)
    frontiera_con_tipo = path_utils.calcola_frontiera(grid_test, O, contesto, complemento)
    print(f"  Trovate {len(contesto)} celle nel Contesto, {len(complemento)} nel Complemento, {len(frontiera_con_tipo)} di Frontiera.")
    
    vis_grid = np.array(grid_test, dtype=int)
    for r, c in contesto: vis_grid[r, c] = 2
    for r, c in complemento: vis_grid[r, c] = 3
    for (r, c), _ in frontiera_con_tipo: vis_grid[r, c] = 5
    vis_grid[O[0], O[1]] = 4
    vis_grid[D[0], D[1]] = 6

    color_map = {0:'white', 1:'#30307A', 2:'#90EE90', 3:'#FFD700', 4:'#FF0000', 5:'#006400', 6:'#800080'}
    label_map = {0:'Spazio Libero', 1:'Ostacolo', 2:'Contesto di O', 3:'Complemento di O', 4:'Origine O', 5:'Frontiera di O', 6:'Destinazione D'}
    cmap = ListedColormap([color_map.get(i) for i in sorted(color_map.keys())])
    legend_patches = [Patch(facecolor=color, edgecolor='black', label=label_map[key]) for key, color in color_map.items()]
    titolo = f"Chiusura e Frontiera di O={O}"
    grid_utils.visualizza_risultato_finale(vis_grid, cmap, legend_patches, titolo)

    # --- 3. ESECUZIONE DEL SOLVER E STAMPA RISULTATO ---
    
    # Crea un'istanza del solver con i dati del problema
    solver = PathfindingSolver(grid_test, O, D)
    # Esegui l'algoritmo
    solver.solve()
    
    # Recupera i risultati
    lunghezza, sequenza_landmark = solver.get_results()

    if lunghezza == float('inf'):
        print("\nRISULTATO: La destinazione D non è raggiungibile da O.")
    else:
        print(f"\nRISULTATO:")
        print(f"  Lunghezza del cammino minimo: {lunghezza:.4f}")
        
        mappa_finale = solver.get_label_map()
        
        print("\n--- DEBUG: Mappa Etichette Globale Creata ---")
        for coord, label in sorted(mappa_finale.items()):
            print(f"  {coord} -> '{label}'")
        print("---------------------------------------------")

        output_str = "<"
        for i, (lm_coords, tipo) in enumerate(sequenza_landmark):
            label = "O" if lm_coords == O else "D" if lm_coords == D else mappa_finale.get(lm_coords, str(lm_coords))
            output_str += f"({label}, {tipo}) "
        print(f"\n  Sequenza di landmark: {output_str.strip()}>")

if __name__ == "__main__":
    main()