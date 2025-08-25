import path_logic
from data_structures import Grid

def calcola_contesto_e_complemento(grid: Grid, origin, forbidden_obstacles=frozenset()):
    contesto, complemento = [], []
    for destination in grid.adj.keys():
        if destination == origin:
            continue
        # Passa forbidden_obstacles a is_path_free
        path_t1 = path_logic.generate_path_coordinates(origin, destination, True)
        if path_logic.is_path_free(grid, path_t1, forbidden_obstacles):
            contesto.append(destination)
        else:
            path_t2 = path_logic.generate_path_coordinates(origin, destination, False)
            if path_logic.is_path_free(grid, path_t2, forbidden_obstacles) and path_t1 != path_t2:
                complemento.append(destination)
    return contesto, complemento

def calcola_frontiera(grid: Grid, origin, contesto, complemento, forbidden_obstacles=frozenset()):
    """
    [Versione Corretta]
    Calcola la frontiera escludendo esplicitamente l'origine del sottoproblema
    dall'essere una cella di frontiera.
    """
    chiusura = set(contesto) | set(complemento) | {origin}
    contesto_set = set(contesto)
    frontiera_con_tipo = []
    
    # --- MODIFICA CHIAVE ---
    # Le uniche candidate per essere celle di frontiera sono quelle nel contesto e nel complemento,
    # MAI l'origine stessa.
    candidate_frontiera = set(contesto) | set(complemento)
    
    for cella_candidata in candidate_frontiera:
        # Per ogni candidato, controlliamo se ha almeno un vicino attraversabile FUORI dalla chiusura.
        for neighbor_pos in grid.get_neighbors(cella_candidata):
            if neighbor_pos not in chiusura and grid.is_traversable(neighbor_pos, forbidden_obstacles):
                # Trovato! Questa cella candidata è una cella di frontiera.
                tipo = 1 if cella_candidata in contesto_set else 2
                frontiera_con_tipo.append((cella_candidata, tipo))
                break # Passiamo al prossimo candidato, non serve controllare altri vicini.
                
    return frontiera_con_tipo