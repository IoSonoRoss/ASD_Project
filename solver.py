import numpy as np
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch
from data_structures import Grid
from labeling import LabelManager
import closure_logic
import path_logic
import search
import visualization # Assumiamo che la logica di plotting sia qui

class PathfindingSolver:
    def __init__(self, grid_data, origin, destination):
        """
        Il costruttore inizializza il problema.
        """
        print("Inizializzazione del solver...")
        self.grid = Grid(grid_data) # Crea l'oggetto Grid
        self.origin = origin
        self.destination = destination
        self.label_manager = LabelManager()
        
        # Attributi per i risultati
        self.lunghezza_minima = float('inf')
        self.sequenza_landmark = []
        
        # Calcoli preliminari sulla chiusura di O
        self.contesto_O, self.complemento_O = closure_logic.calcola_contesto_e_complemento(self.grid, self.origin)
        self.frontiera_O_con_tipo = closure_logic.calcola_frontiera(self.grid, self.origin, self.contesto_O, self.complemento_O)
        
        # 2. Popola la mappa delle etichette per la frontiera di O SUBITO
        self.frontiera_O_con_tipo.sort(key=lambda item: (item[0][0], item[0][1]))
        for (coords, _) in self.frontiera_O_con_tipo:
            self.label_manager.get_label(coords)

    def solve(self):
        """
        [Versione Iterativa Fedele allo Pseudocodice]
        Esegue l'algoritmo CAMMINOMIN e salva i risultati.
        """
        print(f"\n--- Esecuzione Procedura CAMMINOMIN da O={self.origin} a D={self.destination} ---")

        # Righe 3-8: Controlla i casi base (D nella chiusura di O)
        if self.destination in set(self.contesto_O):
            self.lunghezza_minima = path_logic.calcola_distanza_libera(self.origin, self.destination)
            self.sequenza_landmark = [(self.origin, 0), (self.destination, 1)]
            print("--- Esecuzione completata (D nel Contesto) ---")
            return

        if self.destination in set(self.complemento_O):
            self.lunghezza_minima = path_logic.calcola_distanza_libera(self.origin, self.destination)
            self.sequenza_landmark = [(self.origin, 0), (self.destination, 2)]
            print("--- Esecuzione completata (D nel Complemento) ---")
            return
            
        # Riga 10-11: Vicolo cieco
        if not self.frontiera_O_con_tipo:
            print("Vicolo cieco: la frontiera di O è vuota.")
            self.lunghezza_minima = float('inf')
            self.sequenza_landmark = []
            return

        # Righe 12-13: Inizializzazione
        lunghezza_min_locale, seq_min_locale = float('inf'), []
        
        # Ordina la frontiera per ottimizzare il pruning
        self.frontiera_O_con_tipo.sort(key=lambda x: path_logic.calcola_distanza_libera(x[0], self.destination))
        
        # Riga 14: Cicla sulla frontiera di O
        for F_pos, tipo_F in self.frontiera_O_con_tipo:
            lOF = path_logic.calcola_distanza_libera(self.origin, F_pos)

            # Riga 17 (Pruning)
            if lOF + path_logic.calcola_distanza_libera(F_pos, self.destination) >= lunghezza_min_locale:
                continue

            # Riga 18: CHIAMATA ad A* su una griglia modificata
            grid_data_mod = [row[:] for row in self.grid.data]
            chiusura_O = set(self.contesto_O) | set(self.complemento_O) | {self.origin}
            for r, c in chiusura_O:
                if (r, c) != F_pos: grid_data_mod[r][c] = 1
            grid_mod = Grid(grid_data_mod)
            
            lFD, _ = search.cammino_min_reale_astar(grid_mod, F_pos, self.destination)
            
            if lFD == float('inf'):
                continue
            
            # Righe 19-22: Aggiorna il percorso migliore
            lTot = lOF + lFD
            if lTot < lunghezza_min_locale:
                lunghezza_min_locale = lTot
                seq_min_locale = [(self.origin, 0), (F_pos, tipo_F), (self.destination, 3)]

        # Salva i risultati finali
        self.lunghezza_minima = lunghezza_min_locale
        self.sequenza_landmark = seq_min_locale
        print("--- Esecuzione completata ---")

    def display_results(self):
        """Stampa i risultati finali (lunghezza e sequenza)."""
        if self.lunghezza_minima == float('inf'):
            print("\nRISULTATO: La destinazione D non è raggiungibile da O.")
            return

        print(f"\nRISULTATO:")
        print(f"  Lunghezza del cammino minimo: {self.lunghezza_minima:.4f}")
        
        mappa_finale = self.label_manager.mappa_coord_etichetta
        
        output_str = "<"
        for i, (lm_coords, tipo) in enumerate(self.sequenza_landmark):
            label = "O" if lm_coords == self.origin else "D" if lm_coords == self.destination else mappa_finale.get(lm_coords, str(lm_coords))
            output_str += f"({label}, {tipo}) "
        print(f"  Sequenza di landmark: {output_str.strip()}>")
    
    def display_debug_info(self):
        """Stampa informazioni di debug come la mappa delle etichette."""
        print("\n--- DEBUG: Mappa Etichette Creata ---")
        mappa_finale = self.label_manager.mappa_coord_etichetta
        for coord, label in sorted(mappa_finale.items()):
            print(f"  {coord} -> '{label}'")
        print("---------------------------------------------")
        
    def visualize_closure_and_frontier(self):
        """Crea e mostra la visualizzazione della chiusura e frontiera di O."""
        vis_grid = np.array(self.grid.data, dtype=int)
        for r, c in self.contesto_O: vis_grid[r, c] = 2
        for r, c in self.complemento_O: vis_grid[r, c] = 3
        for (r, c), _ in self.frontiera_O_con_tipo: vis_grid[r, c] = 5
        vis_grid[self.origin[0], self.origin[1]] = 4
        vis_grid[self.destination[0], self.destination[1]] = 6

        color_map = {0:'white', 1:'#30307A', 2:'#90EE90', 3:'#FFD700', 4:'#FF0000', 5:'#006400', 6:'#800080'}
        label_map = {0:'Spazio Libero', 1:'Ostacolo', 2:'Contesto di O', 3:'Complemento di O', 4:'Origine O', 5:'Frontiera di O', 6:'Destinazione D'}
        cmap = ListedColormap([color_map.get(i) for i in sorted(color_map.keys())])
        legend_patches = [Patch(facecolor=color, edgecolor='black', label=label_map[key]) for key, color in color_map.items()]
        titolo = f"Chiusura e Frontiera di O={self.origin}"
        
        visualization.visualizza_risultato_finale(vis_grid, cmap, legend_patches, titolo)