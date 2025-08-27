import path_logic
from data_structures import Grid

def calcola_contesto_e_complemento(grid: Grid, origin, forbidden_obstacles=frozenset()):
    """
    Calcola Contesto e Complemento usando la nuova Grid e gestendo gli ostacoli proibiti.
    """
    contesto, complemento = [], []
    for destination in grid.adj.keys():
        if destination == origin:
            continue
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
    Calcola la frontiera escludendo esplicitamente l'origine del sottoproblema
    dall'essere una cella di frontiera.
    """
    chiusura = set(contesto) | set(complemento) | {origin}
    contesto_set = set(contesto)
    frontiera_con_tipo = []
    
    candidate_frontiera = set(contesto) | set(complemento)
    
    for cella_candidata in candidate_frontiera:
        for neighbor_pos in grid.get_neighbors(cella_candidata):
            if neighbor_pos not in chiusura and grid.is_traversable(neighbor_pos, forbidden_obstacles):
                tipo = 1 if cella_candidata in contesto_set else 2
                frontiera_con_tipo.append((cella_candidata, tipo))
                break 
                
    return frontiera_con_tipo