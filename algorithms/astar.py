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
    # Rozpoczęcie pomiaru czasu wykonania algorytmu
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



    #Wynik dla labiryntu 1:
# ===========================================================================
# Konfiguracja algorytmu              |   Koszt |  Liczba stanów |  Czas [ms]
# ---------------------------------------------------------------------------
# BFS                                 |      54 |            576 |      2.025
# DFS                                 |     174 |            475 |      1.157
# A* (Manhattan, α=1, β=0)            |      54 |            576 |      2.679
# A* (Manhattan, α=1, β=0.1)          |      54 |            575 |      2.648
# A* (Manhattan, α=1, β=0.5)          |      54 |            573 |      2.590
# A* (Manhattan, α=1, β=1)            |      54 |            209 |      0.963
# A* (Manhattan, α=1, β=2)            |      60 |            101 |      0.511
# A* (Manhattan, α=1, β=5)            |      68 |             92 |      0.445
# A* (Manhattan, α=0, β=1)            |      68 |             88 |      0.510
# A* (Euklidesowa, α=1, β=0)          |      54 |            576 |      2.698
# A* (Euklidesowa, α=1, β=0.1)        |      54 |            575 |      2.590
# A* (Euklidesowa, α=1, β=0.5)        |      54 |            573 |      2.545
# A* (Euklidesowa, α=1, β=1)          |      54 |            424 |      1.974
# A* (Euklidesowa, α=1, β=2)          |      58 |             96 |      0.491
# A* (Euklidesowa, α=1, β=5)          |      60 |             79 |      0.388
# A* (Euklidesowa, α=0, β=1)          |      60 |             81 |      0.405
# ===========================================================================


    #Wynika dla labiryntu 2:
#===========================================================================
# Konfiguracja algorytmu              |   Koszt |  Liczba stanów |  Czas [ms]
# ---------------------------------------------------------------------------
# BFS                                 |     106 |           1148 |      3.921
# DFS                                 |     332 |            809 |      2.847
# A* (Manhattan, α=1, β=0)            |     106 |           1147 |      5.484
# A* (Manhattan, α=1, β=0.1)          |     106 |           1143 |      5.246
# A* (Manhattan, α=1, β=0.5)          |     106 |           1117 |      7.211
# A* (Manhattan, α=1, β=1)            |     106 |           1060 |      5.204
# A* (Manhattan, α=1, β=2)            |     118 |            847 |      4.207
# A* (Manhattan, α=1, β=5)            |     144 |            781 |      4.727
# A* (Manhattan, α=0, β=1)            |     170 |            716 |      3.092
# A* (Euklidesowa, α=1, β=0)          |     106 |           1147 |      4.446
# A* (Euklidesowa, α=1, β=0.1)        |     106 |           1144 |      5.246
# A* (Euklidesowa, α=1, β=0.5)        |     106 |           1119 |      4.087
# A* (Euklidesowa, α=1, β=1)          |     106 |           1084 |      2.935
# A* (Euklidesowa, α=1, β=2)          |     108 |            710 |      2.249
# A* (Euklidesowa, α=1, β=5)          |     130 |            657 |      1.962
# A* (Euklidesowa, α=0, β=1)          |     134 |            582 |      1.634
# ===========================================================================

    #Wynik dla labiryntu 3:
# ===========================================================================
# Konfiguracja algorytmu              |   Koszt |  Liczba stanów |  Czas [ms]
# ---------------------------------------------------------------------------
# BFS                                 |     174 |           5374 |     19.097
# DFS                                 |     714 |           1785 |      2.812
# A* (Manhattan, α=1, β=0)            |     174 |           5374 |     17.386
# A* (Manhattan, α=1, β=0.1)          |     174 |           5374 |     15.003
# A* (Manhattan, α=1, β=0.5)          |     174 |           5278 |     15.685
# A* (Manhattan, α=1, β=1)            |     174 |           2006 |      5.767
# A* (Manhattan, α=1, β=2)            |     194 |            432 |      1.302
# A* (Manhattan, α=1, β=5)            |     238 |            374 |      1.119
# A* (Manhattan, α=0, β=1)            |     250 |            345 |      1.040
# A* (Euklidesowa, α=1, β=0)          |     174 |           5374 |     15.311
# A* (Euklidesowa, α=1, β=0.1)        |     174 |           5374 |     15.599
# A* (Euklidesowa, α=1, β=0.5)        |     174 |           5316 |     15.149
# A* (Euklidesowa, α=1, β=1)          |     174 |           4204 |     12.013
# A* (Euklidesowa, α=1, β=2)          |     176 |            294 |      0.911
# A* (Euklidesowa, α=1, β=5)          |     206 |            348 |      1.067
# A* (Euklidesowa, α=0, β=1)          |     226 |            343 |      1.046
# ===========================================================================

    #Wynik dla labiryntu 4:
#===========================================================================
# Konfiguracja algorytmu              |   Koszt |  Liczba stanów |  Czas [ms]
# ---------------------------------------------------------------------------
# BFS                                 |     208 |           4625 |     15.475
# DFS                                 |     472 |           1800 |      4.302
# A* (Manhattan, α=1, β=0)            |     208 |           4591 |     16.586
# A* (Manhattan, α=1, β=0.1)          |     208 |           4414 |     12.073
# A* (Manhattan, α=1, β=0.5)          |     208 |           3360 |      9.265
# A* (Manhattan, α=1, β=1)            |     208 |           1830 |      5.061
# A* (Manhattan, α=1, β=2)            |     214 |           1116 |      3.185
# A* (Manhattan, α=1, β=5)            |     234 |            568 |      2.677
# A* (Manhattan, α=0, β=1)            |     254 |            613 |      1.786
# A* (Euklidesowa, α=1, β=0)          |     208 |           4591 |     12.666
# A* (Euklidesowa, α=1, β=0.1)        |     208 |           4438 |     11.889
# A* (Euklidesowa, α=1, β=0.5)        |     208 |           3709 |     10.544
# A* (Euklidesowa, α=1, β=1)          |     208 |           2473 |      6.686
# A* (Euklidesowa, α=1, β=2)          |     210 |            758 |      2.193
# A* (Euklidesowa, α=1, β=5)          |     230 |           1060 |      3.620
# A* (Euklidesowa, α=0, β=1)          |     250 |            459 |      1.346
# ===========================================================================
