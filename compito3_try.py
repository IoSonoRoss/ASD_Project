# File: compito3_try.py

from matplotlib import pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch
import numpy as np
# --- IMPORT CORRETTI ---
import grid_utils_new
import path_utils_new 

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