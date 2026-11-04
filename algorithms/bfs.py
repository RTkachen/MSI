from collections import deque
from typing import Dict, Optional, Set
from models import Maze, Point, SearchResult, get_neighbors
from algorithms.base import reconstruct_path


def bfs(maze: Maze) -> SearchResult:
    """
    Algorytm przeszukiwania wszerz (Breadth-First Search).
    Działa falami, używając kolejki FIFO (First-In, First-Out).
    Zawsze znajduje najkrótszą ścieżkę, gdy koszt każdego kroku jest taki sam.
    """
    # deque to kolejka dwukierunkowa, która pozwala usuwać elementy z początku (popleft) w czasie stałym O(1).
    # Zwykła lista przy pop(0) musiałaby przesuwać wszystkie pozostałe elementy w pamięci.
    queue: deque[Point] = deque([maze.start])

    # Zbiór (set) przechowuje już odwiedzone punkty. Sprawdzanie 'neighbor in visited'
    # w zbiorze jest błyskawiczne i zapobiega zapętleniu się algorytmu.
    visited: Set[Point] = {maze.start}

    # Słownik pamiętający poprzednika każdego pola: {pole_odwiedzone: pole_z_ktorego_przyszliśmy}
    parent_map: Dict[Point, Optional[Point]] = {maze.start: None}

    while queue:
        # Pobieramy i usuwamy najstarszy element z początku kolejki (zasada FIFO)
        current = queue.popleft()

        # Jeśli dotarliśmy do celu G, przerywamy dalsze przeszukiwanie
        if current == maze.goal:
            break

        # Sprawdzamy wszystkich dostępnych sąsiadów aktualnego pola
        for neighbor in get_neighbors(current, maze):
            if neighbor not in visited:
                visited.add(neighbor)           # Oznaczamy sąsiada jako odwiedzonego
                parent_map[neighbor] = current  # Zapamiętujemy, że na 'neighbor' weszliśmy z 'current'
                queue.append(neighbor)          # Dokładamy sąsiada na koniec kolejki do późniejszego sprawdzenia

    # Odtwarzamy ostateczną trasę od S do G na podstawie zapamiętanej mapy rodziców
    path = reconstruct_path(parent_map, maze.start, maze.goal)
    return SearchResult(algorithm_name="BFS", path=path, visited=visited)
