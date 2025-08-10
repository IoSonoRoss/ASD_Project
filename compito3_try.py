# File: compito3_try.py (Versione Definitiva e Corretta)

from matplotlib import pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch
import numpy as np
import grid_utils_new
import path_utils_new

# Variabile globale per la mappatura, condivisa durante la ricorsione
mappa_etichette_globale = {}
etichette_disponibili = list("ABCEFGHIJKLMNPQRSTUVWXYZΣΔΦΓ&*%$#@")

def procedura_cammino_min_wrapper(origin, destination, grid):
    """
    Funzione wrapper per inizializzare e chiamare la procedura ricorsiva.
    """
    global mappa_etichette_globale, etichette_disponibili
    
    # Reset per ogni esecuzione
    mappa_etichette_globale = {}
    etichette_disponibili = list("ABCEFGHIJKLMNPQRSTUVWXYZΣΔΦΓ&*%$#@")
    path_utils_new.memoization_cache = {}

    # La prima chiamata ricorsiva parte qui
    return procedura_cammino_min_ricorsiva_con_mappatura(origin, destination, grid)

def procedura_cammino_min_ricorsiva_con_mappatura(origin, destination, grid, ostacoli_proibiti=frozenset()):
    # ... (Il corpo di questa funzione è la procedura ricorsiva che ti ho fornito prima)
    # ... (L'ho integrata qui per non creare un altro file)
    global mappa_etichette_globale, etichette_disponibili
    cache_key = (origin, destination, ostacoli_proibiti)
    if cache_key in path_utils_new.memoization_cache: return path_utils_new.memoization_cache[cache_key]
    if origin == destination: return 0, [(origin, 1)]
    grid_temp = [row[:] for row in grid]; 
    for r, c in ostacoli_proibiti: 
        if 0 <= r < len(grid_temp) and 0 <= c < len(grid_temp[0]): grid_temp[r][c] = 1
    contesto, complemento = path_utils_new.calcola_contesto_e_complemento(grid_temp, origin)
    if destination in set(contesto): return path_utils_new.calcola_distanza_libera(origin, destination), [(origin, 0), (destination, 1)]
    if destination in set(complemento): return path_utils_new.calcola_distanza_libera(origin, destination), [(origin, 0), (destination, 2)]
    
    frontiera_con_tipo = path_utils_new.calcola_frontiera(grid_temp, origin, contesto, complemento)
    
    # Assegna etichette a nuove celle di frontiera
    for (r, c), _ in frontiera_con_tipo:
        if (r,c) not in mappa_etichette_globale and etichette_disponibili:
            mappa_etichette_globale[(r,c)] = etichette_disponibili.pop(0)

    if not frontiera_con_tipo: return float('inf'), []
    
    lunghezza_min, seq_min = float('inf'), []
    frontiera_con_tipo.sort(key=lambda x: path_utils_new.calcola_distanza_libera(x[0], destination))
    
    for F, tipo_F in frontiera_con_tipo:
        lOF = path_utils_new.calcola_distanza_libera(origin, F)
        if lOF + path_utils_new.calcola_distanza_libera(F, destination) >= lunghezza_min: continue
        chiusura_attuale = set(contesto) | set(complemento) | {origin}
        nuovi_ostacoli_proibiti = ostacoli_proibiti.union(chiusura_attuale)
        lFD, seqFD = procedura_cammino_min_ricorsiva_con_mappatura(F, destination, grid, frozenset(nuovi_ostacoli_proibiti))
        if lFD == float('inf'): continue
        lTot = lOF + lFD
        if lTot < lunghezza_min:
            lunghezza_min = lTot
            seq_min = path_utils_new.compatta_sequenza([(origin, 0), (F, tipo_F)], seqFD)
            
    path_utils_new.memoization_cache[cache_key] = (lunghezza_min, seq_min)
    return lunghezza_min, seq_min

def main():
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
    O = (4, 6)
    D = (8, 19)
    print(f"Origine: {O}, Destinazione: {D}\n")

    # --- ESECUZIONE DI CAMMINOMIN ---
    print(f"--- Esecuzione Procedura CAMMINOMIN da O={O} a D={D} ---")
    
    # 1. Crea un gestore di etichette per questa esecuzione
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
        
        # 3. Ottieni la mappa finale dal gestore
        mappa_finale = label_manager.mappa_coord_etichetta
        
        # Stampa di debug
        print("\n--- DEBUG: Mappa Etichette Globale Creata ---")
        for coord, label in sorted(mappa_finale.items(), key=lambda item: item[1]):
            print(f"  '{label}' -> {coord}")
        print("---------------------------------------------")

        # 4. Stampa la sequenza di landmark usando la mappa
        output_str = "<"
        for i, (lm_coords, tipo) in enumerate(sequenza_landmark):
            label = "O" if lm_coords == O else "D" if lm_coords == D else mappa_finale.get(lm_coords, str(lm_coords))
            output_str += f"({label}, {tipo}) "
        print(f"\n  Sequenza di landmark: {output_str.strip()}>")

if __name__ == "__main__":
    main()