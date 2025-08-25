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
    Genera una lista di coordinate che rappresentano un percorso dalla origine alla destinazione
    su una griglia, muovendosi prima in diagonale o prima in modo rettilineo in base al flag.
    Args:
        origine (tuple[int, int]): La coordinata di partenza come (riga, colonna).
        destinazione (tuple[int, int]): La coordinata di arrivo come (riga, colonna).
        diagonale_prima (bool): Se True, i movimenti diagonali vengono fatti prima di quelli rettilinei.
                                Se False, i movimenti rettilinei vengono fatti prima di quelli diagonali.
    Returns:
        list[tuple[int, int]]: Una lista di coordinate che rappresentano il percorso da origine a destinazione.
    """

    percorso = [origine]
    r_corr, c_corr = origine
    r_dest, c_dest = destinazione
    delta_r, delta_c = r_dest - r_corr, c_dest - c_corr
    num_diag = min(abs(delta_r), abs(delta_c))
    num_rett = abs(abs(delta_r) - abs(delta_c))
    passo_r, passo_c = int(np.sign(delta_r)), int(np.sign(delta_c))
    
    if abs(delta_r) > abs(delta_c):
        rett_passo_r, rett_passo_c = passo_r, 0
    else:
        rett_passo_r, rett_passo_c = 0, passo_c
    
    def muovi_diagonale():
        """
            Definisce le mosse in direzione diagonale.
        """
        nonlocal r_corr, c_corr
        for _ in range(num_diag):
            r_corr += passo_r; c_corr += passo_c
            percorso.append((r_corr, c_corr))
    
    def muovi_rettilineo():
        """
            Definisce le mosse in direzione rettilinea.
        """
        nonlocal r_corr, c_corr
        for _ in range(num_rett):
            r_corr += rett_passo_r; c_corr += rett_passo_c
            percorso.append((r_corr, c_corr))
            
    if diagonale_prima:
        muovi_diagonale(); muovi_rettilineo()
    else:
        muovi_rettilineo(); muovi_diagonale()
    return percorso

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