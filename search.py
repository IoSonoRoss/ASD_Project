# File: search.py

import math
import heapq
import closure_logic
import path_logic
from data_structures import Grid, State, PriorityQueue # Nuovi import

# Variabile globale per il debug della destinazione
D_globale = None
memoization_cache = {}

# --- A* REFACTORED PER USARE LE NUOVE CLASSI ---
def cammino_min_reale_astar(grid: Grid, start_pos, end_pos):
    """
    [Versione Refactored] Algoritmo A* che usa State e PriorityQueue.
    """
    start_state = State(start_pos, g_cost=0.0)
    
    open_list = PriorityQueue()
    # La priorità è il f_score = g_score + h_score
    f_score_start = path_logic.calcola_distanza_libera(start_pos, end_pos)
    open_list.add(start_state, f_score_start)
    
    # La closed list ora contiene oggetti State, per ricostruire il percorso
    closed_set = set()

    neighbors_moves = [((0, 1), 1), ((0, -1), 1), ((1, 0), 1), ((-1, 0), 1),
                       ((1, 1), math.sqrt(2)), ((1, -1), math.sqrt(2)),
                       ((-1, 1), math.sqrt(2)), ((-1, -1), math.sqrt(2))]

    while not open_list.is_empty():
        current_state = open_list.pop()

        if current_state.position == end_pos:
            # Ricostruisci il percorso risalendo i parent
            path = []
            curr = current_state
            while curr:
                path.append(curr.position)
                curr = curr.parent
            return current_state.g_cost, path[::-1]

        closed_set.add(current_state)

        for (dr, dc), cost in neighbors_moves:
            neighbor_pos = (current_state.position[0] + dr, current_state.position[1] + dc)

            if not grid.is_within_bounds(neighbor_pos) or grid.is_obstacle(neighbor_pos):
                continue
            
            neighbor_state = State(neighbor_pos, parent=current_state, g_cost=current_state.g_cost + cost)

            if neighbor_state in closed_set:
                continue

            f_score = neighbor_state.g_cost + path_logic.calcola_distanza_libera(neighbor_pos, end_pos)
            open_list.add(neighbor_state, f_score)
            
    return float('inf'), []

# --- PROCEDURA CAMMINOMIN REFACTORED ---
def procedura_cammino_min_ricorsiva(origin_pos, destination_pos, original_grid: Grid, label_manager, stats_tracker, ostacoli_proibiti=frozenset(), depth=0):
    
    # ... (Stampa di debug iniziale, invariata) ...
    
    cache_key = (origin_pos, destination_pos, frozenset(sorted(list(ostacoli_proibiti))))
    if cache_key in memoization_cache:
        return memoization_cache[cache_key]

    if origin_pos == destination_pos:
        return 0, [(origin_pos, 1)]
    
    # Crea una griglia temporanea per questa chiamata
    # NOTA: Questo è il punto meno efficiente. Una soluzione avanzata
    # passerebbe solo il set di ostacoli e modificherebbe i metodi di Grid.
    # Per ora, questo è più semplice e robusto.
    grid_data_temp = [row[:] for row in original_grid.data]
    for r, c in ostacoli_proibiti:
        if 0 <= r < original_grid.rows and 0 <= c < original_grid.cols:
            grid_data_temp[r][c] = 1
    grid_temp = Grid(grid_data_temp)
    
    # Calcola chiusura e frontiera sulla griglia temporanea
    contesto, complemento = closure_logic.calcola_contesto_e_complemento(grid_temp, origin_pos)
    
    if destination_pos in set(contesto):
        result = path_logic.calcola_distanza_libera(origin_pos, destination_pos), [(origin_pos, 0), (destination_pos, 1)]
        memoization_cache[cache_key] = result
        return result
    if destination_pos in set(complemento):
        result = path_logic.calcola_distanza_libera(origin_pos, destination_pos), [(origin_pos, 0), (destination_pos, 2)]
        memoization_cache[cache_key] = result
        return result

    frontiera_con_tipo = closure_logic.calcola_frontiera(grid_temp, origin_pos, contesto, complemento)
    
    stats_tracker.add_frontier_cells(frontiera_con_tipo)
    for (coords, _) in frontiera_con_tipo: label_manager.get_label(coords)

    if not frontiera_con_tipo:
        return float('inf'), []

    lunghezza_min, seq_min = float('inf'), []
    frontiera_con_tipo.sort(key=lambda x: path_logic.calcola_distanza_libera(x[0], destination_pos))
    
    for F_pos, tipo_F in frontiera_con_tipo:
        lOF = path_logic.calcola_distanza_libera(origin_pos, F_pos)
        if lOF + path_logic.calcola_distanza_libera(F_pos, destination_pos) >= lunghezza_min:
            stats_tracker.increment_pruning_count()
            continue

        chiusura_attuale = set(contesto) | set(complemento) | {origin_pos}
        nuovi_ostacoli_proibiti = ostacoli_proibiti.union(chiusura_attuale)
        
        # CHIAMATA RICORSIVA
        # Ora, invece di passare una griglia modificata, passiamo la griglia originale
        # e un set aggiornato di ostacoli. Ma questo richiederebbe di modificare
        # tutte le funzioni. La nostra logica attuale di ricreare grid_temp è corretta.
        # Per la chiamata A* invece non serve ricorsione.
        
        # ERRORE LOGICO PRECEDENTE: `procedura_cammino_min` è per percorsi liberi.
        # Qui serve l'algoritmo A*.
        
        # Correzione: `procedura_cammino_min_iterativa` (che usa A*)
        # è più vicina allo pseudocodice.
        # Ma per mantenere la ricorsione, A* è solo per l'ultimo miglio.

        # --- Questo blocco è stato rimosso in favore di un approccio iterativo nel solver ---
        # Per ora lasciamo la versione ricorsiva, ma è inefficiente
        lFD, seqFD = procedura_cammino_min_ricorsiva(
            F_pos, destination_pos, original_grid, label_manager, stats_tracker,
            frozenset(nuovi_ostacoli_proibiti), depth + 1
        )
        
        if lFD == float('inf'): continue
        
        lTot = lOF + lFD
        if lTot < lunghezza_min:
            lunghezza_min = lTot
            seq_min = path_logic.compatta_sequenza([(origin_pos, 0), (F_pos, tipo_F)], seqFD)
            
    memoization_cache[cache_key] = (lunghezza_min, seq_min)
    return lunghezza_min, seq_min