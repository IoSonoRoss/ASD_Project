import random
import math
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap
import heapq

def generate_grid_map(rows=10, cols=10, num_obstacles=None, obstacle_ratio=0.2):
    """
    Genera una mappa a griglia (matrice) con ostacoli casuali.
    :param rows: Numero di righe nella griglia.
    :param cols: Numero di colonne nella griglia.
    :param num_obstacles: Numero di celle ostacolo (se None, usa obstacle_ratio).
    :param obstacle_ratio: Percentuale predefinita di ostacoli se num_obstacles non è specificato.
    :return: Lista 2D che rappresenta la griglia (0: vuoto, 1: ostacolo).
    """
    grid = [[0 for _ in range(cols)] for _ in range(rows)]
    total_cells = rows * cols
    if num_obstacles is None:
        num_obstacles = int(obstacle_ratio * total_cells)
    placed = 0
    while placed < num_obstacles:
        x, y = random.randint(0, rows - 1), random.randint(0, cols - 1)
        if grid[x][y] == 0:
            grid[x][y] = 1
            placed += 1
    return grid

def print_grid(grid):
    """
    Stampa la mappa a griglia e le sue caratteristiche.
    """
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    total_cells = rows * cols
    num_obstacles = sum(cell for row in grid for cell in row)
    print(f"\nCaratteristiche della grid map:")
    print(f"  Righe: {rows}")
    print(f"  Colonne: {cols}")
    print(f"  Celle totali: {total_cells}")
    print(f"  Numero di ostacoli: {num_obstacles}")
    print("Grid map:")
    for row in grid:
        print(' '.join(str(cell) for cell in row))
    print()

def is_within_bounds(x, y, grid):
    """
    Verifica se la posizione (x, y) è dentro i limiti della gridmap.
    """
    return 0 <= x < len(grid) and 0 <= y < len(grid[0])

def is_obstacle(x, y, grid):
    """
    Verifica se la cella (x, y) non è un ostacolo.
    """
    return grid[x][y] == 0

def move(x, y, direction, grid):
    """
    Muove la posizione (x, y) in una direzione specificata se possibile.
    :param x: Coordinata x corrente.
    :param y: Coordinata y corrente.
    :param direction: Direzione in cui muoversi ('N', 'S', 'E', 'O', 'NE', 'NO', 'SE', 'SO').
    :param grid: La griglia su cui muoversi.
    :return: (nuova_x, nuova_y, costo) o None se il movimento non è possibile.
    """
    directions = {
        'N':  (-1,  0, 1),
        'S':  ( 1,  0, 1),
        'E':  ( 0,  1, 1),
        'O':  ( 0, -1, 1),
        'NE': (-1,  1, math.sqrt(2)),
        'NO': (-1, -1, math.sqrt(2)),
        'SE': ( 1,  1, math.sqrt(2)),
        'SO': ( 1, -1, math.sqrt(2)),
    }

    if direction not in directions:
        return None
    
    dx, dy, cost = directions[direction]
    new_x, new_y = x + dx, y + dy
    
    if is_within_bounds(new_x, new_y, grid) and is_obstacle(new_x, new_y, grid):
        return (new_x, new_y, cost)
    return None

def visualizza_gridmap_pcolormesh(grid):
    np_grid = np.array(grid)
    rows, cols = np_grid.shape

    cmap = ListedColormap(['white', '#333399']) # Un blu facile da vedere
    fig, ax = plt.subplots()

    # La logica corretta per pcolormesh
    x_coords = np.arange(cols + 1)
    y_coords = np.arange(rows + 1)
    ax.pcolormesh(x_coords, y_coords, np_grid, cmap=cmap, edgecolors='black', linewidth=1)

    ax.set_title("Test di Isolamento: Dovresti vedere TUTTI i bordi")
    ax.set_aspect('equal')
    ax.invert_yaxis()
    ax.axis('off') # Rimuoviamo gli assi per chiarezza

    plt.show()

