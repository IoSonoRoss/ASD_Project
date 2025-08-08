import random
import math
import heapq
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch

# ==============================================================================
# SEZIONE 1: FUNZIONI DI BASE E UTILITY
# ==============================================================================

def generate_grid_map(rows=10, cols=20, obstacle_ratio=0.15):
    """Genera una mappa a griglia con ostacoli casuali."""
    grid = [[0 for _ in range(cols)] for _ in range(rows)]
    num_obstacles = int(rows * cols * obstacle_ratio)
    placed_obstacles = 0
    while placed_obstacles < num_obstacles:
        r, c = random.randint(0, rows - 1), random.randint(0, cols - 1)
        if grid[r][c] == 0:
            grid[r][c] = 1
            placed_obstacles += 1
    return grid

def print_grid_info(grid):
    """Stampa le caratteristiche della griglia."""
    rows, cols = len(grid), len(grid[0])
    num_obstacles = sum(row.count(1) for row in grid)
    print(f"\n--- Caratteristiche della Grid Map ---")
    print(f"  Dimensioni: {rows} righe x {cols} colonne")
    print(f"  Ostacoli: {num_obstacles}")
    print("-" * 35)

# ==============================================================================
# SEZIONE 2: FUNZIONI PER CAMMINI LIBERI E DISTANZA LIBERA
# ==============================================================================

def is_path_free(grid, path):
    """
    Verifica se un dato percorso è "libero", cioè se nessuna delle sue celle
    (dalla seconda in poi) è un ostacolo (valore 1).
    La destinazione deve essere libera.
    
    :param grid: La mappa a griglia.
    :param path: Lista di tuple (riga, colonna) che rappresenta il percorso.
    :return: True se il percorso è libero, False altrimenti.
    """
    if not path:
        return False # Un percorso vuoto non è valido
        
    # Controlla ogni cella del percorso, a partire dalla seconda (l'origine è esclusa dai controlli)
    # fino alla destinazione inclusa.
    for riga, colonna in path[1:]:
        # Controlla se le coordinate sono valide per la griglia
        if not (0 <= riga < len(grid) and 0 <= colonna < len(grid[0])):
            return False # Il percorso esce dalla griglia
            
        if grid[riga][colonna] == 1:
            return False  # Trovato un ostacolo
            
    return True

def generate_path_coordinates(origin, destination, diagonal_first):
    """Genera la sequenza di coordinate per un percorso di Tipo 1 o Tipo 2."""
    path = [origin]
    r_curr, c_curr = origin
    r_dest, c_dest = destination
    delta_r, delta_c = r_dest - r_curr, c_dest - c_curr
    num_diag = min(abs(delta_r), abs(delta_c))
    num_rect = abs(abs(delta_r) - abs(delta_c))
    step_r, step_c = int(np.sign(delta_r)), int(np.sign(delta_c))
    
    if abs(delta_r) > abs(delta_c):
        rect_step_r, rect_step_c = step_r, 0
    else:
        rect_step_r, rect_step_c = 0, step_c
    
    def make_diag_moves():
        nonlocal r_curr, c_curr
        for _ in range(num_diag):
            r_curr += step_r; c_curr += step_c
            path.append((r_curr, c_curr))
    
    def make_rect_moves():
        nonlocal r_curr, c_curr
        for _ in range(num_rect):
            r_curr += rect_step_r; c_curr += rect_step_c
            path.append((r_curr, c_curr))
            
    if diagonal_first:
        make_diag_moves(); make_rect_moves()
    else:
        make_rect_moves(); make_diag_moves()
    return path

def calcola_distanza_libera(origin, destination):
    """Calcola la distanza libera (dlib) tra due celle O e D."""
    delta_x = abs(origin[1] - destination[1])
    delta_y = abs(origin[0] - destination[0])
    delta_min, delta_max = min(delta_x, delta_y), max(delta_x, delta_y)
    return math.sqrt(2) * delta_min + (delta_max - delta_min)

# ==============================================================================
# SEZIONE 3: FUNZIONI PER CHIUSURA E FRONTIERA
# ==============================================================================

def calcola_contesto_e_complemento(grid, origin):
    """
    Calcola il Contesto e il Complemento di O.
    - Contesto: raggiungibile con un cammino libero di Tipo 1.
    - Complemento: NON raggiungibile con T1, ma raggiungibile con T2.
    """
    num_rows, num_cols = len(grid), len(grid[0])
    contesto, complemento = [], []
    for r_dest in range(num_rows):
        for c_dest in range(num_cols):
            destination = (r_dest, c_dest)
            if destination == origin or grid[r_dest][c_dest] == 1:
                continue
            path_t1 = generate_path_coordinates(origin, destination, True)
            if is_path_free(grid, path_t1):
                contesto.append(destination)
            else:
                path_t2 = generate_path_coordinates(origin, destination, False)
                if is_path_free(grid, path_t2) and path_t1 != path_t2:
                    complemento.append(destination)
    return contesto, complemento

