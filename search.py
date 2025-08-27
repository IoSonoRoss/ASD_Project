# File: search.py

import math
import heapq
import closure_logic
import path_logic
from data_structures import Grid, State, PriorityQueue 

D_globale = None
memoization_cache = {}

def cammino_min_reale_astar(grid: Grid, start_pos, end_pos):
    """
    Algoritmo A* che usa State e PriorityQueue.
    """
    start_state = State(start_pos, g_cost=0.0)
    
    open_list = PriorityQueue()
    f_score_start = path_logic.calcola_distanza_libera(start_pos, end_pos)
    open_list.add(start_state, f_score_start)
    
    closed_set = set()

    neighbors_moves = [((0, 1), 1), ((0, -1), 1), ((1, 0), 1), ((-1, 0), 1),
                       ((1, 1), math.sqrt(2)), ((1, -1), math.sqrt(2)),
                       ((-1, 1), math.sqrt(2)), ((-1, -1), math.sqrt(2))]

    while not open_list.is_empty():
        current_state = open_list.pop()

        if current_state.position == end_pos:
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

def procedura_cammino_min_ricorsiva(origin_pos, destination_pos, original_grid: Grid, label_manager, stats_tracker, ostacoli_proibiti=frozenset(), depth=0):
    """
    Procedura ricorsiva per trovare il cammino minimo tra due posizioni su una griglia,
    tenendo conto degli ostacoli proibiti e utilizzando la memorizzazione per ottimizzare.
    """
    cache_key = (origin_pos, destination_pos, frozenset(sorted(list(ostacoli_proibiti))))
    if cache_key in memoization_cache:
        return memoization_cache[cache_key]

    if origin_pos == destination_pos:
        return 0, [(origin_pos, 1)]
   
    grid_data_temp = [row[:] for row in original_grid.data]
    for r, c in ostacoli_proibiti:
        if 0 <= r < original_grid.rows and 0 <= c < original_grid.cols:
            grid_data_temp[r][c] = 1
    grid_temp = Grid(grid_data_temp)
    
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
    for (coords, _) in frontiera_con_tipo:
        label_manager.get_label(coords)

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
        
        lFD, seqFD = procedura_cammino_min_ricorsiva(
            F_pos, destination_pos, original_grid, label_manager, stats_tracker,
            frozenset(nuovi_ostacoli_proibiti), depth + 1
        )
        
        if lFD == float('inf'):
            continue
        
        lTot = lOF + lFD
        if lTot < lunghezza_min:
            lunghezza_min = lTot
            seq_min = path_logic.compatta_sequenza([(origin_pos, 0), (F_pos, tipo_F)], seqFD)
            
    memoization_cache[cache_key] = (lunghezza_min, seq_min)
    return lunghezza_min, seq_min