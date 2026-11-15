import math
from typing import Callable, Dict
from models import Point

# Typ pomocniczy opisujący funkcję heurystyczną: przyjmuje dwa punkty (aktualny, cel) i zwraca liczbę float
HeuristicFunc = Callable[[Point, Point], float]


def manhattan_distance(current: Point, goal: Point) -> float:
    """
    Odległość Manhattan (miejska): h_M(n) = |x_n - x_G| + |y_n - y_G|.
    Naturalna heurystyka dla siatki, na której dozwolone są tylko 4 kierunki ruchu.
    """
    return float(abs(current.row - goal.row) + abs(current.col - goal.col))


def euclidean_distance(current: Point, goal: Point) -> float:
    """
    Odległość Euklidesowa (w linii prostej): h_E(n) = sqrt((x_n - x_G)^2 + (y_n - y_G)^2).
    Geometryczna odległość między aktualnym położeniem agenta a celem G.
    """
    # math.hypot(dx, dy) to zoptymalizowany zapis sqrt(dx*dx + dy*dy)
    return math.hypot(current.row - goal.row, current.col - goal.col)


# Słownik ułatwiający wybieranie heurystyki po nazwie
HEURISTICS: Dict[str, HeuristicFunc] = {
    "Manhattan": manhattan_distance,
    "Euklidesowa": euclidean_distance,
}
