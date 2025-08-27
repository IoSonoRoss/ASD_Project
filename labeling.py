class LabelManager:
    
    def __init__(self):
        """
        Iniziailizza l'oggetto etichettato con valori di default.
        Attributi:
            mappa_coord_etichetta (dict): un dizionario che mappa le coordinate in etichette.
            prossimo_indice (int): l'indice successivo da usare per etichettare.
            alfabeto (str): una stringa che contiene un insieme di caratteri usati per etichettare.
        """
        self.mappa_coord_etichetta = {}
        self.prossimo_indice = 0
        self.alfabeto = "ABCEFGHIJKLMNPQRSTUVWXYZΣΔΦΓ&*%$#@"
    
    def _indice_a_etichetta(self, n):
        """
        Converte un indice intero non negativo 'n' in una etichetta usando l'alfabeto specificato.
        Args:
            n (int): l'indice intero non negativo da convertire.
        Returns:
            str: l'etichetta corrispondente come stringa. Ritorna una stringa vuota se `n` è negativa.
        """
        if n < 0: return ""
        base = len(self.alfabeto)
        if n < base: return self.alfabeto[n]
        else: return self._indice_a_etichetta(n // base - 1) + self.alfabeto[n % base]
    
    def get_label(self, coords):
        """
        Ritorna l'etichetta associata con le coordinate. Se le coordinate non sono ancora associate ad una etichetta,
        ne viene generata una nuova, assegnata e restituita.
        Args:
            coords: le coordinate per cui recuperare o assegnare un'etichetta.
        Returns:
            L'etichetta associata con le coordinate date.
        """
        if coords not in self.mappa_coord_etichetta:
            nuova_etichetta = self._indice_a_etichetta(self.prossimo_indice)
            self.mappa_coord_etichetta[coords] = nuova_etichetta
            self.prossimo_indice += 1
        return self.mappa_coord_etichetta[coords]