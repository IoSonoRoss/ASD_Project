import pandas as pd
import matplotlib.pyplot as plt
import os
import glob # Utile per trovare file che corrispondono a un pattern

def load_and_combine_data(data_directory="experiment_data"):
    """
    Carica tutti i file CSV dalla directory dei dati, li unisce in un unico
    DataFrame pandas e lo restituisce.
    """
    # Cerca tutti i file .csv nella cartella specificata
    csv_files = glob.glob(os.path.join(data_directory, "*.csv"))
    
    if not csv_files:
        print(f"Nessun file CSV trovato nella cartella '{data_directory}'.")
        print("Assicurati di aver eseguito prima lo script 'experiment.py'.")
        return None

    print(f"Trovati {len(csv_files)} file di risultati. Unificazione in corso...")

    # Leggi ogni file CSV in un DataFrame e mettili in una lista
    df_list = [pd.read_csv(file) for file in csv_files]
    
    # Concatena tutti i DataFrame in uno solo
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
    
    # --- ANALISI 1: SCALABILITA' SULLA DIMENSIONE ---
    df_dimensione = df[df['id_scenario'].str.startswith('dimensione')].copy()
    
    # --- CORREZIONE QUI ---
    # Usiamo 'execution_time_OD' invece di 'tempo_OD'
    avg_dimensione = df_dimensione.groupby('rows')['execution_time_OD'].mean().reset_index()

    plt.figure(figsize=(10, 6))
    plt.plot(avg_dimensione['rows'], avg_dimensione['execution_time_OD'], marker='o', linestyle='-', color='b')
    plt.title('Tempo Medio di Esecuzione vs. Dimensione Griglia (NxN)')
    plt.xlabel('Dimensione (N)')
    plt.ylabel('Tempo Medio (secondi)')
    plt.grid(True, which='both', linestyle='--')
    plt.xticks(avg_dimensione['rows'])
    plt.savefig("grafico_scalabilita_dimensione.png")
    print("\nGrafico 'grafico_scalabilita_dimensione.png' salvato.")
    plt.show()

    # --- ANALISI 2: IMPATTO DEGLI OSTACOLI ---
    df_ostacoli = df[df['id_scenario'].str.startswith('ostacoli')].copy()

    # --- CORREZIONE QUI ---
    # Usiamo 'execution_time_OD' anche qui
    avg_ostacoli = df_ostacoli.groupby('obstacle_ratio')['execution_time_OD'].mean().reset_index()

    plt.figure(figsize=(10, 6))
    plt.plot(avg_ostacoli['obstacle_ratio'] * 100, avg_ostacoli['execution_time_OD'], marker='s', linestyle='-', color='r')
    plt.title('Tempo Medio di Esecuzione vs. Densità Ostacoli (Griglia 20x20)')
    plt.xlabel('Percentuale di Ostacoli (%)')
    plt.ylabel('Tempo Medio (secondi)')
    plt.grid(True, which='both', linestyle='--')
    plt.savefig("grafico_impatto_ostacoli.png")
    print("Grafico 'grafico_impatto_ostacoli.png' salvato.")
    plt.show()
    
    # --- ANALISI 3: VERIFICA CORRETTEZZA ---
    num_inconsistent = len(df[df['correttezza_superata'] == False])
    if num_inconsistent > 0:
        print(f"\nATTENZIONE: Trovati {num_inconsistent} run con risultati di lunghezza O->D e D->O non consistenti!")
    else:
        print("\nVerifica di coerenza superata: Tutti i run hanno prodotto lunghezze O->D e D->O identiche.")


if __name__ == "__main__":
    full_dataframe = load_and_combine_data()
    analyze_and_plot(full_dataframe)