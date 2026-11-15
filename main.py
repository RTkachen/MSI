import sys
from pathlib import Path
from loader import load_maze, MazeFormatError
from algorithms import run_all_configurations
from gui import MazeGUI
from visualizer import print_maze, print_cost


def print_comparison_table(results) -> None:
    """Wyświetla w terminalu sformatowaną tabelę wyników."""
    header = f"{'Konfiguracja algorytmu':<35} | {'Koszt':>7} | {'Liczba stanów':>14} | {'Czas [ms]':>10}"
    print("=" * len(header))
    print(header)
    print("-" * len(header))

    for res in results:
        cost_str = str(res.cost) if res.found else "Brak"
        print(
            f"{res.algorithm_name:<35} | "
            f"{cost_str:>7} | "
            f"{len(res.visited):>14} | "
            f"{res.execution_time_ms:>10.3f}"
        )
    print("=" * len(header))


def main() -> None:
    # 1. Odczyt flag z wiersza poleceń
    has_gui = "--gui" in sys.argv
    has_terminal = "--terminal" in sys.argv
    has_blocks = "--blocks" in sys.argv

    # GUI uruchamia się domyślnie, CHYBA ŻE wybrano terminal/bloczki bez jawnej flagi --gui
    open_gui = has_gui or not (has_terminal or has_blocks)
    show_terminal = has_terminal or has_blocks

    # 2. Odczyt nazwy pliku
    args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]
    raw_filename = args[0] if args else "labirynt.txt"

    # Logika dopasowania folderu: jeśli podano samą nazwę (bez ukośników), szukamy w maps/
    path_obj = Path(raw_filename)
    if not path_obj.parent.name and not path_obj.exists():
        filepath = Path("maps") / raw_filename
    else:
        filepath = path_obj

    try:
        maze = load_maze(filepath)
        rows, cols = maze.size

        print(f"Załadowano plik: {filepath} ({rows}x{cols}), Start={maze.start}, Cel={maze.goal}\n")

        # Uruchomienie wszystkich konfiguracji (BFS, DFS, A*)
        results = run_all_configurations(maze)

        # Wypisanie tabeli podsumowującej do sprawozdania
        print_comparison_table(results)

        # 3. Wyświetlanie w terminalu (jeśli zażądano)
        if show_terminal:
            print("\n--- Wizualizacja w terminalu ---")
            for res in results:
                print_cost(res)
                print_maze(maze, path=res.path, visited=res.visited, use_blocks=has_blocks)
                print("-" * 60 + "\n")

        # 4. Otwarcie interaktywnego okna z wizualizacją
        if open_gui:
            print("\nOtwieranie okna wizualizacji GUI... (zamknij okno, aby zakończyć program)")
            app = MazeGUI(maze, results)
            app.run()

    except FileNotFoundError as e:
        print(f"Błąd wejścia/wyjścia: {e}", file=sys.stderr)
        sys.exit(1)
    except MazeFormatError as e:
        print(f"Błąd walidacji formatu: {e}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
