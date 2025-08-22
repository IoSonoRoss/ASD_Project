import math
import heapq
import numpy as np
import closure_logic
import path_logic

# Variabile globale per il debug della destinazione
D_globale = None
memoization_cache = {}

# La firma della funzione ora include 'stats_tracker'
def procedura_cammino_min(
    origin, destination, grid, label_manager, stats_tracker,
    ostacoli_proibiti=frozenset(), depth=0):
    """
    [Versione con Logging e StatsTracker] 
    Implementazione RICORSIVA che raccoglie dati per la sperimentazione.
    """
    # --- STATS: Traccia la profondità massima della ricorsione ---
    stats_tracker.track_depth(depth)

    # Il logging di debug rimane per l'analisi manuale
    indent = "  " * depth
    origin_label = "O" if depth == 0 else label_manager.get_label(origin)
    dest_label = "D" if destination == D_globale else label_manager.get_label(destination)
    print(f"{indent}--> Chiamata CAMMINOMIN(O={origin_label}, D={dest_label}) con {len(ostacoli_proibiti)} ostacoli proibiti")

    cache_key = (origin, destination, ostacoli_proibiti)
    if cache_key in memoization_cache:
        # ... (logica cache)
        return memoization_cache[cache_key]

    if origin == destination:
        return 0, [(origin, 1)]
    
    grid_temp = [row[:] for row in grid]
    for r, c in ostacoli_proibiti:
        if 0 <= r < len(grid_temp) and 0 <= c < len(grid_temp[0]):
            grid_temp[r][c] = 1
    
    contesto, complemento = closure_logic.calcola_contesto_e_complemento(grid_temp, origin)
    
    if destination in set(contesto):
        return path_logic.calcola_distanza_libera(origin, destination), [(origin, 0), (destination, 1)]
    if destination in set(complemento):
        return path_logic.calcola_distanza_libera(origin, destination), [(origin, 0), (destination, 2)]

    frontiera_con_tipo = closure_logic.calcola_frontiera(grid_temp, origin, contesto, complemento)
    
    # --- STATS: Aggiungi le nuove celle di frontiera scoperte al tracker ---
    stats_tracker.add_frontier_cells(frontiera_con_tipo)
    
    for (coords, _) in frontiera_con_tipo:
        label_manager.get_label(coords)

    if not frontiera_con_tipo:
        return float('inf'), []

    lunghezza_min, seq_min = float('inf'), []
    frontiera_con_tipo.sort(key=lambda x: path_logic.calcola_distanza_libera(x[0], destination))
    
    print(f"{indent}    Frontiera di {origin_label} trovata con {len(frontiera_con_tipo)} celle. Inizio ciclo for...")

    for F, tipo_F in frontiera_con_tipo:
        lOF = path_logic.calcola_distanza_libera(origin, F)
        costo_stimato_totale = lOF + path_logic.calcola_distanza_libera(F, destination)
        
        if costo_stimato_totale >= lunghezza_min:
            # --- STATS: Incrementa il contatore del pruning ---
            stats_tracker.increment_pruning_count()
            print(f"{indent}    - Scarto F={label_manager.get_label(F)}: stima ...") # La stampa rimane
            continue
        
        print(f"{indent}    - Provo F={label_manager.get_label(F)} ...")

        chiusura_attuale = set(contesto) | set(complemento) | {origin}
        nuovi_ostacoli_proibiti = ostacoli_proibiti.union(chiusura_attuale)
        
        # Passa lo stats_tracker alla chiamata ricorsiva
        lFD, seqFD = procedura_cammino_min(
            F, destination, grid, label_manager, stats_tracker,
            frozenset(nuovi_ostacoli_proibiti), depth + 1
        )
        
        if lFD == float('inf'):
            continue
        
        lTot = lOF + lFD
        if lTot < lunghezza_min:
            lunghezza_min = lTot
            seq_min = path_logic.compatta_sequenza([(origin, 0), (F, tipo_F)], seqFD)
            
    memoization_cache[cache_key] = (lunghezza_min, seq_min)
    return lunghezza_min, seq_min