import math
import heapq
import numpy as np
import closure_logic
import path_logic

# Variabile globale per il debug della destinazione
D_globale = None
memoization_cache = {}

def procedura_cammino_min_ricorsiva(
    origin, destination, grid, label_manager, stats_tracker,
    ostacoli_proibiti=frozenset(), depth=0):
    """
    [Versione Corretta con Chiave di Cache Robusta e Logging] 
    """
    # --- LOGGING: Inizio chiamata ---
    indent = "  " * depth
    origin_label = "O" if depth == 0 else label_manager.get_label(origin)
    dest_label = "D" if destination == D_globale else label_manager.get_label(destination)
    print(f"{indent}--> Chiamata CAMMINOMIN(O={origin_label}, D={dest_label}) con {len(ostacoli_proibiti)} ostacoli proibiti")

    # --- STATS: Traccia la profondità ---
    stats_tracker.track_depth(depth)

    # --- CORREZIONE CRITICA: Creazione di una chiave di cache canonica e ordinata ---
    ostacoli_ordinati_tuple = tuple(sorted(list(ostacoli_proibiti)))
    cache_key = (origin, destination, ostacoli_ordinati_tuple)
    # --- FINE CORREZIONE ---

    if cache_key in memoization_cache:
        lunghezza, _ = memoization_cache[cache_key]
        status = "Infinito" if lunghezza == float('inf') else f"{lunghezza:.2f}"
        print(f"{indent}<-- Trovato in cache! Risultato: {status}")
        return memoization_cache[cache_key]

    if origin == destination:
        print(f"{indent}<-- Caso Base: Origine == Destinazione. Ritorno (0, [destinazione])")
        return 0, [(origin, 1)]
    
    grid_temp = [row[:] for row in grid]
    for r, c in ostacoli_proibiti:
        if 0 <= r < len(grid_temp) and 0 <= c < len(grid_temp[0]):
            grid_temp[r][c] = 1
    
    contesto, complemento = closure_logic.calcola_contesto_e_complemento(grid_temp, origin)
    
    if destination in set(contesto):
        lunghezza = path_logic.calcola_distanza_libera(origin, destination)
        print(f"{indent}<-- Caso Base: {dest_label} nel Contesto di {origin_label}. Ritorno ({lunghezza:.2f}, ...)")
        result = lunghezza, [(origin, 0), (destination, 1)]
        memoization_cache[cache_key] = result
        return result
    if destination in set(complemento):
        lunghezza = path_logic.calcola_distanza_libera(origin, destination)
        print(f"{indent}<-- Caso Base: {dest_label} nel Complemento di {origin_label}. Ritorno ({lunghezza:.2f}, ...)")
        result = lunghezza, [(origin, 0), (destination, 2)]
        memoization_cache[cache_key] = result
        return result

    frontiera_con_tipo = closure_logic.calcola_frontiera(grid_temp, origin, contesto, complemento)
    
    # --- STATS: Aggiungi frontiere ---
    stats_tracker.add_frontier_cells(frontiera_con_tipo)
    
    for (coords, _) in frontiera_con_tipo:
        label_manager.get_label(coords)

    if not frontiera_con_tipo:
        print(f"{indent}<-- Vicolo Cieco: Frontiera di {origin_label} è vuota. Ritorno (inf, [])")
        memoization_cache[cache_key] = (float('inf'), [])
        return float('inf'), []

    lunghezza_min, seq_min = float('inf'), []
    frontiera_con_tipo.sort(key=lambda x: path_logic.calcola_distanza_libera(x[0], destination))
    
    print(f"{indent}    Frontiera di {origin_label} trovata con {len(frontiera_con_tipo)} celle. Inizio ciclo for...")

    for F, tipo_F in frontiera_con_tipo:
        lOF = path_logic.calcola_distanza_libera(origin, F)
        costo_stimato_totale = lOF + path_logic.calcola_distanza_libera(F, destination)
        
        if costo_stimato_totale >= lunghezza_min:
            # --- STATS: Incrementa pruning ---
            stats_tracker.increment_pruning_count()
            # ... (stampa di debug) ...
            continue
        
        # ... (stampa di debug) ...

        chiusura_attuale = set(contesto) | set(complemento) | {origin}
        nuovi_ostacoli_proibiti = ostacoli_proibiti.union(chiusura_attuale)
        
        # Passa lo stats_tracker alla chiamata ricorsiva
        lFD, seqFD = procedura_cammino_min_ricorsiva(
            F, destination, grid, label_manager, stats_tracker,
            frozenset(nuovi_ostacoli_proibiti), depth + 1
        )
        
        if lFD == float('inf'):
            continue
        
        lTot = lOF + lFD
        if lTot < lunghezza_min:
            lunghezza_min = lTot
            seq_min = path_logic.compatta_sequenza([(origin, 0), (F, tipo_F)], seqFD)
            
    # ... (stampa di debug finale) ...
    
    memoization_cache[cache_key] = (lunghezza_min, seq_min)
    return lunghezza_min, seq_min

