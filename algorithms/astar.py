import heapq
import time
from itertools import count
from typing import Dict, List, Optional, Set, Tuple
from models import Maze, Point, SearchResult, get_neighbors
from algorithms.base import reconstruct_path
from algorithms.heuristics import HeuristicFunc, manhattan_distance


def astar(
    maze: Maze,
    heuristic: HeuristicFunc = manhattan_distance,
    heuristic_name: str = "Manhattan",
    alpha: float = 1.0,
    beta: float = 1.0,
) -> SearchResult:
    """
    Uogólniony algorytm A* wykorzystujący funkcję oceny:
        f(n) = alpha * g(n) + beta * h(n)
    gdzie:
    - g(n) to rzeczywisty koszt dojścia od startu S do węzła n,
    - h(n) to heurystyczne oszacowanie kosztu od węzła n do celu G,
    - alpha to waga kosztu dotychczasowej ścieżki,
    - beta to waga heurystyki.
    """
    # Rozpoczęcie pomiaru czasu wykonania algorytmu (w wysokiej rozdzielczości)
    start_time = time.perf_counter()

    # Licznik (0, 1, 2, ...) służący do rozstrzygania remisów w kolejce priorytetowej,
    # gdy dwa różne pola mają identyczną wartość funkcji oceny f(n).
    tie_breaker = count()

    # Słownik g_score przechowuje najniższy znany koszt dojścia g(n) od punktu S do danego pola.
    # Dla pola startowego koszt wynosi 0.0.
    g_score: Dict[Point, float] = {maze.start: 0.0}

    # Obliczenie początkowej wartości f(S) = alpha * 0 + beta * h(S)
    f_start = alpha * 0.0 + beta * heuristic(maze.start, maze.goal)

    # Zbiór otwarty (kolejka priorytetowa) zrealizowany za pomocą listy i modułu heapq.
    # Każdy element to krotka: (wartość_f, licznik_remisów, obiekt_Point).
    # heapq zawsze ustawia na pierwszym miejscu krotkę z najmniejszą wartością_f.
    open_heap: List[Tuple[float, int, Point]] = [(f_start, next(tie_breaker), maze.start)]

    # Zbiór zamknięty (visited) przechowuje stany, które zostały już wyjęte z kolejki i w pełni przeanalizowane
    visited: Set[Point] = set()

    # Słownik poprzedników do odtworzenia ścieżki na końcu
    parent_map: Dict[Point, Optional[Point]] = {maze.start: None}

    while open_heap:
        # 1. Wyciągamy ze zbioru otwartego węzeł o NAJMNIEJSZEJ wartości f(n)
        _, _, current = heapq.heappop(open_heap)

        # Jeśli ten punkt był już wcześniej rozwinięty (mógł trafić do kopca podwójnie z wyższym kosztem), pomijamy go
        if current in visited:
            continue

        # Oznaczamy bieżący węzeł jako odwiedzony (przeniesienie do zbioru zamkniętego)
        visited.add(current)

        # 2. Jeśli dotarliśmy do punktu docelowego G, kończymy przeszukiwanie
        if current == maze.goal:
            break

        # 3. Rozwijamy wszystkich legalnych sąsiadów bieżącego pola
        for neighbor in get_neighbors(current, maze):
            if neighbor in visited:
                continue

            # Koszt każdego kroku wynosi 1, więc nowy koszt g(neighbor) to g(current) + 1
            tentative_g = g_score[current] + 1.0

            # Jeśli odkryliśmy sąsiada po raz pierwszy LUB znaleźliśmy do niego tańszą drogę niż wcześniej:
            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                g_score[neighbor] = tentative_g
                parent_map[neighbor] = current

                # Wyliczamy ocenę f(n) = alpha * g(n) + beta * h(n)
                h_val = heuristic(neighbor, maze.goal)
                f_val = alpha * tentative_g + beta * h_val

                # Wrzucamy sąsiada do kolejki priorytetowej
                heapq.heappush(open_heap, (f_val, next(tie_breaker), neighbor))

    # Zatrzymanie stopera i przeliczenie czasu z sekund na milisekundy [ms]
    elapsed_ms = (time.perf_counter() - start_time) * 1000.0

    # Odtworzenie ścieżki od S do G
    path = reconstruct_path(parent_map, maze.start, maze.goal)
    algo_label = f"A* ({heuristic_name}, α={alpha}, β={beta})"

    return SearchResult(
        algorithm_name=algo_label,
        path=path,
        visited=visited,
        execution_time_ms=elapsed_ms,
    )
