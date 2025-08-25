import pandas as pd
import matplotlib.pyplot as plt
import os
import glob

def load_and_combine_data(data_directory="experiment_data"):
    # ... (questa funzione rimane identica) ...
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
    Prende il DataFrame completo e genera i grafici di base e avanzati.
    """
    if df is None:
        return

    # --- ANALISI DI CORRETTEZZA (Sempre importante) ---
    # ... (questa parte rimane identica) ...
    num_inconsistent = len(df[df['correttezza_superata'] == False])
    if num_inconsistent > 0:
        print(f"\nATTENZIONE: Trovati {num_inconsistent} run con risultati non consistenti!")
    else:
        print("\nVerifica di coerenza superata: Tutti i run sono consistenti.")
    
    # --- ANALISI SULLA SCALABILITA' (SUITE 'dimensione') ---
    df_dimensione = df[df['id_scenario'].str.startswith('dimensione')].copy()
    if not df_dimensione.empty:
        colonne_da_mediare = [
            'execution_time_OD', 'recursive_calls_OD', 'cache_hits_OD', 
            'total_unique_frontiers_OD', 'pruning_successes_OD', 'max_recursion_depth_OD'
        ]
        avg_dimensione = df_dimensione.groupby('rows')[colonne_da_mediare].mean().reset_index()

        print("\n--- Dati Medi per Test di Dimensione ---")
        print(avg_dimensione)

        # Grafico 1 (Base): Tempo di Esecuzione vs. Dimensione
        plt.figure(figsize=(10, 6))
        plt.plot(avg_dimensione['rows'], avg_dimensione['execution_time_OD'], marker='o', label='Tempo Medio')
        plt.title('Tempo di Esecuzione vs. Dimensione Griglia')
        plt.xlabel('Dimensione (N in griglia NxN)')
        plt.ylabel('Tempo (secondi)')
        plt.grid(True)
        plt.legend()
        plt.savefig("grafico_1_tempo_vs_dimensione.png")
        plt.show()

        # Grafico 2 (Avanzato): Cache Hit Ratio
        # Calcoliamo la nuova colonna per il rapporto
        avg_dimensione['cache_hit_ratio'] = avg_dimensione['cache_hits_OD'] / avg_dimensione['recursive_calls_OD']
        plt.figure(figsize=(10, 6))
        plt.plot(avg_dimensione['rows'], avg_dimensione['cache_hit_ratio'] * 100, marker='s', color='green', label='Cache Hit Ratio')
        plt.title('Efficacia della Cache vs. Dimensione Griglia')
        plt.xlabel('Dimensione (N in griglia NxN)')
        plt.ylabel('Cache Hit Ratio (%)')
        plt.grid(True)
        plt.ylim(0, 100) # La percentuale va da 0 a 100
        plt.legend()
        plt.savefig("grafico_2_cache_vs_dimensione.png")
        print("Grafico 'grafico_2_cache_vs_dimensione.png' salvato.")
        plt.show()

        # Grafico 3 (Avanzato): Pruning Successes
        plt.figure(figsize=(10, 6))
        plt.plot(avg_dimensione['rows'], avg_dimensione['pruning_successes_OD'], marker='^', color='orange', label='Successi Pruning')
        plt.title('Efficacia del Pruning vs. Dimensione Griglia')
        plt.xlabel('Dimensione (N in griglia NxN)')
        plt.ylabel('Numero Medio di Rami Potati')
        plt.grid(True)
        plt.legend()
        plt.savefig("grafico_3_pruning_vs_dimensione.png")
        print("Grafico 'grafico_3_pruning_vs_dimensione.png' salvato.")
        plt.show()

    # --- ANALISI SULL'IMPATTO DEGLI OSTACOLI (SUITE 'ostacoli') ---
    df_ostacoli = df[df['id_scenario'].str.startswith('ostacoli')].copy()
    if not df_ostacoli.empty:
        colonne_da_mediare_ostacoli = ['execution_time_OD', 'max_recursion_depth_OD']
        avg_ostacoli = df_ostacoli.groupby('obstacle_ratio')[colonne_da_mediare_ostacoli].mean().reset_index()

        print("\n--- Dati Medi per Test su Densità Ostacoli ---")
        print(avg_ostacoli)
        
        # Grafico 4 (Avanzato): Profondità Ricorsione
        plt.figure(figsize=(10, 6))
        plt.plot(avg_ostacoli['obstacle_ratio'] * 100, avg_ostacoli['max_recursion_depth_OD'], marker='D', color='purple', label='Profondità Max Ricorsione')
        plt.title('Profondità della Ricerca vs. Densità Ostacoli (Griglia 20x20)')
        plt.xlabel('Percentuale di Ostacoli (%)')
        plt.ylabel('Profondità Massima Media')
        plt.grid(True)
        plt.legend()
        plt.savefig("grafico_4_profondita_vs_ostacoli.png")
        print("Grafico 'grafico_4_profondita_vs_ostacoli.png' salvato.")
        plt.show()


if __name__ == "__main__":
    full_dataframe = load_and_combine_data()
    analyze_and_plot(full_dataframe)