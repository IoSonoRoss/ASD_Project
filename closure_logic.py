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

