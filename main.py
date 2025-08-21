from matplotlib import pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch
import numpy as np
import grid_utils_new as grid_utils
import path_utils_new as path_utils
import solver

def main():
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

    # --- 3. ESECUZIONE DEL SOLVER E STAMPA RISULTATO ---
    
    # Crea un'istanza del solver con i dati del problema
    solver_instance = solver.PathfindingSolver(grid_test, O, D)

    solver_instance.visualize_closure()

    # Esegui l'algoritmo
    solver_instance.solve()

    # Recupera i risultati
    lunghezza, sequenza_landmark = solver_instance.get_results()

    solver_instance.display_results()

    # solver_instance.visualize_solution() <--- valutare se può eliminare

if __name__ == "__main__":
    main()