def definisci_quadranti(grid, start_pos):
    """
    Data una griglia e un punto di origine, classifica tutti gli ostacoli (valore 1)
    nei quattro quadranti standard. Gli ostacoli sugli assi non appartengono a nessun quadrante.

    Convenzione dei quadranti (come da immagine):
    - I  : in alto a destra
    - II : in alto a sinistra
    - III: in basso a sinistra
    - IV : in basso a destra

    :param grid: La griglia 2D (lista di liste o array NumPy).
    :param start_pos: Una tupla (start_row, start_col) per le coordinate dell'origine.
    :return: 4 liste, una per ogni quadrante, contenenti le coordinate (row, col) degli ostacoli.
    """
    start_row, start_col = start_pos
    num_rows = len(grid)
    num_cols = len(grid[0])

    # Liste per contenere le coordinate degli ostacoli in ogni quadrante
    primo_quadrante = []   
    secondo_quadrante = [] 
    terzo_quadrante = []   
    quarto_quadrante = []  

    # Scansiona ogni cella della griglia
    for row in range(num_rows):
        for col in range(num_cols):
                # Confronta le coordinate con quelle dell'origine
                
                # Quadrante I (in alto a destra)
                if row < start_row and col > start_col:
                    primo_quadrante.append((row, col))
                    
                # Quadrante II (in alto a sinistra)
                elif row < start_row and col < start_col:
                    secondo_quadrante.append((row, col))
                    
                # Quadrante III (in basso a sinistra)
                elif row > start_row and col < start_col:
                    terzo_quadrante.append((row, col))
                    
                # Quadrante IV (in basso a destra)
                elif row > start_row and col > start_col:
                    quarto_quadrante.append((row, col))
    
    return primo_quadrante, secondo_quadrante, terzo_quadrante, quarto_quadrante

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
    """
    Genera la sequenza di coordinate per un percorso "a L" (obliquo + rettilineo).
    
    :param origin: Tupla (r, c) di partenza.
    :param destination: Tupla (r, c) di arrivo.
    :param diagonal_first: Booleano. True per percorso di Tipo 1 (obliquo->rettilineo),
                           False per Tipo 2 (rettilineo->obliquo).
    :return: Lista di tuple (r, c) che rappresenta il percorso.
    """
    path = [origin]
    r_curr, c_curr = origin
    r_dest, c_dest = destination

    delta_r = r_dest - r_curr
    delta_c = c_dest - c_curr

    # Calcola il numero di passi diagonali e rettilinei necessari
    num_diagonal_steps = min(abs(delta_r), abs(delta_c))
    num_rectilinear_steps = abs(abs(delta_r) - abs(delta_c))
    
    # Determina la direzione dei passi (-1, 0, o 1)
    step_r = int(np.sign(delta_r))
    step_c = int(np.sign(delta_c))
    
    # Determina la direzione del tratto rettilineo
    if abs(delta_r) > abs(delta_c):
        rect_step_r, rect_step_c = step_r, 0 # Movimento verticale
    else:
        rect_step_r, rect_step_c = 0, step_c # Movimento orizzontale

    # Funzioni interne per generare i segmenti del percorso
    def make_diagonal_moves():
        nonlocal r_curr, c_curr
        for _ in range(num_diagonal_steps):
            r_curr += step_r
            c_curr += step_c
            path.append((r_curr, c_curr))

    def make_rectilinear_moves():
        nonlocal r_curr, c_curr
        for _ in range(num_rectilinear_steps):
            r_curr += rect_step_r
            c_curr += rect_step_c
            path.append((r_curr, c_curr))

    # Costruisci il percorso nell'ordine richiesto
    if diagonal_first: # Tipo 1
        make_diagonal_moves()
        make_rectilinear_moves()
    else: # Tipo 2
        make_rectilinear_moves()
        make_diagonal_moves()
        
    return path

