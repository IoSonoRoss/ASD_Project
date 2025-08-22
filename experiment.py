# File: experiment.py

import random
import pandas as pd # Per la gestione e salvataggio dei dati (pip install pandas)
import math

# Importa i tuoi moduli
import grid_generator
import search
import closure_logic
import stats
import labeling

def run_single_experiment(grid, origin, destination):
    """
    Esegue una singola coppia di test (O->D e D->O) e restituisce i risultati.
    """
    results = {}
    
    # --- Test 1: O -> D ---
    label_manager_od = labeling.LabelManager()
    stats_tracker_od = stats.StatsTracker()
    search.memoization_cache = {} # Pulisce la cache
    
    stats_tracker_od.start()
    lunghezza_od, sequenza_od = search.procedura_cammino_min(
        origin, destination, grid, label_manager_od, stats_tracker_od
    )
    stats_tracker_od.stop()
    
    results['lunghezza_OD'] = lunghezza_od
    summary_od = stats_tracker_od.get_summary()
    results.update({f"{key}_OD": val for key, val in summary_od.items()})

    # --- Test 2: D -> O (per verifica correttezza) ---
    label_manager_do = labeling.LabelManager()
    stats_tracker_do = stats.StatsTracker()
    search.memoization_cache = {} # Pulisce la cache
    
    stats_tracker_do.start()
    lunghezza_do, sequenza_do = search.procedura_cammino_min(
        destination, origin, grid, label_manager_do, stats_tracker_do
    )
    stats_tracker_do.stop()
    
    results['lunghezza_DO'] = lunghezza_do
    
    # Verifica di correttezza
    results['correttezza_superata'] = math.isclose(lunghezza_od, lunghezza_do)
    
    return results

def main():
    """
    Script principale per eseguire la suite di esperimenti.
    """
    
    # --- DEFINIZIONE DEGLI SCENARI DI TEST ---
    
    # Esperimento 1: Variazione della Dimensione della Griglia
    scenari_dimensione = [
        # {"id": "Dim-10x10", "rows": 10, "cols": 10, "obstacle_ratio": 0.2, "num_runs": 5},
        {"id": "Dim-20x20", "rows": 20, "cols": 20, "obstacle_ratio": 0.2, "num_runs": 1},
        #{"id": "Dim-30x30", "rows": 30, "cols": 30, "obstacle_ratio": 0.2, "num_runs": 3},
        #{"id": "Dim-40x40", "rows": 40, "cols": 40, "obstacle_ratio": 0.2, "num_runs": 2},
        # {"id": "Dim-50x50", "rows": 50, "cols": 50, "obstacle_ratio": 0.2, "num_runs": 1}, # Può essere lento
    ]

    # Esperimento 2: Variazione della Densità di Ostacoli
    scenari_ostacoli = [
        {"id": "Obs-10%", "rows": 30, "cols": 30, "obstacle_ratio": 0.1, "num_runs": 1},
        #{"id": "Obs-20%", "rows": 30, "cols": 30, "obstacle_ratio": 0.2, "num_runs": 5},
        #{"id": "Obs-30%", "rows": 30, "cols": 30, "obstacle_ratio": 0.3, "num_runs": 5},
        #{"id": "Obs-40%", "rows": 30, "cols": 30, "obstacle_ratio": 0.4, "num_runs": 3}, # Più ostacoli, più lento
    ]
    
    tutti_gli_scenari = scenari_dimensione + scenari_ostacoli
    lista_risultati_completa = []

    print("--- INIZIO SPERIMENTAZIONE ---")
    
    for scenario in tutti_gli_scenari:
        print(f"\n--- Esecuzione Scenario: {scenario['id']} ({scenario['num_runs']} runs) ---")
        
        for i in range(scenario['num_runs']):
            print(f"  Run {i+1}/{scenario['num_runs']}...")
            
            # 1. Genera la griglia
            grid = grid_generator.generate_grid_map(
                rows=scenario['rows'], 
                cols=scenario['cols'], 
                obstacle_ratio=scenario['obstacle_ratio']
            )
            
            # 2. Scegli O e D validi
            celle_libere = [(r, c) for r in range(len(grid)) for c in range(len(grid[0])) if grid[r][c] == 0]
            if len(celle_libere) < 2:
                print("    ERRORE: Non ci sono abbastanza celle libere per scegliere O e D.")
                continue
            O, D = random.sample(celle_libere, 2)
            
            # Imposta la destinazione globale per il logging
            search.D_globale = D
            
            # 3. Esegui l'esperimento
            risultati_run = run_single_experiment(grid, O, D)
            
            # 4. Combina i dati di input con i dati di output
            record_completo = {
                "id_scenario": scenario['id'],
                "run_num": i + 1,
                "rows": scenario['rows'],
                "cols": scenario['cols'],
                "obstacle_ratio": scenario['obstacle_ratio'],
                "origin": O,
                "destination": D,
                **risultati_run # Aggiunge tutti i risultati del test
            }
            
            lista_risultati_completa.append(record_completo)

    # --- 5. SALVATAGGIO DEI RISULTATI ---
    if lista_risultati_completa:
        df = pd.DataFrame(lista_risultati_completa)
        nome_file_csv = "risultati_sperimentazione.csv"
        df.to_csv(nome_file_csv, index=False)
        print(f"\n--- SPERIMENTAZIONE COMPLETATA ---")
        print(f"Tutti i risultati sono stati salvati nel file: {nome_file_csv}")
    else:
        print("\n--- SPERIMENTAZIONE COMPLETATA SENZA RISULTATI ---")

if __name__ == "__main__":
    main()