import sys
from loader import load_maze, MazeFormatError
from visualizer import print_maze, print_cost
from algorithms import ALGORITHMS


def main() -> None:
    """
    Główna funkcja koordynująca przepływ programu:
    1. Odczytuje argumenty wiersza poleceń (ścieżkę do mapy oraz opcjonalną flagę --blocks).
    2. Wczytuje i waliduje planszę.
    3. Uruchamia wszystkie zarejestrowane algorytmy (BFS, DFS) i wyświetla ich wyniki.
    """
    # Sprawdzenie, czy użytkownik dodał flagę '--blocks' w terminalu (włącza tryb kafelków ██)
    use_blocks = "--blocks" in sys.argv
    # Odfiltrowanie flag zaczynających się od '--', aby pobrać samą ścieżkę do pliku mapy
    args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]

    # Jeśli podano ścieżkę jako argument, używamy jej; w przeciwnym razie bierzemy domyślny plik
    filename = args[0] if args else "./maps/labirynt.txt"

    try:
        maze = load_maze(filename)
        rows, cols = maze.size

        print("=== Labirynt załadowany pomyślnie ===")
        print(f"Plik: {filename}")
        print(f"Rozmiar planszy: {rows} wierszy x {cols} kolumn (łącznie {rows * cols} pól)")
        print(f"Punkt startowy (S): ({maze.start.row}, {maze.start.col})")
        print(f"Punkt docelowy (G): ({maze.goal.row}, {maze.goal.col})\n")

        print("--- Podgląd wczytanej planszy ---")
        print_maze(maze, use_blocks=use_blocks)
        print()

        # Lista przechowująca wyniki poszczególnych algorytmów do końcowego zestawienia
        results = []

        # Pętla przechodzi przez wszystkie algorytmy zarejestrowane w słowniku ALGORITHMS
        for name, algo_func in ALGORITHMS.items():
            print(f"=== Wynik działania algorytmu {name} ===")
            result = algo_func(maze)
            results.append(result)

            print_cost(result)
            print("\nWizualizacja trasy (S-start, G-cel, 1-ściana, 0-wolne, .-odwiedzone, *-ścieżka):")
            print_maze(maze, path=result.path, visited=result.visited, use_blocks=use_blocks)
            print()

        # Zbiorcze porównanie skuteczności przebadanych algorytmów
        print("=== Porównanie algorytmów ===")
        for res in results:
            if res.found:
                status = f"koszt ścieżki = {res.cost}, odwiedzone pola = {len(res.visited)}"
            else:
                status = f"brak ścieżki (odwiedzone pola = {len(res.visited)})"
            print(f"- {res.algorithm_name}: {status}")

    except FileNotFoundError as e:
        print(f"Błąd wejścia/wyjścia: {e}", file=sys.stderr)
        sys.exit(1)
    except MazeFormatError as e:
        print(f"Błąd walidacji formatu: {e}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
