import os
from typing import Iterable, Optional
from models import Maze, Point, SearchResult

# Włączenie natywnej obsługi kolorów ANSI w terminalu systemu Windows (CMD / PowerShell)
os.system("")


class Colors:
    """Kody sterujące ANSI nadające kolory i style znakom w terminalu."""
    RESET = "\033[0m"           # Przywrócenie domyślnego koloru terminala
    DIM_GRAY = "\033[90m"       # Przygaszony ciemnoszary (dla wolnych pól '0', aby nie męczyły wzroku)
    WALL = "\033[38;5;240m"     # Wyraźny grafitowy dla przeszkód ('1')
    VISITED = "\033[36m"        # Cyjan / jasnoniebieski dla pól odwiedzonych ('.')
    PATH = "\033[1;93m"         # Pogrubiony jaskrawożółty dla ostatecznej ścieżki agenta ('*')
    START = "\033[1;97;42m"     # Biała pogrubiona litera S na zielonym tle
    GOAL = "\033[1;97;41m"      # Biała pogrubiona litera G na czerwonym tle
    HEADER = "\033[38;5;245m"   # Kolor dla numeracji wierszy i kolumn na brzegach mapy


# Parametry 'path' i 'visited' mają typ Optional[Iterable[Point]] = None, co oznacza:
# - są opcjonalne (domyślnie mają wartość None, gdy chcemy wyświetlić samą czystą mapę),
# - można do nich przekazać dowolną kolekcję punktów (listę, zbiór, krotkę), po której da się iterować.
def print_maze(
    maze: Maze,
    path: Optional[Iterable[Point]] = None,
    visited: Optional[Iterable[Point]] = None,
    use_colors: bool = True,
    use_blocks: bool = False,
) -> None:
    """
    Wyświetla planszę labiryntu w terminalu z kolorowaniem oraz indeksami wierszy/kolumn.
    - use_colors=True: koloruje wymagane znaki (S, G, 1, 0, ., *), znacznie poprawiając czytelność.
    - use_blocks=True: zamienia znaki na jednolite, połączone kafelki graficzne 2x1 (██).
    """
    path_set = set(path) if path else set()
    visited_set = set(visited) if visited else set()

    # W trybie blokowym łączymy kolumny bez spacji (""), a w tekstowym ze spacją (" ").
    # Dzięki temu każde pole w obu trybach zajmuje dokładnie 2 znaki szerokości w terminalu.
    sep = "" if use_blocks else " "

    # Nagłówek kolumn: każdy indeks zajmuje 2 znaki szerokości, dopasowując się do kafelków pod spodem
    col_header = "".join(f"{c % 10:2d}" for c in range(maze.cols))

    if use_colors:
        print(f"{Colors.HEADER}   {col_header}{Colors.RESET}")
        print(f"{Colors.HEADER}   +{'-' * len(col_header)}+{Colors.RESET}")
    else:
        print(f"   {col_header}")
        print(f"   +{'-' * len(col_header)}+")

    for r in range(maze.rows):
        row_symbols: list[str] = []
        for c in range(maze.cols):
            pos = Point(r, c)
            cell = maze.grid[r][c]

            # W trybie blokowym każdy symbol ma dokładnie 2 znaki szerokości,
            # a przy sklejaniu za pomocą "" ściany '██' tworzą ciągły mur bez przerw.
            if cell == "S":
                sym = " S" if use_blocks else "S"
                row_symbols.append(f"{Colors.START}{sym}{Colors.RESET}" if use_colors else sym)
            elif cell == "G":
                sym = " G" if use_blocks else "G"
                row_symbols.append(f"{Colors.GOAL}{sym}{Colors.RESET}" if use_colors else sym)
            elif pos in path_set:
                sym = " *" if use_blocks else "*"
                row_symbols.append(f"{Colors.PATH}{sym}{Colors.RESET}" if use_colors else sym)
            elif pos in visited_set:
                sym = " ·" if use_blocks else "."
                row_symbols.append(f"{Colors.VISITED}{sym}{Colors.RESET}" if use_colors else sym)
            elif cell == "1":
                sym = "██" if use_blocks else "1"
                row_symbols.append(f"{Colors.WALL}{sym}{Colors.RESET}" if use_colors else sym)
            else:  # Wolne pole '0'
                sym = "  " if use_blocks else "0"
                row_symbols.append(f"{Colors.DIM_GRAY}{sym}{Colors.RESET}" if use_colors else sym)

        row_prefix = f"{Colors.HEADER}{r:2d} |{Colors.RESET}" if use_colors else f"{r:2d} |"
        row_suffix = f"{Colors.HEADER}|{Colors.RESET}" if use_colors else "|"

        # Sklejenie wiersza: dla use_blocks używamy sep="" (brak odstępów między blokami)
        print(f"{row_prefix}{sep.join(row_symbols)}{row_suffix}")

    # Dolna ramka zamykająca planszę
    if use_colors:
        print(f"{Colors.HEADER}   +{'-' * len(col_header)}+{Colors.RESET}")
    else:
        print(f"   +{'-' * len(col_header)}+")


def print_cost(result: SearchResult) -> None:
    """Wypisuje podsumowanie kosztu ścieżki oraz liczby sprawdzonych stanów dla danego algorytmu."""
    print(f"Algorytm: {result.algorithm_name}")
    if result.found:
        print(f"  Status:            Znaleziono ścieżkę do celu G")
        print(f"  Koszt ścieżki:     {result.cost} kroków")
        print(f"  Odwiedzone stany:  {len(result.visited)}")
    else:
        print(f"  Status:            Brak drogi do celu G")
        print(f"  Odwiedzone stany:  {len(result.visited)}")
