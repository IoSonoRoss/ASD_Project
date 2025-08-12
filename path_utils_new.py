import math
import heapq
import numpy as np

def is_path_free(grid, path):
    """Verifica se un percorso è libero, senza corner-check."""
    if not path: return False
    for r, c in path[1:]:
        if not (0 <= r < len(grid) and 0 <= c < len(grid[0])) or grid[r][c] == 1: return False
    return True

def generate_path_coordinates(origin, destination, diagonal_first):
    """Genera le coordinate per un percorso di Tipo 1 o Tipo 2."""
    path = [origin]
    r_curr, c_curr = origin; r_dest, c_dest = destination
    delta_r, delta_c = r_dest - r_curr, c_dest - c_curr
    num_diag = min(abs(delta_r), abs(delta_c))
    num_rect = abs(abs(delta_r) - abs(delta_c))
    step_r, step_c = int(np.sign(delta_r)), int(np.sign(delta_c))
    if abs(delta_r) > abs(delta_c): rect_step_r, rect_step_c = step_r, 0
    else: rect_step_r, rect_step_c = 0, step_c
    def make_diag_moves():
        nonlocal r_curr, c_curr
        for _ in range(num_diag): r_curr += step_r; c_curr += step_c; path.append((r_curr, c_curr))
    def make_rect_moves():
        nonlocal r_curr, c_curr
        for _ in range(num_rect): r_curr += rect_step_r; c_curr += rect_step_c; path.append((r_curr, c_curr))
    if diagonal_first: make_diag_moves(); make_rect_moves()
    else: make_rect_moves(); make_diag_moves()
    return path

def calcola_distanza_libera(origin, destination):
    """Calcola la distanza libera (dlib) tra due celle O e D."""
    if not origin or not destination: return float('inf')
    delta_x = abs(origin[1] - destination[1])
    delta_y = abs(origin[0] - destination[0])
    delta_min, delta_max = min(delta_x, delta_y), max(delta_x, delta_y)
    return math.sqrt(2) * delta_min + (delta_max - delta_min)

def calcola_contesto_e_complemento(grid, origin):
    """Calcola Contesto e Complemento di O."""
    num_rows, num_cols = len(grid), len(grid[0])
    contesto, complemento = [], []
    for r_dest in range(num_rows):
        for c_dest in range(num_cols):
            destination = (r_dest, c_dest)
            if destination == origin or grid[r_dest][c_dest] == 1: continue
            path_t1 = generate_path_coordinates(origin, destination, True)
            if is_path_free(grid, path_t1):
                contesto.append(destination)
            else:
                path_t2 = generate_path_coordinates(origin, destination, False)
                if is_path_free(grid, path_t2) and path_t1 != path_t2: complemento.append(destination)
    return contesto, complemento

def calcola_frontiera(grid, origin, contesto, complemento):
    """Calcola la frontiera di O e associa a ogni cella il suo tipo (1 o 2)."""
    chiusura = set(contesto) | set(complemento) | {origin}
    contesto_set = set(contesto)
    frontiera_con_tipo = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    for r, c in chiusura:
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]) and grid[nr][nc] == 0 and (nr, nc) not in chiusura:
                tipo = 1 if (r, c) in contesto_set else 2
                frontiera_con_tipo.append(((r, c), tipo))
                break
    return frontiera_con_tipo

# --- CLASSE ROBUSTA PER GESTIRE ETICHETTE DINAMICHE E UNIVOCHE ---
class LabelManager:
    """
    Gestisce la creazione di etichette univoche e infinite per le coordinate.
    Usa una logica simile alle colonne di Excel (A-Z, AA, AB...).
    """
    def __init__(self):
        self.mappa_coord_etichetta = {}
        self.prossimo_indice = 0
        # Definiamo l'alfabeto di base da usare per la generazione.
        # Escludiamo O e D per evitare ambiguità.
        self.alfabeto = "ABCEFGHIJKLMNPQRSTUVWXYZEΣΔΦΓ&*%$#@"

    def _indice_a_etichetta(self, n):
        """
        Converte un indice numerico (0, 1, 2...) in un'etichetta univoca.
        Esempio con alfabeto 'ABC': 0->A, 1->B, 2->C, 3->AA, 4->AB...
        """
        if n < 0:
            return ""
        
        base = len(self.alfabeto)
        etichetta = ""
        
        # Copia di n per non modificare l'originale nel ciclo
        temp_n = n
        
        while True:
            # Calcola l'indice del carattere per la posizione corrente
            remainder = temp_n % base
            # Aggiungi il carattere all'inizio della stringa
            etichetta = self.alfabeto[remainder] + etichetta
            
            # Aggiorna l'indice per la prossima "cifra" a sinistra
            temp_n = temp_n // base - 1
            
            # Se abbiamo processato tutte le "cifre", usciamo
            if temp_n < 0:
                break
                
        return etichetta

    def get_label(self, coords):
        """
        Restituisce l'etichetta per una coordinata, creandone una nuova se non esiste.
        Questo è l'unico metodo pubblico da chiamare dall'esterno.
        """
        if coords not in self.mappa_coord_etichetta:
            # Genera una nuova etichetta basata sull'indice corrente
            nuova_etichetta = self._indice_a_etichetta(self.prossimo_indice)
            
            # Salva l'associazione e incrementa l'indice per la prossima etichetta
            self.mappa_coord_etichetta[coords] = nuova_etichetta
            self.prossimo_indice += 1
            
        return self.mappa_coord_etichetta[coords]

