import path_utils_new as path_utils

class PathfindingSolver:
    def __init__(self, grid, origin, destination):
        """Il costruttore inizializza il problema con i dati essenziali."""
        self.grid = grid
        self.origin = origin
        self.destination = destination
        self.label_manager = path_utils.LabelManager()
        
        # Attributi per salvare i risultati
        self.lunghezza_minima = float('inf')
        self.sequenza_landmark = []

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
    # Qui dentro va la logica che era nel main per preparare vis_grid,
    # color_map, etc., e chiamare la funzione di plotting da visualization.py
        pass

    def visualize_solution(self):
    # Qui dentro va la logica per preparare e visualizzare il percorso finale
        pass