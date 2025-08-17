import path_logic

def calcola_contesto_e_complemento(grid, origin):
    """
    Calcola il Contesto e il Complemento di O.
    - Contesto: raggiungibile con un cammino libero di Tipo 1.
    - Complemento: NON raggiungibile con T1, ma raggiungibile con T2.
    """
    num_rows, num_cols = len(grid), len(grid[0])
    contesto, complemento = [], []
    for r_dest in range(num_rows):
        for c_dest in range(num_cols):
            destination = (r_dest, c_dest)
            if destination == origin or grid[r_dest][c_dest] == 1:
                continue
            path_t1 = path_logic.generate_path_coordinates(origin, destination, True)
            if path_logic.is_path_free(grid, path_t1):
                contesto.append(destination)
            else:
                path_t2 = path_logic.generate_path_coordinates(origin, destination, False)
                if path_logic.is_path_free(grid, path_t2) and path_t1 != path_t2:
                    complemento.append(destination)
    return contesto, complemento

def calcola_frontiera(grid, origin, contesto, complemento):
    """
    [Versione Definitiva] Calcola la frontiera di O e associa a ogni cella 
    il suo tipo (1 per contesto, 2 per complemento).
    Restituisce una lista di tuple nel formato: [ ((riga, colonna), tipo) ].
    """
    chiusura = set(contesto) | set(complemento) | {origin}
    contesto_set = set(contesto)
    frontiera_con_tipo = []
    
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), 
                  (-1, -1), (-1, 1), (1, -1), (1, 1)]
    
    for r, c in chiusura:
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            
            if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]):
                neighbor_pos = (nr, nc)
                if grid[nr][nc] == 0 and neighbor_pos not in chiusura:
                    
                    # Determina il tipo della cella di frontiera (r,c)
                    tipo = 1 if (r, c) in contesto_set else 2
                    
                    # Aggiungi la tupla nel formato corretto ((r,c), tipo)
                    frontiera_con_tipo.append( ((r, c), tipo) )
                    
                    break 
            
    return frontiera_con_tipo