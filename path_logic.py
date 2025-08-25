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

def genera_coordinate_percorso(origine, destinazione, diagonale_prima):
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
    percorso = [origine]
    r_corr, c_corr = origine
    r_dest, c_dest = destinazione
    delta_r, delta_c = r_dest - r_corr, c_dest - c_corr
    num_diag = min(abs(delta_r), abs(delta_c))
    num_rect = abs(abs(delta_r) - abs(delta_c))
    passo_r, passo_c = int(np.sign(delta_r)), int(np.sign(delta_c))

    if abs(delta_r) > abs(delta_c):
        passo_rect_r, passo_rect_c = passo_r, 0
    else:
        passo_rect_r, passo_rect_c = 0, passo_c

    def mosse_diagonali():
        """
        Genera le mosse in diagonale.
        """
        nonlocal r_corr, c_corr
        for _ in range(num_diag):
            r_corr += passo_r
            c_corr += passo_c
            percorso.append((r_corr, c_corr))

    def mosse_rettilinee():
        """
        Genera le mosse rettilinee.
        """
        nonlocal r_corr, c_corr
        for _ in range(num_rect):
            r_corr += passo_rect_r
            c_corr += passo_rect_c
            percorso.append((r_corr, c_corr))

    if diagonale_prima:
        mosse_diagonali()
        mosse_rettilinee()
    else:
        mosse_rettilinee()
        mosse_diagonali()
    return percorso


def calcola_distanza_libera(origin, destination):
    """Calcola la distanza libera tra due punti su una griglia.
    Questa funzione determina la distanza più breve tra due punti, consentendo movimenti in otto direzioni (orizzontale, verticale e diagonale).
    Restituisce infinito se origin o destination non sono forniti.
    Argomenti:
        origin (tuple): Coordinate (riga, colonna) del punto di partenza.
        destination (tuple): Coordinate (riga, colonna) del punto di arrivo.
    Restituisce:
        float: Distanza octile tra origin e destination, oppure infinito se gli input non sono validi.
    """
    if not origin or not destination: return float('inf')
    delta_x = abs(origin[1] - destination[1])
    delta_y = abs(origin[0] - destination[0])
    delta_min, delta_max = min(delta_x, delta_y), max(delta_x, delta_y)
    return math.sqrt(2) * delta_min + (delta_max - delta_min)