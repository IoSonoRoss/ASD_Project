import math
import heapq
import numpy as np

# Variabile globale per il debug della destinazione, da impostare nel main
D_globale = None

# ==============================================================================
# SEZIONE 1: FUNZIONI DI BASE
# ==============================================================================

def is_path_free(grid, path):
    """
    Versione SEMPLICE che lavora sulla griglia fornita.
    """
    if not path: return False
    for r, c in path[1:]:
        if not (0 <= r < len(grid) and 0 <= c < len(grid[0])): return False
        if grid[r][c] == 1: return False
    return True

def find_free_paths(grid, origin, destination):
    """
    Trova i cammini liberi tra un'origine e una destinazione.
    
    :return: Una lista di tuple. Ogni tupla è nella forma (tipo, percorso),
             dove tipo è una stringa ("Tipo 1" o "Tipo 2") e percorso è
             una lista di coordinate.
    """
    found_paths = [] # Nome cambiato per chiarezza
    
    if grid[destination[0]][destination[1]] == 1:
        return []

    # 1. Controlla il percorso di TIPO 1 (obliquo -> rettilineo)
    path_type1 = generate_path_coordinates(origin, destination, diagonal_first=True)
    if is_path_free(grid, path_type1):
        # Aggiungi una tupla con il tipo e il percorso
        found_paths.append(("Tipo 1", path_type1))
        
    # 2. Controlla il percorso di TIPO 2 (rettilineo -> obliquo)
    path_type2 = generate_path_coordinates(origin, destination, diagonal_first=False)
    
    # Se il percorso è una linea retta, Tipo 1 e Tipo 2 sono uguali.
    # In base alla regola, un percorso solo obliquo o solo rettilineo
    # è classificato come TIPO 1. Quindi non dobbiamo aggiungere un duplicato.
    if path_type1 == path_type2:
        return found_paths # Restituisce solo il risultato del Tipo 1
    
    # Se i percorsi sono diversi, controlla se il Tipo 2 è libero
    if is_path_free(grid, path_type2):
        # Aggiungi una tupla con il tipo e il percorso
        found_paths.append(("Tipo 2", path_type2))
        
    return found_paths

def generate_path_coordinates(origin, destination, diagonal_first):
    path = [origin]
    r_curr, c_curr = origin; r_dest, c_dest = destination
    delta_r, delta_c = r_dest - r_curr, c_dest - c_curr
    num_diag = min(abs(delta_r), abs(delta_c))
    num_rect = abs(abs(delta_r) - abs(delta_c))
    step_r, step_c = int(np.sign(delta_r)), int(np.sign(delta_c))
    if abs(delta_r) > abs(delta_c): rect_step_r, rect_step_c = step_r, 0
    else: rect_step_r, rect_step_c = 0, step_c
    def make_diag_moves():
        nonlocal r_curr, c_curr
        for _ in range(num_diag): r_curr += step_r; c_curr += step_c; path.append((r_curr, c_curr))
    def make_rect_moves():
        nonlocal r_curr, c_curr
        for _ in range(num_rect): r_curr += rect_step_r; c_curr += rect_step_c; path.append((r_curr, c_curr))
    if diagonal_first: make_diag_moves(); make_rect_moves()
    else: make_rect_moves(); make_diag_moves()
    return path

def calcola_distanza_libera(origin, destination):
    if not origin or not destination: return float('inf')
    delta_x = abs(origin[1] - destination[1])
    delta_y = abs(origin[0] - destination[0])
    delta_min, delta_max = min(delta_x, delta_y), max(delta_x, delta_y)
    return math.sqrt(2) * delta_min + (delta_max - delta_min)

# ==============================================================================
# SEZIONE 2: FUNZIONI PER CHIUSURA E FRONTIERA
# ==============================================================================