def calcola_frontiera(grid, origin, contesto, complemento):
    """
    [Versione Corretta] Calcola la frontiera di O e associa a ogni cella il suo tipo (1 o 2).
    Restituisce una lista di tuple: [( (r, c), tipo )].
    """
    chiusura = set(contesto) | set(complemento) | {origin}
    contesto_set = set(contesto)
    frontiera = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    for r, c in chiusura:
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]) and grid[nr][nc] == 0 and (nr, nc) not in chiusura:
                tipo = 1 if (r, c) in contesto_set else 2
                frontiera.append(((r, c), tipo))
                break
    return frontiera

# ==============================================================================
# SEZIONE 4: PROCEDURA CAMMINO MINIMO (TRADUZIONE PSEUDOCODICE)
# ==============================================================================

def cammino_min_reale_astar(grid, start, end):
    """
    Trova il cammino minimo reale (A*) da 'start' a 'end', aggirando gli ostacoli.
    Restituisce (lunghezza, percorso_in_coordinate).
    """
    num_rows, num_cols = len(grid), len(grid[0])
    neighbors = [((0, 1), 1),((0, -1), 1),((1, 0), 1),((-1, 0), 1),
                 ((1, 1), math.sqrt(2)),((1, -1), math.sqrt(2)),
                 ((-1, 1), math.sqrt(2)),((-1, -1), math.sqrt(2))]
    
    def heuristic(a, b):
        return calcola_distanza_libera(a,b)

    open_set = [(heuristic(start, end), start)]
    came_from, g_score = {}, { (r, c): float('inf') for r in range(num_rows) for c in range(num_cols) }
    g_score[start] = 0
    
    while open_set:
        _, current = heapq.heappop(open_set)
        if current == end:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return g_score[end], path[::-1]

        for (dr, dc), cost in neighbors:
            neighbor = (current[0] + dr, current[1] + dc)
            r, c = neighbor
            if not (0 <= r < num_rows and 0 <= c < num_cols) or grid[r][c] == 1: continue
            if dr != 0 and dc != 0 and (grid[current[0]][c] == 1 or grid[r][current[1]] == 1): continue
            
            tentative_g_score = g_score[current] + cost
            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor], g_score[neighbor] = current, tentative_g_score
                heapq.heappush(open_set, (g_score[neighbor] + heuristic(neighbor, end), neighbor))
                
    return float('inf'), []

def compatta_sequenza(seq1, seq2_landmark):
    """Accoda il landmark di destinazione del secondo percorso."""
    return seq1 + [seq2_landmark]

def procedura_cammino_min(origin, destination, grid):
    """
    [Versione Fedele] Implementazione ITERATIVA della procedura CAMMINOMIN.
    """
    # Righe 3-8: Controlla se D è nella chiusura di O (casi base)
    contesto, complemento = calcola_contesto_e_complemento(grid, origin)
    
    if destination in set(contesto):
        return calcola_distanza_libera(origin, destination), [(origin, 0), (destination, 1)]
    if destination in set(complemento):
        return calcola_distanza_libera(origin, destination), [(origin, 0), (destination, 2)]

    # Riga 9: Calcola la frontiera
    frontiera_con_tipo = calcola_frontiera(grid, origin, contesto, complemento)

    # Riga 10-11: Vicolo cieco
    if not frontiera_con_tipo: return float('inf'), []

    # Righe 12-13: Inizializzazione
    lunghezza_min, seq_min = float('inf'), []

    # Riga 14: Cicla su ogni cella F della frontiera
    for F, tipo_F in frontiera_con_tipo:
        lF = calcola_distanza_libera(origin, F)
        
        # Riga 17 (Pruning)
        if lF + calcola_distanza_libera(F, destination) >= lunghezza_min: continue

        # Riga 18: CHIAMATA ad A* su griglia modificata
        grid_mod = [row[:] for row in grid]
        chiusura_O = set(contesto) | set(complemento) | {origin}
        for r, c in chiusura_O:
            if (r, c) != F: grid_mod[r][c] = 1
        
        lFD, _ = cammino_min_reale_astar(grid_mod, F, destination)
        
        if lFD == float('inf'): continue
            
        # Righe 19-22: Aggiorna il percorso migliore
        lTot = lF + lFD
        if lTot < lunghezza_min:
            lunghezza_min = lTot
            seq_min = compatta_sequenza([(origin, 0), (F, tipo_F)], (destination, 3))

    # Riga 23: Ritorna il risultato finale
    return lunghezza_min, seq_min