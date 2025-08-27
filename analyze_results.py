import pandas as pd
import matplotlib.pyplot as plt
import os
import glob
import numpy as np
import ast
import math

def calcola_distanza_libera(origin, destination):
    """Calcola la distanza libera tra due punti."""
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
    Prende il DataFrame completo, genera i grafici per l'analisi e
    salva le tabelle riassuntive su file CSV.
    """
    if df is None:
        return

    analysis_output_dir = "analysis_results"
    os.makedirs(analysis_output_dir, exist_ok=True)

    # --- Pre-processing dei dati ---
    # Questa sezione si applica a tutti i dati, ma alcune colonne potrebbero non esistere
    # in tutti i file (es. i file di confronto non hanno 'correttezza_superata').
    # Gestiamo questi casi con dei controlli.
    if 'origin' in df.columns:
        df['origin'] = df['origin'].apply(lambda x: ast.literal_eval(str(x)))
    if 'destination' in df.columns:
        df['destination'] = df['destination'].apply(lambda x: ast.literal_eval(str(x)))
    if 'origin' in df.columns and 'destination' in df.columns:
        df['dlib'] = df.apply(lambda row: calcola_distanza_libera(row['origin'], row['destination']), axis=1)

    # --- ANALISI DI CORRETTEZZA (solo se la colonna esiste) ---
    if 'correttezza_superata' in df.columns:
        num_inconsistent = len(df[df['correttezza_superata'] == False])
        if num_inconsistent > 0:
            print(f"\nATTENZIONE: Trovati {num_inconsistent} run con risultati non consistenti!")
        else:
            print("\nVerifica di coerenza superata: Tutti i run sono consistenti.")
    
    # --- GRAFICI SULLA SCALABILITA' (SUITE 'dimensione') ---
    df_dimensione = df[df['id_scenario'].str.startswith('dimensione', na=False)].copy()
    if not df_dimensione.empty:
        colonne_da_mediare = [
            'execution_time_OD', 'recursive_calls_OD', 'cache_hits_OD', 
            'total_unique_frontiers_OD', 'pruning_successes_OD', 'max_recursion_depth_OD'
        ]
        avg_dimensione = df_dimensione.groupby('rows')[colonne_da_mediare].mean().reset_index()

        print("\n--- Dati Medi per Test di Dimensione ---")
        print(avg_dimensione)

        table_filename_dim = os.path.join(analysis_output_dir, "tabella_analisi_dimensione.csv")
        avg_dimensione.to_csv(table_filename_dim, index=False, float_format='%.4f')
        print(f"Tabella di analisi sulla dimensione salvata in: {table_filename_dim}")

        # Generazione grafici dimensione (codice invariato)
        plt.figure(figsize=(10, 6)); plt.plot(avg_dimensione['rows'], avg_dimensione['execution_time_OD'], marker='o'); plt.title('Tempo Medio di Esecuzione vs. Dimensione Griglia'); plt.xlabel('Dimensione (N)'); plt.ylabel('Tempo (secondi)'); plt.grid(True); plt.savefig(os.path.join(analysis_output_dir, "grafico_1_tempo_vs_dimensione.png")); plt.show()
        fig, ax1 = plt.subplots(figsize=(10, 6)); ax1.plot(avg_dimensione['rows'], avg_dimensione['recursive_calls_OD'], marker='s', color='tab:blue', label='Chiamate Ricorsive'); ax1.set_xlabel('Dimensione (N)'); ax1.set_ylabel('Numero Medio Chiamate Ricorsive', color='tab:blue'); ax2 = ax1.twinx(); ax2.plot(avg_dimensione['rows'], avg_dimensione['cache_hits_OD'], marker='^', color='tab:green', linestyle='--', label='Cache Hits'); ax2.set_ylabel('Numero Medio Cache Hits', color='tab:green'); plt.title('Lavoro Algoritmo e Efficacia Cache vs. Dimensione'); fig.legend(loc="upper left", bbox_to_anchor=(0.1,0.9)); plt.savefig(os.path.join(analysis_output_dir, "grafico_2_lavoro_vs_dimensione.png")); plt.show()
        if 'dlib' in df_dimensione.columns:
            plt.figure(figsize=(10, 6)); plt.scatter(df_dimensione['dlib'], df_dimensione['execution_time_OD'], alpha=0.5); plt.title('Correlazione tra Distanza Libera e Tempo di Esecuzione'); plt.xlabel('Distanza Libera (dlib)'); plt.ylabel('Tempo di Esecuzione (secondi)'); plt.grid(True); plt.savefig(os.path.join(analysis_output_dir, "grafico_3_correlazione_distanza_tempo.png")); plt.show()

    # --- GRAFICI SULL'IMPATTO DEGLI OSTACOLI (SUITE 'ostacoli') ---
    df_ostacoli = df[df['id_scenario'].str.startswith('ostacoli', na=False)].copy()
    if not df_ostacoli.empty:
        df_ostacoli['success'] = (df_ostacoli['lunghezza_OD'] != np.inf).astype(int)
        colonne_da_mediare_ostacoli = ['execution_time_OD', 'max_recursion_depth_OD', 'success']
        avg_ostacoli = df_ostacoli.groupby('obstacle_ratio')[colonne_da_mediare_ostacoli].mean().reset_index()

        print("\n--- Dati Medi per Test su Densità Ostacoli ---")
        print(avg_ostacoli)
        
        table_filename_obs = os.path.join(analysis_output_dir, "tabella_analisi_ostacoli.csv")
        avg_ostacoli.to_csv(table_filename_obs, index=False, float_format='%.4f')
        print(f"Tabella di analisi sugli ostacoli salvata in: {table_filename_obs}")
        
        # Generazione grafici ostacoli (codice invariato)
        plt.figure(figsize=(10, 6)); plt.plot(avg_ostacoli['obstacle_ratio'] * 100, avg_ostacoli['execution_time_OD'], marker='o', color='red'); plt.title('Tempo Medio di Esecuzione vs. Densità Ostacoli (15x15)'); plt.xlabel('Percentuale di Ostacoli (%)'); plt.ylabel('Tempo Medio (secondi)'); plt.grid(True); plt.savefig(os.path.join(analysis_output_dir, "grafico_4_tempo_vs_ostacoli.png")); plt.show()
        plt.figure(figsize=(10, 6)); plt.plot(avg_ostacoli['obstacle_ratio'] * 100, avg_ostacoli['success'] * 100, marker='o', color='teal'); plt.title('Probabilità di Successo vs. Densità Ostacoli (15x15)'); plt.xlabel('Percentuale di Ostacoli (%)'); plt.ylabel('Percentuale di Run con Soluzione (%)'); plt.grid(True); plt.ylim(0, 105); plt.savefig(os.path.join(analysis_output_dir, "grafico_5_successo_vs_ostacoli.png")); plt.show()
        plt.figure(figsize=(10, 6)); plt.plot(avg_ostacoli['obstacle_ratio'] * 100, avg_ostacoli['max_recursion_depth_OD'], marker='D', color='purple'); plt.title('Profondità Media della Ricerca vs. Densità Ostacoli (15x15)'); plt.xlabel('Percentuale di Ostacoli (%)'); plt.ylabel('Profondità Massima Media'); plt.grid(True); plt.savefig(os.path.join(analysis_output_dir, "grafico_6_profondita_vs_ostacoli.png")); plt.show()

    # --- NUOVO: GRAFICO DI CONFRONTO (SUITE 'confronto') ---
    df_confronto = df[df['id_scenario'].str.startswith('confronto', na=False)].copy()
    if not df_confronto.empty:
        # Calcola la media dei tempi per ogni dimensione e tipo (ottimizzato vs. naive)
        avg_confronto_series = df_confronto.groupby(['rows', 'type'])['execution_time'].mean()
        avg_confronto_df = avg_confronto_series.unstack()

        print("\n--- Dati Medi per Test di Confronto ---")
        print(avg_confronto_df)

        # --- NUOVO: ESPORTA LA TABELLA DI CONFRONTO SU CSV ---
        table_filename_comp = os.path.join(analysis_output_dir, "tabella_analisi_confronto.csv")
        # Usiamo .to_csv() direttamente sul DataFrame pivotato
        avg_confronto_df.to_csv(table_filename_comp, float_format='%.6f') # Usiamo piu decimali per i tempi piccoli
        print(f"Tabella di analisi sul confronto salvata in: {table_filename_comp}")
        
        # --- Logica di plotting (rimane invariata) ---
        colori = {
            'naive': '#C70039',
            'ottimizzato': '#1E8449'
        }
        
        avg_confronto_df.plot(
            kind='bar', 
            figsize=(12, 8), 
            color=[colori[col] for col in avg_confronto_df.columns],
            logy=True,
            edgecolor='black',
            linewidth=0.7
        )
        
        plt.title('Confronto Performance: Versione Ottimizzata vs. Naive (Scala Logaritmica)', fontsize=16)
        plt.xlabel('Dimensione Griglia (NxN)', fontsize=12)
        plt.ylabel('Tempo Medio di Esecuzione (secondi)', fontsize=12)
        plt.xticks(rotation=0, fontsize=10)
        plt.yticks(fontsize=10)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.legend(title='Versione Algoritmo', fontsize=11)
        plt.tight_layout()
        plt.savefig(os.path.join(analysis_output_dir, "grafico_7_confronto_versioni.png"))
        plt.show()


if __name__ == "__main__":
    full_dataframe = load_and_combine_data()
    analyze_and_plot(full_dataframe)