import argparse
import pandas as pd
import random
import time
import math
import os
import csv

# Importa i moduli del progetto refattorizzato
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

    # Tenta di scegliere O e D in quadranti opposti per massimizzare la distanza
    quadrant1 = [cell for cell in free_cells if cell[0] < rows / 2 and cell[1] < cols / 2]
    quadrant4 = [cell for cell in free_cells if cell[0] > rows / 2 and cell[1] > cols / 2]
    
    if quadrant1 and quadrant4:
        origin = random.choice(quadrant1)
        destination = random.choice(quadrant4)
        return origin, destination
    else:
        # Fallback se i quadranti sono vuoti o per griglie piccole
        return random.sample(free_cells, 2)

def run_single_run(grid_data, origin, destination):
    """
    Esegue un test usando PathfindingSolver e recupera le statistiche.
    Include la verifica di correttezza D->O.
    """
    results = {}

    # --- Test O -> D ---
    print(f"    Esecuzione CAMMINOMIN({origin}, {destination})...")
    solver_od = PathfindingSolver(grid_data, origin, destination)
    solver_od.solve() 
    stats_od = solver_od.get_stats_summary()
    results['lunghezza_OD'] = solver_od.lunghezza_minima
    results.update({f"{key}_OD": val for key, val in stats_od.items()})

    # --- Test D -> O (Correttezza) ---
    print(f"    Esecuzione CAMMINOMIN({destination}, {origin})...")
    solver_do = PathfindingSolver(grid_data, destination, origin)
    solver_do.solve()
    stats_do = solver_do.get_stats_summary()
    results['lunghezza_DO'] = solver_do.lunghezza_minima
    results.update({f"{key}_DO": val for key, val in stats_do.items()})
    
    # Verifica coerenza
    lung_od, lung_do = results['lunghezza_OD'], results['lunghezza_DO']
    results['correttezza_superata'] = math.isclose(lung_od, lung_do) if lung_od != float('inf') else lung_do == float('inf')

    return results

def main(args):
    """Script principale per l'esecuzione degli esperimenti."""
    
    scenari_dimensione = [
        {"rows": 10, "cols": 10, "obstacle_ratio": 0.25, "num_runs": 5},
        {"rows": 15, "cols": 15, "obstacle_ratio": 0.25, "num_runs": 5},
        {"rows": 20, "cols": 20, "obstacle_ratio": 0.25, "num_runs": 3},
        {"rows": 25, "cols": 25, "obstacle_ratio": 0.25, "num_runs": 2},
    ]
    scenari_ostacoli = [
        {"rows": 20, "cols": 20, "obstacle_ratio": 0.15, "num_runs": 5},
        {"rows": 20, "cols": 20, "obstacle_ratio": 0.30, "num_runs": 5},
        {"rows": 20, "cols": 20, "obstacle_ratio": 0.45, "num_runs": 3},
    ]
    scenario_map = {"dimensione": scenari_dimensione, "ostacoli": scenari_ostacoli}
    
    test_type = args.test_type
    config_index = args.config_index
    
    if test_type not in scenario_map or not (0 <= config_index < len(scenario_map[test_type])):
        print(f"Errore: tipo di test '{test_type}' o indice '{config_index}' non validi.")
        return

    config = scenario_map[test_type][config_index]
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
            
        risultati_run = run_single_run(grid_data, origin, destination)
        
        record_completo = {**config, "run_num": i + 1, "origin": origin, "destination": destination, **risultati_run}
        lista_risultati_run.append(record_completo)

    if lista_risultati_run:
        output_dir = "experiment_data"
        os.makedirs(output_dir, exist_ok=True)
        output_filename = os.path.join(output_dir, f"results_{config['id_scenario']}.csv")
        
        # Scrittura del CSV
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
    parser.add_argument("--test_type", required=True, choices=["dimensione", "ostacoli"], help="Il tipo di esperimento da eseguire.")
    parser.add_argument("--config_index", required=True, type=int, help="L'indice della configurazione da testare all'interno del tipo di test.")
    
    args = parser.parse_args()
    main(args)