import argparse
import pandas as pd
import random
import time
import math
import os
import csv

import grid_generator
from solver import PathfindingSolver
from data_structures import Grid

def select_od_pair(grid_obj: Grid):
    """
    Seleziona una coppia (O, D) valida e possibilmente distante da un oggetto Grid.
    """
    rows, cols = grid_obj.rows, grid_obj.cols
    free_cells = list(grid_obj.adj.keys())
    
    if len(free_cells) < 2:
        return None, None

    quadrant1 = [cell for cell in free_cells if cell[0] < rows / 2 and cell[1] < cols / 2]
    quadrant4 = [cell for cell in free_cells if cell[0] > rows / 2 and cell[1] > cols / 2]
    
    if quadrant1 and quadrant4:
        origin = random.choice(quadrant1)
        destination = random.choice(quadrant4)
        return origin, destination
    else:
        return random.sample(free_cells, 2)

def run_single_run(grid_data, origin, destination, use_cache=True, use_pruning=True):
    """
    Esegue una singola esecuzione dell’algoritmo di ricerca del percorso sulla griglia fornita, dalla posizione di partenza a quella di destinazione.
        Argomenti:
            - grid_data (Any): La rappresentazione della griglia o mappa su cui eseguire il pathfinding.
            - origin (Any): Il punto di partenza per l’algoritmo di ricerca del percorso.
            - destination (Any): Il punto di arrivo per l’algoritmo di ricerca del percorso.
            - use_cache (bool, opzionale): Indica se utilizzare la cache per velocizzare i calcoli. Default è True.
            - use_pruning (bool, opzionale): Indica se applicare tecniche di pruning per ottimizzare la ricerca. Default è True.
        Returns
            - dict: Un dizionario contenente la lunghezza minima del percorso ('lunghezza') e statistiche aggiuntive ottenute dal solver.
    """
    solver = PathfindingSolver(grid_data, origin, destination)
    solver.solve(debug=False, use_cache=use_cache, use_pruning=use_pruning)
    stats = solver.get_stats_summary()
    results = {'lunghezza': solver.lunghezza_minima}
    results.update(stats)
    return results

