import numpy as np
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch
from data_structures import Grid
from labeling import LabelManager
import closure_logic
import path_logic
import visualization

class PathfindingSolver:
    def __init__(self, grid_data, origin, destination):
        """
        Il costruttore inizializza il problema.
        """
        print("Inizializzazione del solver...")
        self.grid = Grid.from_matrix(grid_data)
        self.origin = origin
        self.destination = destination
        
        self.label_manager = LabelManager()
        self.memoization_cache = {}  
        self.lunghezza_minima = float('inf')
        self.sequenza_landmark = []

    def solve(self):
        """
        Avvia l'algoritmo ricorsivo CAMMINOMIN.
        """
        print(f"\n--- Esecuzione Procedura CAMMINOMIN da O={self.origin} a D={self.destination} ---")
        
        self.lunghezza_minima, self.sequenza_landmark = self.cammino_min_ricorsivo(
            self.origin, 
            self.destination, 
            frozenset(),
            depth=0
        )
        print("--- Esecuzione completata ---")

    def cammino_min_ricorsivo(self, current_origin, current_dest, forbidden_obstacles, depth=0):
        """
        Implementazione ricorsiva con stampe di debug dettagliate.
        """
        # --- BLOCCO DI DEBUG INIZIALE ---
        indent = "  " * depth
        print(f"\n{indent}╔══════════════════════════════════════════════════════")
        print(f"{indent}║ RICORSIONE (Livello {depth}): CAMMINOMIN({current_origin}, {current_dest})")
        print(f"{indent}║ Ostacoli Proibiti: {len(forbidden_obstacles)} elementi")
        
        # --- PASSO 1: GESTIONE DELLA CACHE (MEMOIZZAZIONE) ---
        cache_key = (current_origin, current_dest, forbidden_obstacles)
        if cache_key in self.memoization_cache:
            print(f"{indent}║ -> Trovato in CACHE. Ritorno il risultato salvato.")
            print(f"{indent}╚══════════════════════════════════════════════════════")
            return self.memoization_cache[cache_key]

        # --- PASSO 2: CASO BASE DELLA RICORSIONE ---
        if current_origin == current_dest:
            print(f"{indent}║ -> CASO BASE: Origine == Destinazione. Ritorno (0, [...]).")
            print(f"{indent}╚══════════════════════════════════════════════════════")
            return 0, [(current_origin, 1)]

        # --- PASSO 3: CALCOLO CHIUSURA E CASI BASE ---
        contesto, complemento = closure_logic.calcola_contesto_e_complemento(
            self.grid, current_origin, forbidden_obstacles
        )
        print(f"{indent}║ Chiusura calcolata: {len(contesto)} nel contesto, {len(complemento)} nel complemento.")

        if current_dest in set(contesto):
            dist = path_logic.calcola_distanza_libera(current_origin, current_dest)
            print(f"{indent}║ -> CASO BASE: Destinazione nel CONTESTO. Ritorno ({dist:.2f}, [...]).")
            print(f"{indent}╚══════════════════════════════════════════════════════")
            seq = [(current_origin, 0), (current_dest, 1)]
            self.memoization_cache[cache_key] = (dist, seq)
            return dist, seq
        
        if current_dest in set(complemento):
            dist = path_logic.calcola_distanza_libera(current_origin, current_dest)
            print(f"{indent}║ -> CASO BASE: Destinazione nel COMPLEMENTO. Ritorno ({dist:.2f}, [...]).")
            print(f"{indent}╚══════════════════════════════════════════════════════")
            seq = [(current_origin, 0), (current_dest, 2)]
            self.memoization_cache[cache_key] = (dist, seq)
            return dist, seq

        # --- PASSO 4: PASSO RICORSIVO ---
        frontiera = closure_logic.calcola_frontiera(
            self.grid, current_origin, contesto, complemento, forbidden_obstacles
        )
        print(f"{indent}║ Frontiera calcolata: {len(frontiera)} celle.")
        
        if not frontiera:
            print(f"{indent}║ -> VICOLO CIECO: Frontiera vuota. Ritorno (inf, []).")
            print(f"{indent}╚══════════════════════════════════════════════════════")
            return float('inf'), []

        best_len_locale, best_seq_locale = float('inf'), []
        frontiera.sort(key=lambda item: path_logic.calcola_distanza_libera(item[0], current_dest))
        
        print(f"{indent}║ Inizio ciclo FOR sulla frontiera...")
        for i, (f_pos, f_type) in enumerate(frontiera):
            len_of = path_logic.calcola_distanza_libera(current_origin, f_pos)
            
            print(f"{indent}║ ({i+1}/{len(frontiera)}) Esamino F={f_pos} (tipo {f_type}). Costo O->F: {len_of:.2f}")

            if len_of + path_logic.calcola_distanza_libera(f_pos, current_dest) >= best_len_locale:
                print(f"{indent}║   -> PRUNING: costo potenziale ({len_of + path_logic.calcola_distanza_libera(f_pos, current_dest):.2f}) >= miglior costo attuale ({best_len_locale:.2f})")
                continue
            
            current_closure = set(contesto) | set(complemento) | {current_origin}
            new_forbidden_obstacles = forbidden_obstacles.union(current_closure)
            
            len_fd, seq_fd = self.cammino_min_ricorsivo(
                f_pos, current_dest, new_forbidden_obstacles, depth + 1
            )
            
            if len_fd != float('inf'):
                total_len = len_of + len_fd
                print(f"{indent}║   -> Ritorno da ricorsione per F={f_pos}. Costo F->D: {len_fd:.2f}. Totale: {total_len:.2f}")
                if total_len < best_len_locale:
                    print(f"{indent}║   -> NUOVO MIGLIOR PERCORSO LOCALE TROVATO! (costo {total_len:.2f})")
                    best_len_locale = total_len
                    best_seq_locale = path_logic.compatta_sequenza(
                        [(current_origin, 0), (f_pos, f_type)], seq_fd
                    )
        
        # --- PASSO 5: SALVATAGGIO IN CACHE E RITORNO ---
        print(f"{indent}║ Fine ciclo FOR. Miglior risultato locale: ({best_len_locale if best_len_locale != float('inf') else 'inf'}, {len(best_seq_locale)} landmark).")
        print(f"{indent}║ Salvo in CACHE e ritorno.")
        print(f"{indent}╚══════════════════════════════════════════════════════")
        
        self.memoization_cache[cache_key] = (best_len_locale, best_seq_locale)
        return best_len_locale, best_seq_locale

    def display_results(self):
        if self.lunghezza_minima == float('inf'):
            print("\nRISULTATO: La destinazione D non è raggiungibile da O.")
            return

        print(f"\nRISULTATO:")
        print(f"  Lunghezza del cammino minimo: {self.lunghezza_minima:.4f}")
        
        for lm_coords, _ in self.sequenza_landmark:
             self.label_manager.get_label(lm_coords)
        
        output_str = "< "
        for lm_coords, tipo in self.sequenza_landmark:
            label = "O" if lm_coords == self.origin else "D" if lm_coords == self.destination else self.label_manager.get_label(lm_coords)
            output_str += f"({label}, {tipo}) "
        print(f"  Sequenza di landmark: {output_str.strip()}>")

    def visualize_initial_closure_and_frontier(self):
        """
        Visualizza la chiusura e la frontiera del problema INIZIALE (partendo da O).
        """
        contesto_O, complemento_O = closure_logic.calcola_contesto_e_complemento(self.grid, self.origin)
        frontiera_O_con_tipo = closure_logic.calcola_frontiera(self.grid, self.origin, contesto_O, complemento_O)
        
        CELL_CONTESTO, CELL_COMPLEMENTO, CELL_ORIGINE, CELL_FRONTIERA, CELL_DESTINAZIONE = 2, 3, 4, 5, 6
        
        valori_speciali = {}
        for r, c in contesto_O: valori_speciali[(r, c)] = CELL_CONTESTO
        for r, c in complemento_O: valori_speciali[(r, c)] = CELL_COMPLEMENTO
        for (r, c), _ in frontiera_O_con_tipo: valori_speciali[(r, c)] = CELL_FRONTIERA
        valori_speciali[self.origin] = CELL_ORIGINE
        valori_speciali[self.destination] = CELL_DESTINAZIONE
        
        vis_grid = self.grid.to_matrix(custom_values=valori_speciali)
        
        color_map = {0:'white', 1:'#30307A', 2:'#90EE90', 3:'#FFD700', 4:'#FF0000', 5:'#006400', 6:'#800080'}
        label_map = {0:'Spazio Libero', 1:'Ostacolo', 2:'Contesto', 3:'Complemento', 4:'Origine O', 5:'Frontiera', 6:'Destinazione D'}
        cmap = ListedColormap([color_map.get(i) for i in sorted(color_map.keys())])
        legend_patches = [Patch(facecolor=color, edgecolor='black', label=label_map[key]) for key, color in color_map.items()]
        titolo = f"Chiusura e Frontiera di O={self.origin}"
        
        visualization.visualizza_risultato_finale(vis_grid, cmap, legend_patches, titolo)