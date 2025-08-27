import numpy as np
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch
from data_structures import Grid
import grid_generator
import visualization
from solver import PathfindingSolver 

def get_user_configuration():
    """
    Gestisce l'input dell'utente per la configurazione della griglia in modo robusto,
    con cicli di validazione per righe e colonne.
    """
    
    while True:
        try:
            rows_input = input("Inserisci il numero di righe della griglia: ")
            rows = int(rows_input)
            if rows > 0:
                break  
            else:
                print("ERRORE: Il numero di righe deve essere un intero positivo. Riprova.")
        except ValueError:
            print("ERRORE: Input non valido. Inserisci un numero intero. Riprova.")

    while True:
        try:
            cols_input = input("Inserisci il numero di colonne della griglia: ")
            cols = int(cols_input)
            if cols > 0:
                break  
            else:
                print("ERRORE: Il numero di colonne deve essere un intero positivo. Riprova.")
        except ValueError:
            print("ERRORE: Input non valido. Inserisci un numero intero. Riprova.")

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

def main():
    """
    Script principale per eseguire il test del Compito 3 utilizzando
    l'architettura rifattorizzata basata sulla classe PathfindingSolver.
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

    while True:
        try:
            O_input = input("Inserisci le coordinate dell'origine: ").strip()
            O = tuple(map(int, O_input.split(',')))
            if not (0 <= O[0] < len(grid_data) and 0 <= O[1] < len(grid_data[0])):
                print("ERRORE: Coordinate fuori dai limiti della griglia. Riprova.")
                continue
            if grid_data[O[0]][O[1]] == 1:
                print("ERRORE: La cella di origine è un ostacolo. Riprova.")
                continue
            break
        except (ValueError, IndexError):
            print("ERRORE: Formato non valido. Usa 'riga,colonna'. Riprova.")

    while True:
        try:
            D_input = input("Inserisci le coordinate della destinazione: ").strip()
            D = tuple(map(int, D_input.split(',')))
            if not (0 <= D[0] < len(grid_data) and 0 <= D[1] < len(grid_data[0])):
                print("ERRORE: Coordinate fuori dai limiti della griglia. Riprova.")
                continue
            if grid_data[D[0]][D[1]] == 1:
                print("ERRORE: La cella di destinazione è un ostacolo. Riprova.")
                continue
            break
        except (ValueError, IndexError):
            print("ERRORE: Formato non valido. Usa 'riga,colonna'. Riprova.")
    
    print(f"\nOrigine scelta: {O}, Destinazione scelta: {D}")

    solver_instance = PathfindingSolver(grid_data, O, D)
    
    solver_instance.visualize_initial_closure_and_frontier()
    
    solver_instance.solve()
    
    solver_instance.display_results()

if __name__ == "__main__":
    main()