class LabelManager:
    
    def __init__(self):
        self.mappa_coord_etichetta = {}
        self.prossimo_indice = 0
        self.alfabeto = "ABCEFGHIJKLMNPQRSTUVWXYZΣΔΦΓ&*%$#@"
    
    def _indice_a_etichetta(self, n):
        if n < 0: return ""
        base = len(self.alfabeto)
        if n < base: return self.alfabeto[n]
        else: return self._indice_a_etichetta(n // base - 1) + self.alfabeto[n % base]
    
    def get_label(self, coords):
        if coords not in self.mappa_coord_etichetta:
            nuova_etichetta = self._indice_a_etichetta(self.prossimo_indice)
            self.mappa_coord_etichetta[coords] = nuova_etichetta
            self.prossimo_indice += 1
        return self.mappa_coord_etichetta[coords]