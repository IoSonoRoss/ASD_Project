import pandas as pd
import matplotlib.pyplot as plt
import os
import glob
import numpy as np # Importa numpy per gestire l'infinito
import ast # Per convertire stringhe di tuple in vere tuple
import math # Per calcolare dlib

# Aggiungiamo la funzione dlib qui perche ci serve per l'analisi
def calcola_distanza_libera(origin, destination):
    if not origin or not destination: return float('inf')
    delta_x = abs(origin[1] - destination[1])
    delta_y = abs(origin[0] - destination[0])
    delta_min, delta_max = min(delta_x, delta_y), max(delta_x, delta_y)
    return math.sqrt(2) * delta_min + (delta_max - delta_min)

def load_and_combine_data(data_directory="experiment_data"):
    """
    Carica tutti i file CSV dalla directory dei dati, li unisce in un unico
    DataFrame pandas e lo restituisce.
    """
    csv_files = glob.glob(os.path.join(data_directory, "*.csv"))
    if not csv_files:
        print(f"Nessun file CSV trovato nella cartella '{data_directory}'.")
        return None
    print(f"Trovati {len(csv_files)} file di risultati. Unificazione in corso...")
    df_list = [pd.read_csv(file) for file in csv_files]
    full_df = pd.concat(df_list, ignore_index=True)
    print("Unificazione completata.")
    return full_df

def analyze_and_plot(df):
    """
    Prende il DataFrame completo e genera i grafici per l'analisi.
    """
    if df is None:
        return

    # --- Pre-processing dei dati ---
    # Converti le coordinate da stringa a tupla
    df['origin'] = df['origin'].apply(ast.literal_eval)
    df['destination'] = df['destination'].apply(ast.literal_eval)
    # Calcola la colonna dlib per il grafico di correlazione
    df['dlib'] = df.apply(lambda row: calcola_distanza_libera(row['origin'], row['destination']), axis=1)

    # --- ANALISI DI CORRETTEZZA ---
    num_inconsistent = len(df[df['correttezza_superata'] == False])
    if num_inconsistent > 0:
        print(f"\nATTENZIONE: Trovati {num_inconsistent} run con risultati non consistenti!")
    else:
        print("\nVerifica di coerenza superata: Tutti i run sono consistenti.")
    
    # --- GRAFICI SULLA SCALABILITA' (SUITE 'dimensione') ---
    df_dimensione = df[df['id_scenario'].str.startswith('dimensione')].copy()
    if not df_dimensione.empty:
        colonne_da_mediare = [
            'execution_time_OD', 'recursive_calls_OD', 'cache_hits_OD', 
            'total_unique_frontiers_OD', 'pruning_successes_OD', 'max_recursion_depth_OD'
        ]
        avg_dimensione = df_dimensione.groupby('rows')[colonne_da_mediare].mean().reset_index()

        print("\n--- Dati Medi per Test di Dimensione ---")
        print(avg_dimensione)

        # Grafico 1: Tempo di Esecuzione vs. Dimensione
        plt.figure(figsize=(10, 6)); plt.plot(avg_dimensione['rows'], avg_dimensione['execution_time_OD'], marker='o'); plt.title('Tempo Medio di Esecuzione vs. Dimensione Griglia'); plt.xlabel('Dimensione (N)'); plt.ylabel('Tempo (secondi)'); plt.grid(True); plt.savefig("grafico_1_tempo_vs_dimensione.png"); plt.show()

        # Grafico 2: Lavoro dell'Algoritmo vs. Dimensione (Chiamate e Cache)
        fig, ax1 = plt.subplots(figsize=(10, 6)); ax1.plot(avg_dimensione['rows'], avg_dimensione['recursive_calls_OD'], marker='s', color='tab:blue', label='Chiamate Ricorsive'); ax1.set_xlabel('Dimensione (N)'); ax1.set_ylabel('Numero Medio Chiamate Ricorsive', color='tab:blue'); ax2 = ax1.twinx(); ax2.plot(avg_dimensione['rows'], avg_dimensione['cache_hits_OD'], marker='^', color='tab:green', linestyle='--', label='Cache Hits'); ax2.set_ylabel('Numero Medio Cache Hits', color='tab:green'); plt.title('Lavoro Algoritmo e Efficacia Cache vs. Dimensione'); fig.legend(loc="upper left", bbox_to_anchor=(0.1,0.9)); plt.savefig("grafico_2_lavoro_vs_dimensione.png"); plt.show()

        # Grafico 3: Correlazione Distanza vs. Difficolta
        plt.figure(figsize=(10, 6)); plt.scatter(df_dimensione['dlib'], df_dimensione['execution_time_OD'], alpha=0.5); plt.title('Correlazione tra Distanza Libera e Tempo di Esecuzione'); plt.xlabel('Distanza Libera (dlib)'); plt.ylabel('Tempo di Esecuzione (secondi)'); plt.grid(True); plt.savefig("grafico_3_correlazione_distanza_tempo.png"); plt.show()

    # --- GRAFICI SULL'IMPATTO DEGLI OSTACOLI (SUITE 'ostacoli') ---
    df_ostacoli = df[df['id_scenario'].str.startswith('ostacoli')].copy()
    if not df_ostacoli.empty:
        # Calcola la percentuale di successo
        df_ostacoli['success'] = (df_ostacoli['lunghezza_OD'] != np.inf).astype(int)
        colonne_da_mediare_ostacoli = ['execution_time_OD', 'max_recursion_depth_OD', 'success']
        avg_ostacoli = df_ostacoli.groupby('obstacle_ratio')[colonne_da_mediare_ostacoli].mean().reset_index()

        print("\n--- Dati Medi per Test su Densità Ostacoli ---")
        print(avg_ostacoli)
        
        # Grafico 4: Tempo di Esecuzione vs. % Ostacoli (Curva a Campana)
        plt.figure(figsize=(10, 6)); plt.plot(avg_ostacoli['obstacle_ratio'] * 100, avg_ostacoli['execution_time_OD'], marker='o', color='red'); plt.title('Tempo Medio di Esecuzione vs. Densità Ostacoli (15x15)'); plt.xlabel('Percentuale di Ostacoli (%)'); plt.ylabel('Tempo Medio (secondi)'); plt.grid(True); plt.savefig("grafico_4_tempo_vs_ostacoli.png"); plt.show()
        
        # Grafico 5: Probabilita di Successo vs. % Ostacoli
        plt.figure(figsize=(10, 6)); plt.plot(avg_ostacoli['obstacle_ratio'] * 100, avg_ostacoli['success'] * 100, marker='o', color='teal'); plt.title('Probabilità di Successo vs. Densità Ostacoli (15x15)'); plt.xlabel('Percentuale di Ostacoli (%)'); plt.ylabel('Percentuale di Run con Soluzione (%)'); plt.grid(True); plt.ylim(0, 105); plt.savefig("grafico_5_successo_vs_ostacoli.png"); plt.show()

        # Grafico 6: Profondita della Ricerca vs. % Ostacoli
        plt.figure(figsize=(10, 6)); plt.plot(avg_ostacoli['obstacle_ratio'] * 100, avg_ostacoli['max_recursion_depth_OD'], marker='D', color='purple'); plt.title('Profondità Media della Ricerca vs. Densità Ostacoli (15x15)'); plt.xlabel('Percentuale di Ostacoli (%)'); plt.ylabel('Profondità Massima Media'); plt.grid(True); plt.savefig("grafico_6_profondita_vs_ostacoli.png"); plt.show()

if __name__ == "__main__":
    full_dataframe = load_and_combine_data()
    analyze_and_plot(full_dataframe)