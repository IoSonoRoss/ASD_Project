import argparse
import pandas as pd
import random
import time
import math

# Importa i tuoi moduli
import grid_generator
import search
import closure_logic
import stats
import labeling

def select_od_pair(grid):
    """
    Seleziona una coppia (O, D) valida da una griglia.
    Tenta di scegliere punti lontani tra loro.
    """
    rows, cols = len(grid), len(grid[0])
    free_cells = [(r, c) for r in range(rows) for c in range(cols) if grid[r][c] == 0]
    
    if len(free_cells) < 2:
        return None, None

    # Tenta di scegliere O e D in quadranti opposti per massimizzare la distanza
    quadrant1 = [cell for cell in free_cells if cell[0] < rows / 2 and cell[1] < cols / 2]
    quadrant4 = [cell for cell in free_cells if cell[0] > rows / 2 and cell[1] > cols / 2]
    
    if quadrant1 and quadrant4:
        origin = random.choice(quadrant1)
        destination = random.choice(quadrant4)
        return origin, destination
    else:
        # Fallback se i quadranti sono vuoti
        return random.sample(free_cells, 2)

def run_single_run(grid, origin, destination, test_type):
    """
    Esegue un singolo test per una data griglia e coppia (O,D).
    Restituisce un dizionario con i risultati.
    """
    results = {}

    if test_type == 'confronto':
        # --- Esegui entrambe le versioni ---
        
        # Test Ricorsivo
        stats_rec = stats.StatsTracker()
        label_man = labeling.LabelManager()
        search.memoization_cache = {}
        search.D_globale = destination # Per il logging
        stats_rec.start()
        lung_rec, _ = search.procedura_cammino_min_ricorsiva(origin, destination, grid, label_man, stats_rec)
        stats_rec.stop()
        summary_rec = stats_rec.get_summary()
        results.update({f"{key}_rec": val for key, val in summary_rec.items()})
        results['lunghezza_rec'] = lung_rec

        # Test Iterativo
        stats_it = stats.StatsTracker()
        stats_it.start()
        lung_it, _ = search.procedura_cammino_min_iterativa(origin, destination, grid, stats_it)
        stats_it.stop()
        summary_it = stats_it.get_summary()
        results.update({f"{key}_it": val for key, val in summary_it.items()})
        results['lunghezza_it'] = lung_it
        
    else:
        # --- Esegui solo la versione Iterativa (veloce) ---
        stats = stats.StatsTracker()
        lung_it, _ = search.procedura_cammino_min_iterativa(origin, destination, grid, stats)
        summary = stats.get_summary()
        results = {
            "lunghezza_OD": lung_it,
            **summary
        }
        
        # Test di correttezza D -> O
        stats_do = stats.StatsTracker()
        lung_do, _ = search.procedura_cammino_min_iterativa(destination, origin, grid, stats_do)
        results['lunghezza_DO'] = lung_do
        results['correttezza_superata'] = math.isclose(lung_it, lung_do) if lung_it != float('inf') else lung_do == float('inf')

    return results

def main(args):
    """
    Script principale per l'esecuzione degli esperimenti.
    """
    # --- DEFINIZIONE DEGLI SCENARI DI TEST ---
    scenari_dimensione = [
        {"rows": 15, "cols": 15, "obstacle_ratio": 0.2, "num_runs": 5},
        {"rows": 25, "cols": 25, "obstacle_ratio": 0.2, "num_runs": 3},
        {"rows": 35, "cols": 35, "obstacle_ratio": 0.2, "num_runs": 2},
    ]
    scenari_ostacoli = [
        {"rows": 25, "cols": 25, "obstacle_ratio": 0.1, "num_runs": 5},
        {"rows": 25, "cols": 25, "obstacle_ratio": 0.25, "num_runs": 5},
        {"rows": 25, "cols": 25, "obstacle_ratio": 0.4, "num_runs": 3},
    ]
    # Scenari piccoli per il confronto diretto
    scenari_confronto = [
        {"rows": 10, "cols": 10, "obstacle_ratio": 0.2, "num_runs": 5},
        {"rows": 15, "cols": 15, "obstacle_ratio": 0.2, "num_runs": 3},
    ]

    scenario_map = {
        "dimensione": scenari_dimensione,
        "ostacoli": scenari_ostacoli,
        "confronto": scenari_confronto,
    }
    
    test_type = args.test_type
    config_index = args.config_index
    
    if test_type not in scenario_map or not (0 <= config_index < len(scenario_map[test_type])):
        print(f"Errore: tipo di test '{test_type}' o indice '{config_index}' non validi.")
        return

    config = scenario_map[test_type][config_index]
    config['id_scenario'] = f"{test_type}_{config_index}"
    config['test_type'] = test_type
    
    lista_risultati_run = []
    
    print(f"\n--- Esecuzione Scenario: {config['id_scenario']} ({config['num_runs']} runs) ---")
    
    for i in range(config['num_runs']):
        print(f"  Run {i+1}/{config['num_runs']}...")
        
        grid = grid_generator.generate_grid_map(
            rows=config['rows'], cols=config['cols'], obstacle_ratio=config['obstacle_ratio']
        )
        origin, destination = select_od_pair(grid)
        if not origin:
            print("    ERRORE: Griglia troppo piena per trovare una coppia O, D.")
            continue
            
        risultati_run = run_single_run(grid, origin, destination, test_type)
        
        record_completo = {**config, "run_num": i + 1, "origin": origin, "destination": destination, **risultati_run}
        lista_risultati_run.append(record_completo)

    if lista_risultati_run:
        df = pd.DataFrame(lista_risultati_run)
        output_filename = f"results_{config['id_scenario']}.csv"
        df.to_csv(output_filename, index=False, float_format='%.4f')
        print(f"\n--- Scenario Completato ---")
        print(f"Risultati salvati nel file: {output_filename}")
    else:
        print("\n--- Scenario Completato senza Risultati Validi ---")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script per la sperimentazione dell'algoritmo CAMMINOMIN.")
    parser.add_argument("--test_type", required=True, choices=["dimensione", "ostacoli", "confronto"],
                        help="Il tipo di esperimento da eseguire.")
    parser.add_argument("--config_index", required=True, type=int,
                        help="L'indice della configurazione da testare all'interno del tipo di test.")
    
    args = parser.parse_args()
    main(args)