import heapq

class Grid:
    """
    Rappresenta la griglia del problema. Incapsula i dati della mappa e
    fornisce metodi di utility per interagire con essa.
    """
    def __init__(self, grid_data):
        self.data = grid_data
        self.rows = len(grid_data)
        self.cols = len(grid_data[0]) if self.rows > 0 else 0

    def is_obstacle(self, coords):
        """Controlla se una cella è un ostacolo."""
        r, c = coords
        return self.data[r][c] == 1

    def is_within_bounds(self, coords):
        """Controlla se una coordinata è dentro i limiti della griglia."""
        r, c = coords
        return 0 <= r < self.rows and 0 <= c < self.cols

class State:
    """
    Rappresenta uno stato nella ricerca (es. un nodo in A* o un landmark).
    Contiene la posizione, il riferimento al genitore e il costo per raggiungerlo.
    """
    def __init__(self, position, parent=None, g_cost=0.0):
        self.position = position
        self.parent = parent
        self.g_cost = g_cost # Costo esatto dall'origine (g(n))

    def __lt__(self, other):
        """Confronto necessario per la coda di priorità."""
        return False # L'ordine dipende dal f_score, non dallo stato in sé

    def __eq__(self, other):
        """Due stati sono uguali se hanno la stessa posizione."""
        return isinstance(other, State) and self.position == other.position

    def __hash__(self):
        """Permette di usare gli oggetti State in set e dizionari."""
        return hash(self.position)

class PriorityQueue:
    """
    Una coda di priorità (min-heap) per gestire la Open List.
    """
    def __init__(self):
        self._elements = []
        self._entry_finder = {} # Dizionario per aggiornamenti rapidi
        self._counter = 0 # Contatore per gestire gli spareggi

    def add(self, item, priority):
        """Aggiunge un elemento alla coda o aggiorna la sua priorità."""
        if item in self._entry_finder:
            # Se l'elemento è già presente, lo marchiamo come rimosso
            # e ne aggiungiamo una nuova versione con la priorità aggiornata.
            # Questo è più efficiente che cercare e modificare.
            self.remove(item)
        
        entry = [priority, self._counter, item]
        self._entry_finder[item] = entry
        heapq.heappush(self._elements, entry)
        self._counter += 1

    def remove(self, item):
        """Marca un elemento come rimosso."""
        if item in self._entry_finder:
            entry = self._entry_finder.pop(item)
            entry[-1] = None # L'elemento viene "invalidato"

    def pop(self):
        """Rimuove e restituisce l'elemento con la priorità più bassa."""
        while self._elements:
            priority, count, item = heapq.heappop(self._elements)
            if item is not None:
                del self._entry_finder[item]
                return item
        raise KeyError('pop from an empty priority queue')

    def is_empty(self):
        return not self._entry_finder