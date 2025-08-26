import math
import numpy as np
from data_structures import Grid

def is_path_free(grid: Grid, path, forbidden_obstacles=frozenset()):
    """
    Verifica se un percorso e libero. Controlla solo le celle del percorso
    SUCCESSIVE alla prima, poiche la prima e l'origine del sottoproblema
    e si assume che sia valida.
    """
    if not path:
        return False
        
    if len(path) < 2:
        return True

    for coords in path[1:]:
        if not grid.is_traversable(coords, forbidden_obstacles):
            return False
            
    return True

def generate_path_coordinates(origin, destination, diagonal_first):
    """
    Genera una lista di coordinate che rappresentano un percorso dalla cella origine alla destinazione su una griglia.
    Il percorso consiste in mosse diagonali e rettilinee (orizzontali/verticali), con la possibilità di dare priorità alle mosse diagonali.
    Args:
        origine (tuple[int, int]): La coordinata di partenza come (riga, colonna).
        destinazione (tuple[int, int]): La coordinata di arrivo come (riga, colonna).
        diagonale_prima (bool): Se True, le mosse diagonali vengono effettuate prima di quelle rettilinee; altrimenti il contrario.
    Returns:
        list[tuple[int, int]]: Una lista di coordinate che rappresentano il percorso da origine a destinazione, inclusi gli estremi.
    """
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
        """
        Genera le mosse in diagonale.
        """
        nonlocal r_curr, c_curr
        for _ in range(num_diag):
            r_curr += step_r; c_curr += step_c
            path.append((r_curr, c_curr))

    def make_rect_moves():
        """
        Genera le mosse rettilinee.
        """
        nonlocal r_curr, c_curr
        for _ in range(num_rect):
            r_curr += rect_step_r; c_curr += rect_step_c
            path.append((r_curr, c_curr))

    if diagonal_first:
        make_diag_moves()
        make_rect_moves()
    else:
        make_rect_moves()
        make_diag_moves()
    return path

def calcola_distanza_libera(origine, destinazione):
    """
    Calcola la distanza libera tra due coordinate su una griglia, considerando movimenti diagonali e rettilinei.
    Args:
        origine (tuple[int, int]): La coordinata di partenza come (riga, colonna).
        destinazione (tuple[int, int]): La coordinata di arrivo come (riga, colonna).
    Returns:
        float: La distanza minima considerando movimenti diagonali e rettilinei.
    """
    if not origine or not destinazione:
        return float('inf')
    delta_r = abs(origine[0] - destinazione[0])
    delta_c = abs(origine[1] - destinazione[1])
    delta_min, delta_max = min(delta_r, delta_c), max(delta_r, delta_c)
    return math.sqrt(2) * delta_min + (delta_max - delta_min)

def compatta_sequenza(seq1, seq2):
    """
    Compattta due sequenze di coordinate, evitando la duplicazione del punto di giunzione.
    Args:
        seq1 (list[tuple[int, int]]): Prima sequenza di coordinate.
        seq2 (list[tuple[int, int]]): Seconda sequenza di coordinate.
    Returns:
        list[tuple[int, int]]: Sequenza compatta risultante dalla concatenazione.
    """
    if not isinstance(seq2, list) or not seq2:
        return seq1
    return seq1 + seq2[1:]