def calcola_contesto_e_complemento(grid, origin):
    num_rows, num_cols = len(grid), len(grid[0])
    contesto, complemento = [], []
    for r_dest in range(num_rows):
        for c_dest in range(num_cols):
            destination = (r_dest, c_dest)
            if destination == origin or grid[r_dest][c_dest] == 1: continue
            path_t1 = generate_path_coordinates(origin, destination, True)
            if is_path_free(grid, path_t1):
                contesto.append(destination)
            else:
                path_t2 = generate_path_coordinates(origin, destination, False)
                if is_path_free(grid, path_t2) and path_t1 != path_t2: complemento.append(destination)
    return contesto, complemento

def calcola_frontiera(grid, origin, contesto, complemento):
    chiusura = set(contesto) | set(complemento) | {origin}
    contesto_set = set(contesto)
    frontiera_con_tipo = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    for r, c in chiusura:
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]):
                if grid[nr][nc] == 0 and (nr, nc) not in chiusura:
                    tipo = 1 if (r, c) in contesto_set else 2
                    frontiera_con_tipo.append(((r, c), tipo))
                    break
    return frontiera_con_tipo

def compatta_sequenza(seq1, seq2):
    if not isinstance(seq2, list) or not seq2: return seq1
    return seq1 + seq2[1:]

# ==============================================================================
# SEZIONE 3: PROCEDURA CAMMINOMIN
# ==============================================================================

