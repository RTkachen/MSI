from typing import List
from models import Maze, SearchResult
from algorithms.base import reconstruct_path
from algorithms.bfs import bfs
from algorithms.dfs import dfs
from algorithms.astar import astar
from algorithms.heuristics import HEURISTICS


def run_all_configurations(maze: Maze) -> List[SearchResult]:
    """
    Uruchamia zestawienie wszystkich algorytmów i kombinacji parametrów (alfa, beta)
    wymaganych w tabeli z Instrukcji projektowej nr 2.
    """
    results: List[SearchResult] = [
        bfs(maze),
        dfs(maze),
    ]

    # Lista par (alfa, beta) wymaganych w specyfikacji zadania
    param_pairs = [
        (1, 0),
        (1, 0.1),
        (1, 0.5),
        (1, 1),
        (1, 2),
        (1, 5),
        (0, 1),
    ]

    # Uruchomienie każdej pary parametrów dla obu heurystyk (Manhattan oraz Euklidesowa)
    for h_name, h_func in HEURISTICS.items():
        for alpha, beta in param_pairs:
            res = astar(
                maze=maze,
                heuristic=h_func,
                heuristic_name=h_name,
                alpha=alpha,
                beta=beta,
            )
            results.append(res)

    return results
