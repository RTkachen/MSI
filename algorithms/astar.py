from typing import Dict, Optional, Set
from models import Maze, Point, SearchResult, get_neighbors
from algorithms.base import reconstruct_path
import heapq


def astar(maze: Maze, alfa: float, beta: float) -> SearchResult:

    prio_queue: heapq.heapify(Point) = maze.start

    visited: Set[Point] = {maze.start}

    parent_map: Dict[Point, Optional[Point]] = {maze.start: None}

