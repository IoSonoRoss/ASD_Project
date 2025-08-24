import path_logic
from data_structures import Grid # Nuovo import

def calcola_contesto_e_complemento(grid: Grid, origin):
    """
    [Versione Refactored] Calcola Contesto e Complemento usando un oggetto Grid.
    """
    contesto, complemento = [], []
    for r_dest in range(grid.rows):
        for c_dest in range(grid.cols):
            destination = (r_dest, c_dest)
            
            # Usa i metodi della classe Grid
            if destination == origin or grid.is_obstacle(destination):
                continue

            path_t1 = path_logic.generate_path_coordinates(origin, destination, True)
            # Passa l'oggetto Grid alla funzione di validazione
            if path_logic.is_path_free(grid, path_t1):
                contesto.append(destination)
            else:
                path_t2 = path_logic.generate_path_coordinates(origin, destination, False)
                if path_logic.is_path_free(grid, path_t2) and path_t1 != path_t2:
                    complemento.append(destination)
                    
    return contesto, complemento

def calcola_frontiera(grid: Grid, origin, contesto, complemento):
    """
    [Versione Refactored] Calcola la frontiera usando un oggetto Grid.
    """
    chiusura = set(contesto) | set(complemento) | {origin}
    contesto_set = set(contesto)
    frontiera_con_tipo = []
    
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), 
                  (-1, -1), (-1, 1), (1, -1), (1, 1)]
    
    for r, c in chiusura:
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            neighbor_pos = (nr, nc)
            
            # Usa i metodi della classe Grid
            if grid.is_within_bounds(neighbor_pos):
                if not grid.is_obstacle(neighbor_pos) and neighbor_pos not in chiusura:
                    tipo = 1 if (r, c) in contesto_set else 2
                    frontiera_con_tipo.append(((r, c), tipo))
                    break 
            
    return frontiera_con_tipo