import math
import heapq

class Grid:
    """
    Rappresenta la griglia del problema come un grafo usando una lista di adiacenze.
    La lista di adiacenze è un dizionario: {coord: {neighbor_coord: cost}}.
    """
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.adj = {} 

    @classmethod
    def from_matrix(cls, grid_data):
        """
        Metodo factory per creare e popolare la Grid (con la sua lista di adiacenze)
        a partire da una matrice numerica di ostacoli.
        """
        rows = len(grid_data)
        cols = len(grid_data[0]) if rows > 0 else 0
        
        grid = cls(rows, cols)

        obstacles = set()
        for r in range(rows):
            for c in range(cols):
                if grid_data[r][c] == 1:
                    obstacles.add((r, c))
                else:
                    grid.adj[(r, c)] = {} 

        moves = {
            "cardinal": [(-1, 0), (1, 0), (0, -1), (0, 1)],
            "diagonal": [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        }
        
        for r_curr, c_curr in grid.adj.keys():
            for dr, dc in moves["cardinal"]:
                nr, nc = r_curr + dr, c_curr + dc
                if (nr, nc) in grid.adj: 
                    grid.adj[(r_curr, c_curr)][(nr, nc)] = 1.0

            for dr, dc in moves["diagonal"]:
                nr, nc = r_curr + dr, c_curr + dc
                if (nr, nc) in grid.adj:
                    grid.adj[(r_curr, c_curr)][(nr, nc)] = math.sqrt(2)
        
        return grid

    def is_traversable(self, coords, forbidden_obstacles=frozenset()):
        """
        Controlla se una cella è nel grafo (quindi non è un ostacolo originale)
        E non è un ostacolo temporaneo (proibito).
        """
        return coords in self.adj and coords not in forbidden_obstacles

    def get_neighbors(self, coords):
        """Restituisce i vicini di una cella dalla lista di adiacenze."""
        return self.adj.get(coords, {})

    def is_within_bounds(self, coords):
        """Controlla se una coordinata è dentro i limiti della griglia."""
        r, c = coords
        return 0 <= r < self.rows and 0 <= c < self.cols
    
    def to_matrix(self, custom_values=None, default_obstacle_val=1, default_free_val=0):
        """
        Converte la rappresentazione interna (lista di adiacenze) in una
        matrice numerica, adatta per la stampa o la visualizzazione.

        :param custom_values: Un dizionario opzionale {coord: valore} per
                              colorare celle specifiche (es. Origine, Frontiera).
        :param default_obstacle_val: Il valore numerico per gli ostacoli.
        :param default_free_val: Il valore numerico per le celle libere.
        :return: Una lista di liste (matrice numerica).
        """
        matrix = [[default_obstacle_val for _ in range(self.cols)] for _ in range(self.rows)]
        
        for r, c in self.adj.keys():
            matrix[r][c] = default_free_val
            
        if custom_values:
            for (r, c), value in custom_values.items():
                if 0 <= r < self.rows and 0 <= c < self.cols:
                    matrix[r][c] = value
                    
        return matrix