def find_free_paths(grid, origin, destination):
    """
    Trova i cammini liberi tra un'origine e una destinazione.
    
    :return: Una lista di tuple. Ogni tupla è nella forma (tipo, percorso),
             dove tipo è una stringa ("Tipo 1" o "Tipo 2") e percorso è
             una lista di coordinate.
    """
    found_paths = [] # Nome cambiato per chiarezza
    
    if grid[destination[0]][destination[1]] == 1:
        return []

    # 1. Controlla il percorso di TIPO 1 (obliquo -> rettilineo)
    path_type1 = generate_path_coordinates(origin, destination, diagonal_first=True)
    if is_path_free(grid, path_type1):
        # Aggiungi una tupla con il tipo e il percorso
        found_paths.append(("Tipo 1", path_type1))
        
    # 2. Controlla il percorso di TIPO 2 (rettilineo -> obliquo)
    path_type2 = generate_path_coordinates(origin, destination, diagonal_first=False)
    
    # Se il percorso è una linea retta, Tipo 1 e Tipo 2 sono uguali.
    # In base alla regola, un percorso solo obliquo o solo rettilineo
    # è classificato come TIPO 1. Quindi non dobbiamo aggiungere un duplicato.
    if path_type1 == path_type2:
        return found_paths # Restituisce solo il risultato del Tipo 1
    
    # Se i percorsi sono diversi, controlla se il Tipo 2 è libero
    if is_path_free(grid, path_type2):
        # Aggiungi una tupla con il tipo e il percorso
        found_paths.append(("Tipo 2", path_type2))
        
    return found_paths

def generate_ideal_minimum_path(origin, destination):
    """
    Genera le coordinate del "cammino minimo ideale" (il percorso giallo),
    che è un percorso di Tipo 1 (prima tutte le mosse diagonali, poi quelle rettilinee).
    Questa funzione è essenzialmente la stessa di 'generate_path_coordinates'
    con diagonal_first=True.

    :param origin: Tupla (r, c) di partenza.
    :param destination: Tupla (r, c) di arrivo.
    :return: Lista di tuple (r, c) che rappresenta il cammino ideale.
    """
    path = [origin]
    r_curr, c_curr = origin
    r_dest, c_dest = destination

    delta_r = r_dest - r_curr
    delta_c = c_dest - c_curr

    # Calcola il numero di passi diagonali e rettilinei necessari
    num_diagonal_steps = min(abs(delta_r), abs(delta_c))
    num_rectilinear_steps = abs(abs(delta_r) - abs(delta_c))
    
    # Determina la direzione dei passi (-1, 0, o 1)
    step_r = int(np.sign(delta_r))
    step_c = int(np.sign(delta_c))
    
    # Determina la direzione del tratto rettilineo
    if abs(delta_r) > abs(delta_c):
        rect_step_r, rect_step_c = step_r, 0 # Movimento verticale
    else:
        rect_step_r, rect_step_c = 0, step_c # Movimento orizzontale

    # 1. Esegui i passi diagonali
    for _ in range(num_diagonal_steps):
        r_curr += step_r
        c_curr += step_c
        path.append((r_curr, c_curr))

    # 2. Esegui i passi rettilinei
    for _ in range(num_rectilinear_steps):
        r_curr += rect_step_r
        c_curr += rect_step_c
        path.append((r_curr, c_curr))
        
    return path

def is_region_free(grid, origin, destination):
    """
    Verifica se l'intera regione rettangolare delimitata dai percorsi di
    Tipo 1 e Tipo 2 è libera da ostacoli.
    Questo implementa il vincolo di "raggiungibilità reciproca".
    """
    r_o, c_o = origin
    r_d, c_d = destination

    # Determina le coordinate minime e massime per righe e colonne,
    # definendo così il rettangolo di delimitazione.
    min_r, max_r = min(r_o, r_d), max(r_o, r_d)
    min_c, max_c = min(c_o, c_d), max(c_o, c_d)

    # Scansiona ogni cella all'interno di questo rettangolo
    for r in range(min_r, max_r + 1):
        for c in range(min_c, max_c + 1):
            if grid[r][c] == 1:
                return False  # Trovato un ostacolo nella regione
                
    return True # La regione è completamente libera

