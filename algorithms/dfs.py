from typing import Dict, List, Optional, Set
import time
from models import Maze, Point, SearchResult, get_neighbors
from algorithms.base import reconstruct_path


def dfs(maze: Maze) -> SearchResult:
    """
    Algorytm przeszukiwania w głąb (Depth-First Search).
    Używa stosu LIFO (Last-In, First-Out) zrealizowanego na zwykłej liście Pythona.
    Drąży jedną wybraną ścieżkę do końca, zanim cofnie się do skrzyżowania.
    Nie gwarantuje znalezienia najkrótszej drogi.
    """
    start_time = time.perf_counter()
    # Zwykła lista idealnie sprawdza się jako stos LIFO, ponieważ dodawanie na koniec (append)
    # oraz zdejmowanie z końca (pop) działają w czasie stałym O(1) bez przesuwania pamięci.
    stack: List[Point] = [maze.start]

    # Zbiór odwiedzonych stanów chroniący przed wielokrotnym badaniem tych samych pól
    visited: Set[Point] = {maze.start}

    # Słownik poprzedników do późniejszego odtworzenia ścieżki
    parent_map: Dict[Point, Optional[Point]] = {maze.start: None}

    while stack:
        # Zdejmujemy najnowszy (ostatnio dodany) element z wierzchu stosu (zasada LIFO)
        current = stack.pop()

        # Jeśli trafiliśmy na punkt docelowy G, kończymy pętlę
        if current == maze.goal:
            break

        # Dodajemy nieodwiedzonych sąsiadów na wierzch stosu
        for neighbor in get_neighbors(current, maze):
            if neighbor not in visited:
                visited.add(neighbor)
                parent_map[neighbor] = current
                stack.append(neighbor)

    elapsed_ms = (time.perf_counter() - start_time) * 1000.0
    path = reconstruct_path(parent_map, maze.start, maze.goal)
    return SearchResult(algorithm_name="DFS", path=path, visited=visited, execution_time_ms=elapsed_ms)
