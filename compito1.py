import grid_utils

def main():
    rows = int(input("Inserisci il numero di righe della gridmap: "))
    cols = int(input("Inserisci il numero di colonne della gridmap: "))
    num_obstacles_input = input("Inserisci il numero di ostacoli (premi invio per usare la percentuale predefinita): ")
    if num_obstacles_input.strip() == "":
        grid = grid_utils.generate_grid_map(rows, cols)
    else:
        num_obstacles = int(num_obstacles_input)
        grid = grid_utils.generate_grid_map(rows, cols, num_obstacles=num_obstacles)
    grid_utils.print_grid(grid)
    
    grid_utils.visualizza_gridmap_pcolormesh(grid)

if __name__ == "__main__":
    main()