import math
import heapq
import numpy as np
import closure_logic
import path_logic

# Variabile globale per il debug della destinazione
D_globale = None
memoization_cache = {}

def procedura_cammino_min(
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
            
    # ... (stampa di debug finale) ...
    
    memoization_cache[cache_key] = (lunghezza_min, seq_min)
    return lunghezza_min, seq_min