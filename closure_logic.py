import path_logic
from data_structures import Grid # Nuovo import

def calcola_contesto_e_complemento(grid: Grid, origin, forbidden_obstacles=frozenset()):
    """
    Calcola Contesto e Complemento usando la nuova Grid e gestendo gli ostacoli proibiti.
    """
    contesto, complemento = [], []
    
    # Iteriamo su tutte le celle attraversabili del grafo, non su una griglia rettangolare
    for destination in grid.adj.keys():
        if destination == origin:
            continue

        # Non serve più controllare se la destinazione è un ostacolo,
        # perché stiamo già iterando solo sulle celle valide.

        path_t1 = path_logic.generate_path_coordinates(origin, destination, True)
        if path_logic.is_path_free(grid, path_t1, forbidden_obstacles):
            contesto.append(destination)
        else:
            path_t2 = path_logic.generate_path_coordinates(origin, destination, False)
            # Aggiunto controllo per assicurarsi che il path_t2 sia valido
            if path_logic.is_path_free(grid, path_t2, forbidden_obstacles) and path_t1 != path_t2:
                complemento.append(destination)
                
    return contesto, complemento

def calcola_frontiera(grid: Grid, origin, contesto, complemento, forbidden_obstacles=frozenset()):
    """
    Calcola la frontiera usando la nuova Grid e gestendo gli ostacoli proibiti.
    """
    chiusura = set(contesto) | set(complemento) | {origin}
    contesto_set = set(contesto)
    frontiera_con_tipo = []
    
    for cell_in_chiusura in chiusura:
        # Usiamo get_neighbors() per trovare i vicini reali secondo il grafo
        # Questo è molto più elegante e corretto!
        for neighbor_pos in grid.get_neighbors(cell_in_chiusura):
            
            # La frontiera è una cella della chiusura adiacente a una cella libera FUORI dalla chiusura
            if neighbor_pos not in chiusura and grid.is_traversable(neighbor_pos, forbidden_obstacles):
                tipo = 1 if cell_in_chiusura in contesto_set else 2
                frontiera_con_tipo.append((cell_in_chiusura, tipo))
                break # Trovato un vicino esterno, passiamo alla prossima cella della chiusura
            
    return frontiera_con_tipo