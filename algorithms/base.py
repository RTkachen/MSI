from typing import Dict, List, Optional
from models import Point


# Optional[Point] oznacza, że wartością w słowniku może być obiekt Point albo wartość None
# (wartość None ma tylko punkt startowy S, ponieważ nie przyszliśmy do niego z żadnego wcześniejszego pola).
def reconstruct_path(
    parent_map: Dict[Point, Optional[Point]],
    start: Point,
    goal: Point,
) -> List[Point]:
    """
    Odtwarza ścieżkę od punktu S do punktu G metodą cofania się po śladach (backtracking).
    Korzysta ze słownika 'parent_map', w którym kluczem jest pole, a wartością jego poprzednik.
    """
    # Jeśli punkt docelowy G nigdy nie został zapisany w słowniku, ścieżka nie istnieje
    if goal not in parent_map:
        return []

    path: List[Point] = []
    # Zaczynamy cofanie od punktu docelowego G
    current: Optional[Point] = goal

    # Dopóki nie wyjdziemy poza punkt startowy (którego rodzicem w słowniku jest None):
    while current is not None:
        path.append(current)            # Dodajemy aktualne pole do ścieżki
        current = parent_map[current]   # Przestawiamy zmienną 'current' na pole, z którego tu przyszliśmy

    # Ponieważ punkty zbieraliśmy od mety (G) do startu (S), odwracamy listę w miejscu,
    # aby uzyskać właściwą kolejność kroków od S do G.
    path.reverse()

    # Dodatkowe upewnienie się, że ścieżka faktycznie zaczyna się w punkcie startowym
    if path and path[0] == start:
        return path
    return []