def main(args):
    """Script principale per l'esecuzione degli esperimenti."""
    
    TEST_SUITES = {
        "dimensione": [
            {"rows": 5, "cols": 5, "obstacle_ratio": 0.20, "num_runs": 20}, # config_index 0
            {"rows": 7, "cols": 7, "obstacle_ratio": 0.20, "num_runs": 20}, # config_index 1
            {"rows": 9, "cols": 9, "obstacle_ratio": 0.20, "num_runs": 20}, # config_index 2
            {"rows": 10, "cols": 10, "obstacle_ratio": 0.20, "num_runs": 10}, # config_index 3
            {"rows": 12, "cols": 12, "obstacle_ratio": 0.20, "num_runs": 10}, # config_index 4
            {"rows": 15, "cols": 15, "obstacle_ratio": 0.20, "num_runs": 10},  # config_index 5
            {"rows": 17, "cols": 17, "obstacle_ratio": 0.20, "num_runs": 10}, # config_index 6
            {"rows": 20, "cols": 20, "obstacle_ratio": 0.20, "num_runs": 10},  # config_index 7
        ],
        "ostacoli": [
            {"rows": 15, "cols": 15, "obstacle_ratio": 0.10, "num_runs": 10}, # config_index 0
            {"rows": 15, "cols": 15, "obstacle_ratio": 0.15, "num_runs": 10}, # config_index 1
            {"rows": 15, "cols": 15, "obstacle_ratio": 0.20, "num_runs": 10}, # config_index 2
            {"rows": 15, "cols": 15, "obstacle_ratio": 0.25, "num_runs": 10}, # config_index 3
            {"rows": 15, "cols": 15, "obstacle_ratio": 0.30, "num_runs": 10}, # config_index 4
            {"rows": 15, "cols": 15, "obstacle_ratio": 0.35, "num_runs": 10}, # config_index 5
            {"rows": 15, "cols": 15, "obstacle_ratio": 0.40, "num_runs": 10}, # config_index 6
            {"rows": 15, "cols": 15, "obstacle_ratio": 0.45, "num_runs": 10}, # config_index 7
            {"rows": 15, "cols": 15, "obstacle_ratio": 0.50, "num_runs": 10}, # config_index 8
        ],
        "confronto": [
            {"rows": 10, "cols": 10, "obstacle_ratio": 0.20, "num_runs": 10}, # config_index 0
            {"rows": 15, "cols": 15, "obstacle_ratio": 0.20, "num_runs": 5},  # config_index 1
            {"rows": 18, "cols": 18, "obstacle_ratio": 0.20, "num_runs": 3},  # config_index 2
        ]
    }
    
    test_type = args.test_type
    config_index = args.config_index
    
    if test_type not in TEST_SUITES or not (0 <= config_index < len(TEST_SUITES[test_type])):
        print(f"Errore: tipo di test '{test_type}' o indice '{config_index}' non validi.")
        print(f"Tipi validi: {list(TEST_SUITES.keys())}")
        return

    config = TEST_SUITES[test_type][config_index]
    config['id_scenario'] = f"{test_type}_{config_index}"
    
    lista_risultati_run = []
    
    print(f"\n--- Esecuzione Scenario: {config['id_scenario']} ({config['num_runs']} runs) ---")
    
    for i in range(config['num_runs']):
        print(f"  Run {i+1}/{config['num_runs']}...")
        
        grid_data = grid_generator.generate_grid_map(
            rows=config['rows'], cols=config['cols'], obstacle_ratio=config['obstacle_ratio']
        )
        temp_grid_obj = Grid.from_matrix(grid_data)
        origin, destination = select_od_pair(temp_grid_obj)
        
        if not origin:
            print("    ERRORE: Griglia troppo piena per trovare una coppia O, D. Run saltato.")
            continue

        if test_type == 'confronto':
            risultati_opt = run_single_run(grid_data, origin, destination, use_cache=True, use_pruning=True)
            record_opt = {**config, "run_num": i+1, "origin": origin, "destination": destination, "type": "ottimizzato"}
            record_opt.update({f"{k}_OD": v for k, v in risultati_opt.items()}) 
            lista_risultati_run.append(record_opt)
            
            risultati_naive = run_single_run(grid_data, origin, destination, use_cache=False, use_pruning=False)
            record_naive = {**config, "run_num": i+1, "origin": origin, "destination": destination, "type": "naive"}
            record_naive.update({f"{k}_OD": v for k, v in risultati_naive.items()}) 
            lista_risultati_run.append(record_naive)
        else:
            solver_od = PathfindingSolver(grid_data, origin, destination)
            solver_od.solve(debug=False)
            stats_od = solver_od.get_stats_summary()
            
            solver_do = PathfindingSolver(grid_data, destination, origin)
            solver_do.solve(debug=False)
            stats_do = solver_do.get_stats_summary()

            risultati_run = {}
            risultati_run['lunghezza_OD'] = solver_od.lunghezza_minima
            risultati_run.update({f"{key}_OD": val for key, val in stats_od.items()})
            risultati_run['lunghezza_DO'] = solver_do.lunghezza_minima
            risultati_run.update({f"{key}_DO": val for key, val in stats_do.items()})
            
            lung_od, lung_do = risultati_run['lunghezza_OD'], risultati_run['lunghezza_DO']
            risultati_run['correttezza_superata'] = math.isclose(lung_od, lung_do) if lung_od != float('inf') else lung_do == float('inf')
            
            record_completo = {**config, "run_num": i + 1, "origin": origin, "destination": destination, **risultati_run}
            lista_risultati_run.append(record_completo)

    if lista_risultati_run:
        output_dir = "experiment_data"
        os.makedirs(output_dir, exist_ok=True)
        output_filename = os.path.join(output_dir, f"results_{config['id_scenario']}.csv")
        
        fieldnames = list(lista_risultati_run[0].keys())
        file_exists = os.path.exists(output_filename)

        with open(output_filename, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader()
            writer.writerows(lista_risultati_run)

        print(f"\n--- Scenario Completato ---")
        print(f"Risultati aggiunti al file: {output_filename}")
    else:
        print("\n--- Scenario Completato senza Risultati Validi ---")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script per la sperimentazione dell'algoritmo CAMMINOMIN.")
    parser.add_argument("--test_type", required=True, choices=["dimensione", "ostacoli", "confronto"], help="Il tipo di esperimento da eseguire.")
    parser.add_argument("--config_index", required=True, type=int, help="L'indice della configurazione da testare all'interno del tipo di test.")
    
    args = parser.parse_args()
    main(args)