def cammino_min_reale_astar(grid, start, end):
    """Algoritmo A* per trovare il cammino minimo reale."""

    num_rows, num_cols = len(grid), len(grid[0])
    neighbors = [((0, 1), 1), ((0, -1), 1), ((1, 0), 1), ((-1, 0), 1),
                 ((1, 1), math.sqrt(2)), ((1, -1), math.sqrt(2)),
                 ((-1, 1), math.sqrt(2)), ((-1, -1), math.sqrt(2))]
    def heuristic(a, b): return path_logic.calcola_distanza_libera(a, b)
    open_set = [(heuristic(start, end), start)]
    came_from, g_score = {}, {(r, c): float('inf') for r in range(num_rows) for c in range(num_cols)}
    g_score[start] = 0
    while open_set:
        _, current = heapq.heappop(open_set)
        if current == end:
            path = []
            while current in came_from: path.append(current); current = came_from[current]
            path.append(start)
            return g_score[end], path[::-1]
        for (dr, dc), cost in neighbors:
            neighbor = (current[0] + dr, current[1] + dc)
            r, c = neighbor
            if not (0 <= r < num_rows and 0 <= c < num_cols) or grid[r][c] == 1: continue
            tentative_g_score = g_score[current] + cost
            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor], g_score[neighbor] = current, tentative_g_score
                heapq.heappush(open_set, (g_score[neighbor] + heuristic(neighbor, end), neighbor))
    return float('inf'), []

def procedura_cammino_min_iterativa(origin, destination, grid, stats_tracker):
    """
    [Versione ITERATIVA con StatsTracker]
    Usata per gli esperimenti di scalabilità.
    """
    stats_tracker.start() # Avvia il cronometro
    
    contesto, complemento = closure_logic.calcola_contesto_e_complemento(grid, origin)
    
    if destination in set(contesto):
        stats_tracker.stop()
        return path_logic.calcola_distanza_libera(origin, destination), [(origin, 0), (destination, 1)]
    if destination in set(complemento):
        stats_tracker.stop()
        return path_logic.calcola_distanza_libera(origin, destination), [(origin, 0), (destination, 2)]

    frontiera_con_tipo = closure_logic.calcola_frontiera(grid, origin, contesto, complemento)
    stats_tracker.add_frontier_cells(frontiera_con_tipo) # Registra le frontiere

    if not frontiera_con_tipo:
        stats_tracker.stop()
        return float('inf'), []

    lunghezza_min, seq_min = float('inf'), []
    frontiera_con_tipo.sort(key=lambda x: path_logic.calcola_distanza_libera(x[0], destination))

    for F, tipo_F in frontiera_con_tipo:
        lF = path_logic.calcola_distanza_libera(origin, F)
        
        if lF + path_logic.calcola_distanza_libera(F, destination) >= lunghezza_min:
            stats_tracker.increment_pruning_count() # Registra lo scarto
            continue

        grid_mod = [row[:] for row in grid]
        chiusura_O = set(contesto) | set(complemento) | {origin}
        for r, c in chiusura_O:
            if (r, c) != F: grid_mod[r][c] = 1
        
        lFD, _ = cammino_min_reale_astar(grid_mod, F, destination)
        
        if lFD == float('inf'):
            continue
            
        lTot = lF + lFD
        if lTot < lunghezza_min:
            lunghezza_min = lTot
            seq_min = path_logic.compatta_sequenza([(origin, 0), (F, tipo_F)], (destination, 3))

    stats_tracker.stop() # Ferma il cronometro
    return lunghezza_min, seq_min