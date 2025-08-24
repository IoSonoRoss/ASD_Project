import grid_generator
import visualization
from data_structures import Grid

def main_compito1():
    """
    Script principale per dimostrare le funzionalita del Compito 1:
    - Generazione di una griglia basata su parametri forniti dall'utente.
    - Creazione della struttura dati logica (Grid con lista di adiacenze).
    - Stampa delle caratteristiche della griglia.
    - Visualizzazione grafica della mappa generata.
    """
    
    print("--- Progetto Algoritmi e Strutture Dati - Dimostrazione Compito 1 ---")
    print("Questo script si occupa della generazione di mappe a griglia con ostacoli.\n")

    # --- 1. IMPOSTAZIONE DEI PARAMETRI DELLA GRIGLIA TRAMITE INPUT UTENTE ---
    try:
        rows = int(input("Inserisci il numero di righe della griglia: "))
        cols = int(input("Inserisci il numero di colonne della griglia: "))
        
        obstacle_ratio_input = input("Inserisci la percentuale di ostacoli (default: 20): ") or "20"
        obstacle_ratio = int(obstacle_ratio_input) / 100.0
        
        if not (0 <= obstacle_ratio <= 1):
            print("Percentuale non valida. Verrà usato il 20%.")
            obstacle_ratio = 0.20

    except ValueError:
        print("Input non valido. Utilizzo valori di default (10x20, 20% ostacoli).")
        rows, cols, obstacle_ratio = 10, 20, 0.20

    # --- 2. GENERAZIONE DELLA GRIGLIA (CUORE DEL COMPITO 1) ---
    print("\nGenerazione della griglia in corso...")
    
    # a) Il generatore crea la rappresentazione a matrice
    grid_data_matrix = grid_generator.generate_grid_map(
        rows=rows, 
        cols=cols, 
        obstacle_ratio=obstacle_ratio
    )
    
    # b) La matrice viene usata per creare l'oggetto logico Grid.
    #    Questo dimostra che la base per i compiti futuri e gia pronta.
    grid_object = Grid.from_matrix(grid_data_matrix)
    
    print("Generazione completata.")

    # --- 3. STAMPA DELLE CARATTERISTICHE DELLA GRIGLIA ---
    # Usiamo una funzione helper per stampare le info dalla matrice originale
    # e aggiungiamo un'informazione derivata dal nostro oggetto Grid.
    
    num_obstacles = sum(row.count(1) for row in grid_data_matrix)
    total_cells = rows * cols
    actual_ratio = (num_obstacles / total_cells) * 100 if total_cells > 0 else 0

    print(f"\n--- Caratteristiche della Grid Map Generata ---")
    print(f"  Dimensioni: {rows} righe x {cols} colonne ({total_cells} celle totali)")
    print(f"  Ostacoli piazzati: {num_obstacles} (~{actual_ratio:.2f}%)")
    print(f"  Celle attraversabili (nodi del grafo): {len(grid_object.adj)}")
    print("-" * 45)
    
    # --- 4. VISUALIZZAZIONE GRAFICA ---
    print("\nVisualizzazione della mappa generata...")
    visualization.visualizza_gridmap_pcolormesh(grid_data_matrix)
    print("\nVisualizzazione mostrata. Programma terminato.")


if __name__ == "__main__":
    main_compito1()