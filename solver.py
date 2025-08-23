import numpy as np
from matplotlib.patches import Patch
from matplotlib.colors import ListedColormap
import closure_logic
import path_logic
import search
import labeling
import visualization

class PathfindingSolver:
    def __init__(self, grid, origin, destination):
        """Il costruttore inizializza il problema con i dati essenziali."""
        self.grid = grid
        self.origin = origin
        self.destination = destination
        self.label_manager = labeling.LabelManager()
        
        # Attributi per i risultati, inizializzati a vuoto
        self.lunghezza_minima = float('inf')
        self.sequenza_landmark = []

        self.contesto_O, self.complemento_O = closure_logic.calcola_contesto_e_complemento(self.grid, self.origin)
        self.frontiera_O_con_tipo = closure_logic.calcola_frontiera(self.grid, self.origin, self.contesto_O, self.complemento_O)

    def solve(self):
        """
        Esegue la procedura CAMMINOMIN e salva i risultati.
        """
        print(f"\n--- Esecuzione Procedura CAMMINOMIN da O={self.origin} a D={self.destination} ---")
        
        # Pulisci la cache e chiama la procedura ricorsiva, passando il gestore
        search.memoization_cache = {}
        self.lunghezza_minima, self.sequenza_landmark = search.procedura_cammino_min_ricorsiva(
            self.origin, 
            self.destination, 
            self.grid, 
            self.label_manager
        )
        print("--- Esecuzione completata ---")

    def get_results(self):
        """Restituisce i risultati calcolati."""
        return self.lunghezza_minima, self.sequenza_landmark

    def get_label_map(self):
        """Restituisce la mappa completa delle etichette create durante la soluzione."""
        return self.label_manager.mappa_coord_etichetta
    
    def visualize_closure(self):
        vis_grid = np.array(self.grid, dtype=int)
        for r, c in self.contesto_O: 
            vis_grid[r, c] = 2
        for r, c in self.complemento_O: 
            vis_grid[r, c] = 3
        for (r, c), _ in self.frontiera_O_con_tipo: 
            vis_grid[r, c] = 5
        vis_grid[self.origin[0], self.origin[1]] = 4
        vis_grid[self.destination[0], self.destination[1]] = 6

        color_map = {
            0:'white', 
            1:'#30307A', 
            2:'#90EE90', 
            3:'#FFD700', 
            4:'#FF0000', 
            5:'#006400', 
            6:'#800080'}
        label_map = {
            0:'Spazio Libero', 
            1:'Ostacolo', 
            2:'Contesto di O', 
            3:'Complemento di O', 
            4:'Origine O', 
            5:'Frontiera di O', 
            6:'Destinazione D'
        }
        
        cmap = ListedColormap([color_map.get(i) for i in sorted(color_map.keys())])
        legend_patches = [Patch(facecolor=color, edgecolor='black', label=label_map[key]) for key, color in color_map.items()]
        titolo = f"Chiusura e Frontiera di O={self.origin}"
        visualization.visualizza_risultato_finale(vis_grid, cmap, legend_patches, titolo)

    def display_results(self):
        if self.lunghezza_minima == float('inf'):
            print("\nRISULTATO: La destinazione D non è raggiungibile da O.")
        else:
            print(f"\nRISULTATO:")
            print(f"  Lunghezza del cammino minimo: {self.lunghezza_minima:.4f}")

            mappa_finale = self.get_label_map()

            print("\n--- DEBUG: Mappa Etichette Globale Creata ---")
            for coord, label in sorted(mappa_finale.items()):
                print(f"  {coord} -> '{label}'")
            print("---------------------------------------------")

            output_str = "<"
            for i, (lm_coords, tipo) in enumerate(self.sequenza_landmark):
                label = "O" if lm_coords == self.origin else "D" if lm_coords == self.destination else mappa_finale.get(lm_coords, str(lm_coords))
                output_str += f"({label}, {tipo}) "
            print(f"\n  Sequenza di landmark: {output_str.strip()}>")