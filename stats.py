import time

class StatsTracker:
    def __init__(self):
        """
        Inizializza l'oggetto di monitoraggio delle statistiche.
        Attributi:
            start_time (float): il timestamp in cui l'esecuzione parte.
            end_time (float): il timestamp in cui l'esecuzione termina.
            execution_time (float): il tempo totale richiesto per l'esecuzione.
            frontier_cells_discovered (set): un insieme di celle di frontiera trovate.
            pruning_success_count (int): il numero di operazioni di potatura con successo.
            recursion_depth (int): la massima profondità ricorsiva raggiunta.
        """
        self.start_time = 0
        self.end_time = 0
        self.execution_time = 0
        self.frontier_cells_discovered = set()
        self.pruning_success_count = 0
        self.recursion_depth = 0

    def start(self):
        """
        Avvia il cronometro registrando il valore corrente del contatore ad alta risoluzione delle prestazioni.
        """
        self.start_time = time.perf_counter()

    def stop(self):
        """
        Ferma il cronometro registrando il valore corrente del contatore ad alta risoluzione delle prestazioni.
        """
        self.end_time = time.perf_counter()
        self.execution_time = self.end_time - self.start_time

    def add_frontier_cells(self, frontier_cells):
        """
        Aggiunge le coordinate delle celle di frontiera appena scoperte all’insieme delle celle di frontiera già scoperte.
            Argomenti:
                - frontier_cells (iterabile): un iterabile di tuple, ciascuna contenente una coordinata e dati associati.
                - self.frontier_cells_discovered (set): l’insieme viene aggiornato con le coordinate estratte da frontier_cells.
        """
        coords = {item[0] for item, _ in frontier_cells}
        self.frontier_cells_discovered.update(coords)

    def increment_pruning_count(self):
        """
        Incrementa il conteggio delle operazioni di potatura con successo.
        """
        self.pruning_success_count += 1
    
    def track_depth(self, depth):
        """
        Aggiorna la profondità massima ricorsiva incontrata.
        Args:
            depth (int): profondità ricorsiva corrente da tracciare.
        """
        if depth > self.recursion_depth:
            self.recursion_depth = depth
        
    def get_summary(self):
        """
        Restituisce un summary di chiavi statistiche collezionate durante l'esecuzione.

        Returns:
            dict: un dizionario che contiene:
                - execution_time (float): il tempo di esecuzione totale.
                - total_unique_frontiers (int): il conto di frontiere uniche scoperte.
                - pruning_successes (int): il numero di operazioni di potatura con successo.
                - max_recursion_depth (int): la profondità ricorsiva massima raggiunta.
        """
        return {
            "execution_time": self.execution_time,
            "total_unique_frontiers": len(self.frontier_cells_discovered),
            "pruning_successes": self.pruning_success_count,
            "max_recursion_depth": self.recursion_depth + 1 
        }