def calcola_contesto_e_complemento(grid, origin):
    """
    Calcola il Contesto e il Complemento di O basandosi sulla definizione letterale.
    - Contesto: raggiungibile con un cammino libero di Tipo 1.
    - Complemento: NON raggiungibile con T1, ma raggiungibile con T2.
    """
    num_rows, num_cols = len(grid), len(grid[0])
    contesto_di_O = []
    complemento_di_O = []

    for r_dest in range(num_rows):
        for c_dest in range(num_cols):
            destination = (r_dest, c_dest)

            if destination == origin or grid[r_dest][c_dest] == 1:
                continue

            # Genera entrambi i percorsi
            path_type1 = generate_path_coordinates(origin, destination, diagonal_first=True)
            
            # Valuta la libertà del percorso di Tipo 1
            if is_path_free(grid, path_type1):
                contesto_di_O.append(destination)
            else:
                # Se il T1 è bloccato, allora e solo allora valutiamo il T2 per il complemento.
                path_type2 = generate_path_coordinates(origin, destination, diagonal_first=False)
                
                # Per essere nel complemento, il T2 deve essere libero.
                if is_path_free(grid, path_type2):
                    # Un'ultima sicurezza: percorsi perfettamente allineati sono
                    # sempre di Tipo 1 per definizione, quindi non possono essere nel complemento.
                    # Questa condizione è vera solo se non sono allineati.
                    if path_type1 != path_type2:
                        complemento_di_O.append(destination)

    return contesto_di_O, complemento_di_O

def visualizza_risultato_finale(grid_da_mostrare, cmap, legend_elements, titolo):
    """
    Funzione di visualizzazione che usa pcolormesh e aggiunge una legenda personalizzata.
    
    :param grid_da_mostrare: La griglia numerica da visualizzare.
    :param cmap: La mappa di colori (ListedColormap).
    :param legend_elements: Una lista di Patch per la legenda.
    :param titolo: Il titolo del grafico.
    """
    np_grid = np.array(grid_da_mostrare)
    
    fig, ax = plt.subplots(figsize=(14, 8)) # Aumentiamo le dimensioni per fare spazio alla legenda

    # Usiamo pcolormesh per disegnare sia i colori che i bordi
    ax.pcolormesh(np_grid, cmap=cmap, edgecolors='black', linewidth=0.5)

    ax.set_title(titolo, fontsize=16)
    ax.set_aspect('equal')
    ax.invert_yaxis()

    # Rimuoviamo gli assi numerici per una visualizzazione pulita
    ax.set_xticks([])
    ax.set_yticks([])
    
    # Aggiungi la legenda al grafico
    ax.legend(handles=legend_elements, bbox_to_anchor=(1.02, 1), loc='upper left')
    
    # Adatta il layout per assicurarsi che la legenda non venga tagliata
    plt.tight_layout()
    
    plt.show()

def calcola_distanza_libera(origin, destination):
    """
    Calcola la distanza libera (dlib) tra due celle O e D.
    Questa è la lunghezza di un cammino libero, se esiste.
    La formula è: sqrt(2)*delta_min + (delta_max - delta_min).

    :param origin: Tupla (riga, colonna) della cella di partenza O.
    :param destination: Tupla (riga, colonna) della cella di destinazione D.
    :return: La distanza libera (un valore float).
    """
    # Estrai le coordinate
    r_o, c_o = origin
    r_d, c_d = destination

    # 1. Calcola le differenze in valore assoluto (delta_x e delta_y)
    #    Nota: delta_x corrisponde alla differenza tra le colonne (asse orizzontale)
    #    e delta_y alla differenza tra le righe (asse verticale).
    delta_x = abs(c_o - c_d)
    delta_y = abs(r_o - r_d)

    # 2. Trova delta_min e delta_max
    delta_min = min(delta_x, delta_y)
    delta_max = max(delta_x, delta_y)
    
    # 3. Applica la formula
    #    sqrt(2) * (numero di passi diagonali) + 1 * (numero di passi rettilinei)
    distanza = math.sqrt(2) * delta_min + (delta_max - delta_min)
    
    return distanza
