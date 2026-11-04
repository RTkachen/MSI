from typing import Callable, Dict
from models import Maze, SearchResult
from algorithms.base import reconstruct_path
from algorithms.bfs import bfs
from algorithms.dfs import dfs

# Słownik pełniący rolę rejestru algorytmów.
# Kluczem jest nazwa algorytmu, a wartością funkcja przyjmująca obiekt Maze i zwracająca SearchResult.
# Aby dodać w przyszłości nowy algorytm, wystarczy zaimportować go i dopisać tutaj jedną linijkę.
ALGORITHMS: Dict[str, Callable[[Maze], SearchResult]] = {
    "BFS": bfs,
    "DFS": dfs,
}

__all__ = ["bfs", "dfs", "reconstruct_path", "ALGORITHMS"]
