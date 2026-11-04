from pathlib import Path
from models import Maze, Point

# Zbiór (set) dozwolonych znaków w pliku wejściowym
VALID_CELLS = {"0", "1", "S", "G"}


class MazeFormatError(Exception):
    """Własny wyjątek zgłaszany, gdy plik labiryntu narusza wymagania formatu."""
    pass


# Adnotacja 'filepath: str | Path' oznacza, że funkcja przyjmuje ścieżkę jako zwykły napis (str)
# lub obiekt Path.
def load_maze(filepath: str | Path) -> Maze:
    """
    Wczytuje planszę z pliku tekstowego i weryfikuje jej poprawność:
    - sprawdza istnienie pliku i czy nie jest pusty,
    - pilnuje prostokątnego kształtu planszy,
    - weryfikuje, czy użyto wyłącznie symboli 0, 1, S, G,
    - upewnia się, że istnieje dokładnie jeden start (S) i jeden cel (G).
    """
    path = Path(filepath)
    if not path.is_file():
        raise FileNotFoundError(f"Nie znaleziono pliku: {filepath}")

    with path.open("r", encoding="utf-8") as f:
        # line.strip() usuwa białe znaki z początku i końca linii (np. znak nowej linii \n).
        # Warunek 'if line.strip()' pomija całkowicie puste wiersze w pliku.
        lines = [line.strip() for line in f if line.strip()]

    if not lines:
        raise MazeFormatError("Plik labiryntu jest pusty.")

    # line.split() dzieli każdy wiersz tekstu w miejscach spacji na pojedyncze symbole.
    # Powstaje macierz 2D, gdzie każdy element to pojedynczy znak string.
    grid: list[list[str]] = [line.split() for line in lines]

    # Liczba elementów głównej listy to liczba wierszy w pliku
    rows = len(grid)
    # Liczba elementów w pierwszym wierszu (grid[0]) staje się wzorcową liczbą kolumn
    cols = len(grid[0])

    # Listy pomocnicze do zebrania wszystkich wystąpień punktów S oraz G
    starts: list[Point] = []
    goals: list[Point] = []

    # enumerate(grid) zwraca w każdym obiegu pętli parę: (indeks_wiersza, lista_znakow_w_wierszu)
    for r, row in enumerate(grid):
        # Walidacja prostokątności: każdy wiersz musi mieć tyle samo kolumn co pierwszy wiersz
        if len(row) != cols:
            raise MazeFormatError(
                f"Nierówny wiersz {r}: oczekiwano {cols} elementów, otrzymano {len(row)}. "
                "Plansza musi być prostokątna."
            )

        # Druga pętla z enumerate() przechodzi przez pojedyncze znaki w bieżącym wierszu:
        # 'c' to indeks kolumny, a 'val' to symbol na pozycji (r, c)
        for c, val in enumerate(row):
            if val not in VALID_CELLS:
                raise MazeFormatError(
                    f"Nieznany symbol '{val}' na pozycji ({r}, {c}). "
                    f"Dozwolone są wyłącznie: {sorted(VALID_CELLS)}."
                )

            # Zapisanie współrzędnych znalezionego punktu startowego lub docelowego
            if val == "S":
                starts.append(Point(r, c))
            elif val == "G":
                goals.append(Point(r, c))

    # Walidacja unikalności punktów S i G (musi być dokładnie po jednym)
    if len(starts) != 1:
        raise MazeFormatError(
            f"Plansza musi zawierać dokładnie jeden punkt startowy 'S' (znaleziono: {len(starts)})."
        )

    if len(goals) != 1:
        raise MazeFormatError(
            f"Plansza musi zawierać dokładnie jeden punkt docelowy 'G' (znaleziono: {len(goals)})."
        )

    return Maze(
        grid=grid,
        rows=rows,
        cols=cols,
        start=starts[0],
        goal=goals[0],
    )
