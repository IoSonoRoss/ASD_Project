import math
import numpy as np
from data_structures import Grid

def is_path_free(grid: Grid, path, forbidden_obstacles=frozenset()):
    """
    [Versione Corretta]
    Verifica se un percorso e libero. Controlla solo le celle del percorso
    SUCCESSIVE alla prima, poiche la prima e l'origine del sottoproblema
    e si assume che sia valida.
    """
    if not path:
        return False
        
    # Un percorso con una sola cella (solo l'origine) e considerato valido.
    if len(path) < 2:
        return True

    # Itera sul percorso SALTANDO la prima cella (l'origine).
    for coords in path[1:]:
        if not grid.is_traversable(coords, forbidden_obstacles):
            return False
            
    return True

def generate_path_coordinates(origin, destination, diagonal_first):
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
    if not origin or not destination: return float('inf')
    delta_x = abs(origin[1] - destination[1])
    delta_y = abs(origin[0] - destination[0])
    delta_min, delta_max = min(delta_x, delta_y), max(delta_x, delta_y)
    return math.sqrt(2) * delta_min + (delta_max - delta_min)

def compatta_sequenza(seq1, seq2):
    if not isinstance(seq2, list) or not seq2: return seq1
    return seq1 + seq2[1:]