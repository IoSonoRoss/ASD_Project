import pandas as pd
import matplotlib.pyplot as plt
import os
import glob

def load_and_combine_data(data_directory="experiment_data"):
    """
    Carica tutti i file CSV dalla directory dei dati, li unisce in un unico
    DataFrame pandas e lo restituisce.
    """
    csv_files = glob.glob(os.path.join(data_directory, "*.csv"))
    if not csv_files:
        print(f"Nessun file CSV trovato nella cartella '{data_directory}'.")
        print("Assicurati di aver eseguito prima lo script 'experiment.py'.")
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

    print("\n--- Analisi dei Dati ---")
    print("Prime 5 righe del DataFrame completo:")
    print(df.head())
    print(f"\nTotale run analizzate: {len(df)}")
    
    # --- ANALISI DI CORRETTEZZA (Sempre importante) ---
    num_inconsistent = len(df[df['correttezza_superata'] == False])
    if num_inconsistent > 0:
        print(f"\nATTENZIONE: Trovati {num_inconsistent} run con risultati di lunghezza O->D e D->O non consistenti!")
        print(df[df['correttezza_superata'] == False])
    else:
        print("\nVerifica di coerenza superata: Tutti i run hanno prodotto lunghezze O->D e D->O identiche.")

    # --- GRAFICI SULLA SCALABILITA' (SUITE 'dimensione') ---
    df_dimensione = df[df['id_scenario'].str.startswith('dimensione')].copy()
    if not df_dimensione.empty:
        # Specifichiamo le colonne numeriche di cui vogliamo calcolare la media
        colonne_da_mediare = [
            'execution_time_OD', 'recursive_calls_OD', 'cache_hits_OD', 
            'total_unique_frontiers_OD', 'pruning_successes_OD'
        ]
        # Calcolo delle medie per ogni dimensione
        avg_dimensione = df_dimensione.groupby('rows')[colonne_da_mediare].mean().reset_index()

        print("\n--- Dati Medi per Test di Dimensione ---")
        print(avg_dimensione)

        # Grafico 1: Tempo di Esecuzione
        plt.figure(figsize=(12, 8))
        plt.plot(avg_dimensione['rows'], avg_dimensione['execution_time_OD'], marker='o', linestyle='-', label='Tempo Medio Esecuzione')
        plt.title('Tempo di Esecuzione vs. Dimensione Griglia (NxN)', fontsize=16)
        plt.xlabel('Dimensione (N)', fontsize=12)
        plt.ylabel('Tempo Medio (secondi)', fontsize=12)
        plt.grid(True, which='both', linestyle='--')
        plt.xticks(avg_dimensione['rows'])
        plt.legend()
        plt.savefig("grafico_1_tempo_vs_dimensione.png")
        print("\nGrafico 'grafico_1_tempo_vs_dimensione.png' salvato.")
        plt.show()

        # Grafico 2 (Avanzato): Chiamate Ricorsive e Cache Hits
        fig, ax1 = plt.subplots(figsize=(12, 8))
        
        ax1.plot(avg_dimensione['rows'], avg_dimensione['recursive_calls_OD'], marker='s', color='tab:blue', label='Chiamate Ricorsive')
        ax1.set_xlabel('Dimensione (N in una griglia NxN)', fontsize=12)
        ax1.set_ylabel('Numero Medio di Chiamate Ricorsive', color='tab:blue', fontsize=12)
        ax1.tick_params(axis='y', labelcolor='tab:blue')
        ax1.grid(True, linestyle=':')
        
        ax2 = ax1.twinx()
        ax2.plot(avg_dimensione['rows'], avg_dimensione['cache_hits_OD'], marker='^', color='tab:green', linestyle='--', label='Cache Hits')
        ax2.set_ylabel('Numero Medio di Cache Hits', color='tab:green', fontsize=12)
        ax2.tick_params(axis='y', labelcolor='tab:green')
        
        plt.title('Lavoro dell\'Algoritmo e Efficacia della Cache vs. Dimensione', fontsize=16)
        fig.tight_layout()
        # Aggiungiamo la legenda combinando gli handle dei due assi
        lines1, labels1 = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax2.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
        
        plt.savefig("grafico_2_lavoro_vs_dimensione.png")
        print("Grafico 'grafico_2_lavoro_vs_dimensione.png' salvato.")
        plt.show()

    # --- GRAFICI SULL'IMPATTO DEGLI OSTACOLI (SUITE 'ostacoli') ---
    df_ostacoli = df[df['id_scenario'].str.startswith('ostacoli')].copy()
    if not df_ostacoli.empty:
        # Specifichiamo le colonne numeriche di cui vogliamo calcolare la media
        colonne_da_mediare_ostacoli = ['execution_time_OD', 'total_unique_frontiers_OD']
        avg_ostacoli = df_ostacoli.groupby('obstacle_ratio')[colonne_da_mediare_ostacoli].mean().reset_index()

        print("\n--- Dati Medi per Test su Densità Ostacoli ---")
        print(avg_ostacoli)

        # Grafico 3 (Avanzato): Complessità del "Labirinto"
        plt.figure(figsize=(12, 8))
        plt.plot(avg_ostacoli['obstacle_ratio'] * 100, avg_ostacoli['total_unique_frontiers_OD'], marker='D', linestyle='-', color='purple')
        plt.title('Complessità dello Spazio di Ricerca vs. Densità Ostacoli (Griglia 20x20)', fontsize=16)
        plt.xlabel('Percentuale di Ostacoli (%)', fontsize=12)
        plt.ylabel('Numero Medio di Celle di Frontiera Uniche Esplorate', fontsize=12)
        plt.grid(True, which='both', linestyle='--')
        plt.savefig("grafico_3_frontiere_vs_ostacoli.png")
        print("Grafico 'grafico_3_frontiere_vs_ostacoli.png' salvato.")
        plt.show()


if __name__ == "__main__":
    full_dataframe = load_and_combine_data()
    analyze_and_plot(full_dataframe)