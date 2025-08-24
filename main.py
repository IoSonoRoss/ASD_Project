import numpy as np
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch

# Importa i nuovi moduli rifattorizzati
import grid_generator
import visualization
from solver import PathfindingSolver 

def main():
    """
    Script principale per eseguire il test del Compito 3 utilizzando
    l'architettura rifattorizzata basata sulla classe PathfindingSolver.
    """
    
    # --- 1. IMPOSTAZIONE DEL PROBLEMA TRAMITE INPUT UTENTE ---
    try:
        rows = int(input("Inserisci il numero di righe della gridmap: "))
        cols = int(input("Inserisci il numero di colonne della gridmap: "))
        obstacle_input = input("Inserisci la percentuale di ostacoli (premi invio per default 20%): ")
        
        if obstacle_input.strip() == "":
            # L'utente ha premuto invio, usa il default
            obstacle_ratio = 0.20
            print(f"Nessun valore inserito. Utilizzo la percentuale di default del {obstacle_ratio*100}%.")
            grid_data = grid_generator.generate_grid_map(rows=rows, cols=cols, obstacle_ratio=obstacle_ratio)
        else:
            # L'utente ha inserito un valore, lo interpretiamo come percentuale
            percentuale_ostacoli = int(obstacle_input)
            if not (0 <= percentuale_ostacoli <= 100):
                print("Attenzione: la percentuale deve essere tra 0 e 100. Verrà usato il 20%.")
                obstacle_ratio = 0.20
            else:
                # Converti la percentuale (es. 20) in un rapporto (0.20)
                obstacle_ratio = percentuale_ostacoli / 100.0
            
            print(f"Utilizzo una percentuale di ostacoli del {obstacle_ratio*100}%.")
            grid_data = grid_generator.generate_grid_map(rows=rows, cols=cols, obstacle_ratio=obstacle_ratio)
    except ValueError:
        print("Input non valido. Utilizzo una griglia di default 10x20.")
        grid_data = grid_generator.generate_grid_map(rows=10, cols=20, obstacle_ratio=0.2)

    grid_generator.print_grid_info(grid_data)
    
    # --- VISUALIZZAZIONE 1: GRIGLIA DI BASE ---
    print("\nVisualizzazione della griglia iniziale...")
    visualization.visualizza_gridmap_pcolormesh(grid_data)

    # Input Origine e Destinazione con validazione
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

    # --- 2. CREAZIONE ED ESECUZIONE DEL SOLVER ---
    
    # Crea un'istanza del solver. Il costruttore esegue i calcoli preliminari (chiusura, etc.)
    solver_instance = PathfindingSolver(grid_data, O, D)
    
    # Mostra la visualizzazione della chiusura e frontiera di O
    solver_instance.visualize_closure_and_frontier()
    
    # Esegui l'algoritmo principale per trovare il cammino minimo
    solver_instance.solve()
    
    # --- 3. PRESENTAZIONE DEI RISULTATI ---
    solver_instance.display_results()
    
    # (Futuro) Qui potresti chiamare una funzione di visualizzazione del percorso finale
    # solver_instance.visualize_solution()

if __name__ == "__main__":
    main()