from dataclasses import dataclass
from typing import NamedTuple, List, Set


class Point(NamedTuple):
    """
    Reprezentuje położenie (stan) agenta na planszy jako parę współrzędnych (wiersz, kolumna).
    Dziedziczenie po NamedTuple sprawia, że obiekt:
    1. Jest niemutowalny (nieedytowalny po utworzeniu - nie można przypadkowo nadpisać współrzędnych).
    2. Pozwala odwoływać się do pól po nazwie (np. p.row, p.col) zamiast po indeksach (p[0], p[1]).
    3. Może być używany jako klucz w słowniku (parent_map) oraz element w zbiorze (visited).
    """
    row: int  # Numer wiersza (indeksowany od 0, góra -> dół)
    col: int  # Numer kolumny (indeksowany od 0, lewo -> prawo)


# Dekorator @dataclass automatycznie generuje konstruktor __init__(),
# metodę wyświetlania __repr__() oraz porównywanie obiektów __eq__() na podstawie poniższych pól.
@dataclass
class Maze:
    """Przechowuje pełną strukturę wczytanej planszy labiryntu oraz jej kluczowe punkty."""
    grid: List[List[str]]  # Dwuwymiarowa lista znaków reprezentująca siatkę mapy
    rows: int              # Całkowita liczba wierszy planszy (wysokość)
    cols: int              # Całkowita liczba kolumn planszy (szerokość)
    start: Point           # Współrzędne punktu startowego 'S'
    goal: Point            # Współrzędne punktu docelowego 'G'

    # Dekorator @property pozwala wywoływać metodę jak zwykłe pole obiektu (maze.size zamiast maze.size()).
    @property
    def size(self) -> tuple[int, int]:
        """Zwraca krotkę (liczba_wierszy, liczba_kolumn)."""
        return self.rows, self.cols


@dataclass
class SearchResult:
    """Przechowuje ustandaryzowany wynik działania dowolnego algorytmu przeszukiwania."""
    algorithm_name: str  # Nazwa algorytmu (np. 'BFS' lub 'DFS') używana przy wypisywaniu statystyk
    path: List[Point]    # Uporządkowana lista punktów tworzących ścieżkę od S do G (pusta, gdy brak drogi)
    visited: Set[Point]  # Zbiór (set) wszystkich unikalnych pól odwiedzonych podczas działania algorytmu
    execution_time_ms: float = 0.0  # Czas wykonania algorytmu w milisekundach [ms]

    @property
    def found(self) -> bool:
        """
        Sprawdza, czy droga do celu została znaleziona.
        Jeśli lista 'path' ma więcej niż 0 elementów, zwraca True; w przeciwnym razie False.
        """
        return len(self.path) > 0

    @property
    def cost(self) -> int:
        """
        Oblicza całkowity koszt znalezionej ścieżki.
        Każdy ruch ma koszt 1. Ponieważ lista 'path' zawiera również pole startowe S,
        liczba wykonanych kroków to liczba punktów na ścieżce pomniejszona o 1.
        Funkcja max(0, ...) zabezpiecza przed wynikiem -1, gdy ścieżka jest pusta (len == 0).
        """
        return max(0, len(self.path) - 1)


def get_neighbors(position: Point, maze: Maze) -> List[Point]:
    """
    Wyznacza listę wszystkich legalnych sąsiadów dla aktualnego położenia agenta.
    Uwzględnia 4 kierunki ruchu (góra, dół, lewo, prawo) bez ruchów po przekątnej.
    """
    # Rozpakowanie współrzędnych aktualnego punktu do zmiennych r (wiersz) i c (kolumna)
    r, c = position

    # Lista potencjalnych ruchów w czterech dozwolonych kierunkach
    candidates = [
        Point(r - 1, c),  # ruch w górę (wiersz o 1 mniejszy)
        Point(r + 1, c),  # ruch w dół (wiersz o 1 większy)
        Point(r, c - 1),  # ruch w lewo (kolumna o 1 mniejsza)
        Point(r, c + 1),  # ruch w prawo (kolumna o 1 większa)
    ]

    neighbors: List[Point] = []
    for nr, nc in candidates:
        # Warunek 1: Sprawdzenie, czy nowe współrzędne (nr, nc) mieszczą się w granicach planszy
        if 0 <= nr < maze.rows and 0 <= nc < maze.cols:
            # Warunek 2: Sprawdzenie w siatce 2D, czy dane pole nie jest ścianą ('1')
            if maze.grid[nr][nc] != "1":
                neighbors.append(Point(nr, nc))

    return neighbors