class LabelManager:
    def __init__(self):
        self.mappa_coord_etichetta = {}
        self.prossimo_indice = 0
        self.alfabeto = "ABCEFGHIJKLMNPQRSTUVWXYZΣΔΦΓ&*%$#@"
    def _indice_a_etichetta(self, n):
        if n < 0: return ""
        base = len(self.alfabeto)
        if n < base: return self.alfabeto[n]
        else: return self._indice_a_etichetta(n // base - 1) + self.alfabeto[n % base]
    def get_label(self, coords):
        if coords not in self.mappa_coord_etichetta:
            nuova_etichetta = self._indice_a_etichetta(self.prossimo_indice)
            self.mappa_coord_etichetta[coords] = nuova_etichetta
            self.prossimo_indice += 1
        return self.mappa_coord_etichetta[coords]

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
    contesto, complemento = calcola_contesto_e_complemento(grid_temp, origin)
    
    if destination in set(contesto):
        lunghezza = calcola_distanza_libera(origin, destination)
        print(f"{indent}<-- Caso Base: {dest_label} nel Contesto di {origin_label}. Ritorno ({lunghezza:.2f}, ...)")
        result = lunghezza, [(origin, 0), (destination, 1)]
        memoization_cache[cache_key] = result
        return result
    if destination in set(complemento):
        lunghezza = calcola_distanza_libera(origin, destination)
        print(f"{indent}<-- Caso Base: {dest_label} nel Complemento di {origin_label}. Ritorno ({lunghezza:.2f}, ...)")
        result = lunghezza, [(origin, 0), (destination, 2)]
        memoization_cache[cache_key] = result
        return result

    frontiera_con_tipo = calcola_frontiera(grid_temp, origin, contesto, complemento)
    
    for (coords, _) in frontiera_con_tipo:
        label_manager.get_label(coords)

    if not frontiera_con_tipo:
        print(f"{indent}<-- Vicolo Cieco: Frontiera di {origin_label} è vuota. Ritorno (inf, [])")
        memoization_cache[cache_key] = (float('inf'), [])
        return float('inf'), []

    lunghezza_min, seq_min = float('inf'), []
    frontiera_con_tipo.sort(key=lambda x: calcola_distanza_libera(x[0], destination))
    
    print(f"{indent}    Frontiera di {origin_label} trovata con {len(frontiera_con_tipo)} celle. Inizio ciclo for...")

    for F, tipo_F in frontiera_con_tipo:
        F_label = label_manager.get_label(F)
        lOF = calcola_distanza_libera(origin, F)
        
        euristica_FD = calcola_distanza_libera(F, destination)
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
            seq_min = compatta_sequenza([(origin, 0), (F, tipo_F)], seqFD)
            
    status_finale = "Infinito" if lunghezza_min == float('inf') else f"{lunghezza_min:.2f}"
    print(f"{indent}<-- Fine esplorazione per {origin_label}. Miglior risultato: {status_finale}")
    
    memoization_cache[cache_key] = (lunghezza_min, seq_min)
    return lunghezza_min, seq_min

# --- vedere se servono o meno ---

def generate_ideal_minimum_path(origin, destination):
    """
    Genera le coordinate del "cammino minimo ideale" (il percorso giallo),
    che è un percorso di Tipo 1 (prima tutte le mosse diagonali, poi quelle rettilinee).
    Questa funzione è essenzialmente la stessa di 'generate_path_coordinates'
    con diagonal_first=True.

    :param origin: Tupla (r, c) di partenza.
    :param destination: Tupla (r, c) di arrivo.
    :return: Lista di tuple (r, c) che rappresenta il cammino ideale.
    """
    path = [origin]
    r_curr, c_curr = origin
    r_dest, c_dest = destination

    delta_r = r_dest - r_curr
    delta_c = c_dest - c_curr

    # Calcola il numero di passi diagonali e rettilinei necessari
    num_diagonal_steps = min(abs(delta_r), abs(delta_c))
    num_rectilinear_steps = abs(abs(delta_r) - abs(delta_c))
    
    # Determina la direzione dei passi (-1, 0, o 1)
    step_r = int(np.sign(delta_r))
    step_c = int(np.sign(delta_c))
    
    # Determina la direzione del tratto rettilineo
    if abs(delta_r) > abs(delta_c):
        rect_step_r, rect_step_c = step_r, 0 # Movimento verticale
    else:
        rect_step_r, rect_step_c = 0, step_c # Movimento orizzontale

    # 1. Esegui i passi diagonali
    for _ in range(num_diagonal_steps):
        r_curr += step_r
        c_curr += step_c
        path.append((r_curr, c_curr))

    # 2. Esegui i passi rettilinei
    for _ in range(num_rectilinear_steps):
        r_curr += rect_step_r
        c_curr += rect_step_c
        path.append((r_curr, c_curr))
        
    return path

def cammino_min_reale(grid, start, end):
    """
    Trova il cammino minimo reale da 'start' a 'end' usando A*,
    aggirando gli ostacoli.
    Restituisce (lunghezza, percorso_in_coordinate).
    """
    num_rows, num_cols = len(grid), len(grid[0])
    
    neighbors = [((0, 1), 1),((0, -1), 1),((1, 0), 1),((-1, 0), 1),
                 ((1, 1), math.sqrt(2)),((1, -1), math.sqrt(2)),
                 ((-1, 1), math.sqrt(2)),((-1, -1), math.sqrt(2))]

    def heuristic(a, b):
        dr, dc = abs(a[0] - b[0]), abs(a[1] - b[1])
        return math.sqrt(2) * min(dr, dc) + (max(dr, dc) - min(dr, dc))

    open_set = [(heuristic(start, end), start)]
    came_from = {}
    g_score = { (r, c): float('inf') for r in range(num_rows) for c in range(num_cols) }
    g_score[start] = 0
    
    while open_set:
        _, current = heapq.heappop(open_set)
        
        if current == end:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return g_score[end], path[::-1] # Restituisce costo e percorso

        for (dr, dc), cost in neighbors:
            neighbor = (current[0] + dr, current[1] + dc)
            r, c = neighbor
            
            if not (0 <= r < num_rows and 0 <= c < num_cols) or grid[r][c] == 1:
                continue
            
            # Corner check per A* (coerenza con is_path_free)
            if dr != 0 and dc != 0: # Mossa diagonale
                if grid[current[0]][neighbor[1]] == 1 and grid[neighbor[0]][current[1]] == 1:
                    continue

            tentative_g_score = g_score[current] + cost
            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score = tentative_g_score + heuristic(neighbor, end)
                heapq.heappush(open_set, (f_score, neighbor))
                
    return float('inf'), [] # Nessun percorso trovato