# --- PROCEDURA CAMMINOMIN CHE USA IL LABELMANAGER ---
memoization_cache = {}

def procedura_cammino_min(
    origin, destination, grid, label_manager, 
    ostacoli_proibiti=frozenset(), depth=0):
    """
    [Versione con Logging] Implementazione RICORSIVA che stampa l'albero di esplorazione.
    """
    # --- LOGGING: Inizio chiamata ---
    indent = "  " * depth
    origin_label = "O" if depth == 0 else label_manager.get_label(origin)
    print(f"{indent}--> Chiamata CAMMINOMIN(O={origin_label}, D={destination})")

    cache_key = (origin, destination, ostacoli_proibiti)
    if cache_key in memoization_cache:
        lunghezza, _ = memoization_cache[cache_key]
        status = "Infinito" if lunghezza == float('inf') else f"{lunghezza:.2f}"
        print(f"{indent}<-- Trovato in cache! Risultato: {status}")
        return memoization_cache[cache_key]

    if origin == destination:
        print(f"{indent}<-- Caso Base: Origine == Destinazione. Ritorno (0, [destinazione])")
        return 0, [(origin, 1)]

    grid_temp = [row[:] for row in grid]
    for r, c in ostacoli_proibiti:
        if 0 <= r < len(grid_temp) and 0 <= c < len(grid_temp[0]):
            grid_temp[r][c] = 1

    contesto, complemento = calcola_contesto_e_complemento(grid_temp, origin)
    
    if destination in set(contesto):
        lunghezza = calcola_distanza_libera(origin, destination)
        print(f"{indent}<-- Caso Base: D nel Contesto di {origin_label}. Ritorno ({lunghezza:.2f}, ...)")
        return lunghezza, [(origin, 0), (destination, 1)]
    if destination in set(complemento):
        lunghezza = calcola_distanza_libera(origin, destination)
        print(f"{indent}<-- Caso Base: D nel Complemento di {origin_label}. Ritorno ({lunghezza:.2f}, ...)")
        return lunghezza, [(origin, 0), (destination, 2)]

    frontiera_con_tipo = calcola_frontiera(grid_temp, origin, contesto, complemento)
    
    for (coords, _) in frontiera_con_tipo:
        label_manager.get_label(coords)

    if not frontiera_con_tipo:
        print(f"{indent}<-- Vicolo Cieco: Frontiera di {origin_label} è vuota. Ritorno (inf, [])")
        return float('inf'), []

    lunghezza_min, seq_min = float('inf'), []
    frontiera_con_tipo.sort(key=lambda x: calcola_distanza_libera(x[0], destination))
    
    print(f"{indent}    Frontiera di {origin_label} trovata con {len(frontiera_con_tipo)} celle. Inizio ciclo for...")

    for F, tipo_F in frontiera_con_tipo:
        F_label = label_manager.get_label(F)
        lOF = calcola_distanza_libera(origin, F)
        
        # Pruning
        stima_costo = lOF + calcola_distanza_libera(F, destination)
        if stima_costo >= lunghezza_min:
            print(f"{indent}    - Scarto F={F_label}: stima {stima_costo:.2f} >= min_attuale {lunghezza_min:.2f}")
            continue
        
        print(f"{indent}    - Provo F={F_label} (tipo {tipo_F}), costo O->F: {lOF:.2f}")

        chiusura_attuale = set(contesto) | set(complemento) | {origin}
        nuovi_ostacoli_proibiti = ostacoli_proibiti.union(chiusura_attuale)
        
        # Chiamata Ricorsiva
        lFD, seqFD = procedura_cammino_min(
            F, destination, grid, label_manager, 
            frozenset(nuovi_ostacoli_proibiti), depth + 1
        )
        
        if lFD == float('inf'):
            print(f"{indent}      Risultato da F={F_label}: Vicolo cieco.")
            continue
        
        lTot = lOF + lFD
        print(f"{indent}      Risultato da F={F_label}: Trovato percorso di lunghezza totale {lTot:.2f}")
        if lTot < lunghezza_min:
            print(f"{indent}      !!! NUOVO MINIMO TROVATO: {lTot:.2f} (precedente: {lunghezza_min:.2f}) !!!")
            lunghezza_min = lTot
            seq_min = compatta_sequenza([(origin, 0), (F, tipo_F)], seqFD)
            
    status_finale = "Infinito" if lunghezza_min == float('inf') else f"{lunghezza_min:.2f}"
    print(f"{indent}<-- Fine esplorazione per {origin_label}. Miglior risultato: {status_finale}")
    
    memoization_cache[cache_key] = (lunghezza_min, seq_min)
    return lunghezza_min, seq_min

def compatta_sequenza(seq1, seq2):
    if not isinstance(seq2, list) or not seq2: return seq1
    return seq1 + seq2[1:]