import math
import numpy as np

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

def compatta_sequenza(seq1, seq2_landmark):
    """Accoda il landmark di destinazione del secondo percorso."""
    return seq1 + [seq2_landmark]