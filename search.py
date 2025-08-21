import math
import heapq
import numpy as np
import closure_logic
import path_logic

# Variabile globale per il debug della destinazione, da impostare nel main
D_globale = None

memoization_cache = {}

def procedura_cammino_min(origin, destination, grid, label_manager, ostacoli_proibiti=frozenset(), depth=0):
    """
    [Versione con Logging e Correzione Bug] 
    Implementazione RICORSIVA che passa la griglia modificata.
    """
    indent = "  " * depth
    origin_label = "O" if depth == 0 else label_manager.get_label(origin)
    dest_label = "D" if destination == D_globale else label_manager.get_label(destination)
    print(f"{indent}--> Chiamata CAMMINOMIN(O={origin_label}, D={dest_label}) con {len(ostacoli_proibiti)} ostacoli proibiti")

    cache_key = (origin, destination, ostacoli_proibiti)
    if cache_key in memoization_cache:
        lunghezza, _ = memoization_cache[cache_key]
        status = "Infinito" if lunghezza == float('inf') else f"{lunghezza:.2f}"
        print(f"{indent}<-- Trovato in cache! Risultato: {status}")
        return memoization_cache[cache_key]

    if origin == destination:
        print(f"{indent}<-- Caso Base: Origine == Destinazione. Ritorno (0, [destinazione])")
        return 0, [(origin, 1)]
    
    # Crea una griglia temporanea che include gli ostacoli proibiti
    grid_temp = [row[:] for row in grid]
    for r, c in ostacoli_proibiti:
        if 0 <= r < len(grid_temp) and 0 <= c < len(grid_temp[0]):
            grid_temp[r][c] = 1
    
    # Ora, tutte le funzioni lavorano sulla griglia corretta
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
        F_label = label_manager.get_label(F)
        lOF = path_logic.calcola_distanza_libera(origin, F)

        euristica_FD = path_logic.calcola_distanza_libera(F, destination)
        costo_stimato_totale = lOF + euristica_FD
        
        if costo_stimato_totale >= lunghezza_min:
            print(f"{indent}    - Scarto F={F_label}: costo stimato {costo_stimato_totale:.2f} (lOF {lOF:.2f} + euristica {euristica_FD:.2f}) >= min_attuale {lunghezza_min:.2f}")
            continue
        
        print(f"{indent}    - Provo F={F_label} (tipo {tipo_F}), costo O->F: {lOF:.2f}, stima totale: {costo_stimato_totale:.2f}")

        chiusura_attuale = set(contesto) | set(complemento) | {origin}
        nuovi_ostacoli_proibiti = ostacoli_proibiti.union(chiusura_attuale)
        
        lFD, seqFD = procedura_cammino_min(F, destination, grid, label_manager, frozenset(nuovi_ostacoli_proibiti), depth + 1)
        
        if lFD == float('inf'):
            print(f"{indent}      Risultato da F={F_label}: Vicolo cieco.")
            continue
        
        lTot = lOF + lFD
        print(f"{indent}      Risultato da F={F_label}: Trovato percorso reale di lunghezza totale {lTot:.2f}")
        if lTot < lunghezza_min:
            print(f"{indent}      !!! NUOVO MINIMO TROVATO: {lTot:.2f} (precedente: {lunghezza_min:.2f}) !!!")
            lunghezza_min = lTot
            seq_min = path_logic.compatta_sequenza([(origin, 0), (F, tipo_F)], seqFD)
            
    status_finale = "Infinito" if lunghezza_min == float('inf') else f"{lunghezza_min:.2f}"
    print(f"{indent}<-- Fine esplorazione per {origin_label}. Miglior risultato: {status_finale}")
    
    memoization_cache[cache_key] = (lunghezza_min, seq_min)
    return lunghezza_min, seq_min