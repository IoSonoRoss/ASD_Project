import path_utils_new as path_utils
import grid_utils_new as grid_utils
import numpy as np
from matplotlib.patches import Patch
from matplotlib.colors import ListedColormap

class PathfindingSolver:
    def __init__(self, grid, origin, destination):
        """Il costruttore inizializza il problema con i dati essenziali."""
        self.grid = grid
        self.origin = origin
        self.destination = destination
        self.label_manager = path_utils.LabelManager()
        
        # Attributi per i risultati, inizializzati a vuoto
        self.lunghezza_minima = float('inf')
        self.sequenza_landmark = []

        self.contesto_O, self.complemento_O = path_utils.calcola_contesto_e_complemento(self.grid, self.origin)
        self.frontiera_O_con_tipo = path_utils.calcola_frontiera(self.grid, self.origin, self.contesto_O, self.complemento_O)

    def solve(self):
        """
        Esegue la procedura CAMMINOMIN e salva i risultati.
        """
        print(f"\n--- Esecuzione Procedura CAMMINOMIN da O={self.origin} a D={self.destination} ---")
        
        # Pulisci la cache e chiama la procedura ricorsiva, passando il gestore
        path_utils.memoization_cache = {}
        self.lunghezza_minima, self.sequenza_landmark = path_utils.procedura_cammino_min(
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
        grid_utils.visualizza_risultato_finale(vis_grid, cmap, legend_patches, titolo)

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

    # FORSE SI PUÒ ELIMINARE
    def visualize_solution(self):
        """
        Crea e mostra la visualizzazione del percorso finale,
        evidenziando i landmark con le loro etichette.
        """
        if self.lunghezza_minima == float('inf'):
            print("Impossibile visualizzare la soluzione: nessun percorso trovato.")
            return

        print("\nGenerazione visualizzazione del percorso finale...")
        
        # --- 1. PREPARAZIONE DATI ---
        percorso_completo = path_utils.ricostruisci_percorso_da_landmark(self.sequenza_landmark, self.grid)
        mappa_finale_etichette = self.get_label_map()

        # Prepara la griglia di sfondo (solo con la chiusura di O)
        vis_grid_sfondo = np.array(self.grid, dtype=int)
        for r, c in self.contesto_O: vis_grid_sfondo[r, c] = 2
        for r, c in self.complemento_O: vis_grid_sfondo[r, c] = 3
        
        # --- 2. PREPARAZIONE ELEMENTI GRAFICI ---
        color_map = {
            0:'white', 
            1:'#30307A', 
            2:'#90EE90', 
            3:'#FFD700'
            }
        
        label_map = {
            0:'Spazio Libero', 
            1:'Ostacolo', 
            2:'Contesto di O (Sfondo)', 
            3:'Complemento di O (Sfondo)'
            }
        
        cmap = ListedColormap([color_map.get(i) for i in sorted(color_map.keys())])
        
        legend_patches = [Patch(facecolor=c, edgecolor='black', label=l) for l, c in label_map.items()]
        legend_patches.append(Patch(facecolor='red', edgecolor='black', label='Origine O'))
        legend_patches.append(Patch(facecolor='magenta', edgecolor='black', label='Destinazione D'))
        legend_patches.append(Patch(facecolor='#4682B4', edgecolor='black', label='Landmark di Frontiera'))
        
        titolo = f"Percorso Minimo Trovato (Lunghezza: {self.lunghezza_minima:.2f})"

        # --- 3. CHIAMATA ALLA FUNZIONE DI PLOTTING AVANZATA ---
        grid_utils.visualizza_percorso_avanzato(
            vis_grid=vis_grid_sfondo, cmap=cmap, legend_patches=legend_patches,
            origin=self.origin, destination=self.destination, 
            sequenza_landmark=self.sequenza_landmark, 
            percorso_ricostruito=percorso_completo, 
            mappa_etichette=mappa_finale_etichette,
            titolo=titolo
        )