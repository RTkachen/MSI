import random
import sys
from pathlib import Path
from typing import List, Tuple


def generate_complex_maze(
    rows: int = 101,
    cols: int = 101,
    loop_factor: float = 0.18,
    add_traps: bool = True,
    seed: int | None = None,
) -> List[List[str]]:
    """
    Generuje duży, skomplikowany labirynt ze 100% gwarancją istnienia ścieżki od S do G.

    Parametry:
    - rows, cols: wymiary planszy (najlepiej liczby nieparzyste, np. 101x101).
    - loop_factor: odsetek dodatkowych przejść (0.0 = jedna ścieżka, 0.18 = dużo alternatywnych dróg o różnym koszcie).
    - add_traps: czy dodać wklęsłe bariery ("kieszenie") utrudniające zachłanną eksplorację.
    - seed: ziarno generatora losowego (pozwala odtworzyć dokładnie tę samą mapę).
    """
    if seed is not None:
        random.seed(seed)

    # Wymuszenie nieparzystych wymiarów dla poprawnego działania siatki korytarzy
    rows = rows if rows % 2 == 1 else rows + 1
    cols = cols if cols % 2 == 1 else cols + 1

    # KROK 1: Inicjalizacja planszy samymi przeszkodami '1'
    grid: List[List[str]] = [["1" for _ in range(cols)] for _ in range(rows)]

    # KROK 2: Generowanie labiryntu doskonałego (Randomized DFS na siatce o kroku 2)
    # Daje 100% gwarancję spójności (z każdego korytarza da się dojść w każde inne miejsce).
    start_r, start_c = 1, 1
    grid[start_r][start_c] = "0"
    stack: List[Tuple[int, int]] = [(start_r, start_c)]

    directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]

    while stack:
        r, c = stack[-1]
        # Szukamy sąsiadów oddalonych o 2 pola, którzy są jeszcze całkowicie zamurowani ('1')
        unvisited_neighbors = []
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 1 <= nr < rows - 1 and 1 <= nc < cols - 1 and grid[nr][nc] == "1":
                unvisited_neighbors.append((nr, nc, r + dr // 2, c + dc // 2))

        if unvisited_neighbors:
            # Wybieramy losowego sąsiada i przebijamy ścianę pomiędzy nimi
            nr, nc, wall_r, wall_c = random.choice(unvisited_neighbors)
            grid[wall_r][wall_c] = "0"
            grid[nr][nc] = "0"
            stack.append((nr, nc))
        else:
            stack.pop()

    # KROK 3: Dodawanie pułapek heurystycznych (ukośnych barier zmuszających do objazdów)
    # Zanim wyburzymy losowe ściany, możemy wstawić kilka większych komór/przeszkód,
    # a potem upewnić się, że spójność nie została naruszona.
    if add_traps and rows >= 31 and cols >= 31:
        _carve_open_chambers(grid, rows, cols)

    # KROK 4: Braiding (wyburzanie części wewnętrznych ścian w celu stworzenia wielu alternatywnych ścieżek)
    # Dzięki temu BFS / A*(beta=1) szuka idealnego skrótu przez tysiące stanów,
    # a A*(beta=5) biegnie pierwszą napotkaną drogą do celu.
    for r in range(2, rows - 2):
        for c in range(2, cols - 2):
            if grid[r][c] == "1":
                # Sprawdzamy, czy ściana rozdziela dwa poziome lub dwa pionowe korytarze
                horizontal_bridge = grid[r][c - 1] == "0" and grid[r][c + 1] == "0"
                vertical_bridge = grid[r - 1][c] == "0" and grid[r + 1][c] == "0"
                if (horizontal_bridge or vertical_bridge) and random.random() < loop_factor:
                    grid[r][c] = "0"

    # KROK 5: Ustawienie punktu startowego S w lewym górnym rogu i celu G w prawym dolnym rogu
    grid[1][1] = "S"
    grid[rows - 2][cols - 2] = "G"

    return grid


def _carve_open_chambers(grid: List[List[str]], rows: int, cols: int) -> None:
    """
    Tworzy na mapie kilka otwartych komnat (np. 5x5 z pustych pól '0').
    Otwarte przestrzenie drastycznie zwiększają liczbę stanów badanych przez algorytmy
    z małym beta (np. beta=0 lub beta=0.1), podczas gdy duże beta przecina je po linii prostej.
    """
    num_chambers = max(3, (rows * cols) // 800)
    for _ in range(num_chambers):
        cr = random.randint(3, rows - 8)
        cc = random.randint(3, cols - 8)
        for r in range(cr, cr + 5):
            for c in range(cc, cc + 5):
                grid[r][c] = "0"


def save_maze_to_file(grid: List[List[str]], filepath: str | Path) -> None:
    """Zapisuje wygenerowaną siatkę do pliku tekstowego ze spacjami między symbolami."""
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in grid:
            f.write(" ".join(row) + "\n")


if __name__ == "__main__":
    # Obsługiwane sposoby wywołania z terminala:
    # 1. python generator.py                  -> domyślnie 101x101 -> maps/hard_101x101.txt
    # 2. python generator.py 81               -> kwadrat 81x81   -> maps/hard_81x81.txt
    # 3. python generator.py 51 151           -> prostokąt 51x151 -> maps/hard_51x151.txt
    # 4. python generator.py 51 151 moja.txt  -> prostokąt 51x151 -> maps/moja.txt

    args = sys.argv[1:]

    if len(args) == 0:
        rows, cols = 101, 101
        out_name = f"hard_{rows}x{cols}.txt"
    elif len(args) == 1:
        # Podano tylko jeden wymiar -> tworzymy mapę kwadratową
        rows = cols = int(args[0])
        out_name = f"hard_{rows}x{cols}.txt"
    else:
        # Podano dwa wymiary (wiersze oraz kolumny) -> tworzymy mapę prostokątną
        rows = int(args[0])
        cols = int(args[1])
        # Jeśli podano trzeci argument, traktujemy go jako nazwę pliku wyjściowego
        out_name = args[2] if len(args) > 2 else f"hard_{rows}x{cols}.txt"

    out_path = Path("maps") / out_name

    maze_grid = generate_complex_maze(rows=rows, cols=cols, loop_factor=0.18, add_traps=True)
    save_maze_to_file(maze_grid, out_path)
    print(f"Wygenerowano labirynt ({len(maze_grid)} wierszy x {len(maze_grid[0])} kolumn) -> {out_path}")
