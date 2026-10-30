from __future__ import annotations

import heapq
from collections import defaultdict
from collections.abc import Iterator


class RoadGraph:
    """Undirected road network. Nodes are stop names, weights are whole minutes."""

    def __init__(self) -> None:
        self._adj: dict[str, list[tuple[str, int]]] = defaultdict(list)

    def add_road(self, a: str, b: str, minutes: int) -> None:
        if minutes < 0:
            raise ValueError("minutes must be >= 0")
        self._adj[a].append((b, minutes))
        self._adj[b].append((a, minutes))

    def neighbors(self, node: str) -> list[tuple[str, int]]:
        return self._adj.get(node, [])

    def nodes(self) -> Iterator[str]:
        return iter(self._adj)

    def __contains__(self, node: object) -> bool:
        return node in self._adj


def shortest_time(graph: RoadGraph, source: str, target: str) -> int | None:
    """Minimum travel minutes from source to target, or None when unreachable."""
    if source == target:
        return 0
    best: dict[str, int] = {source: 0}
    heap: list[tuple[int, str]] = [(0, source)]
    while heap:
        time, node = heapq.heappop(heap)
        if time > best[node]:
            continue  # stale entry: a faster path to node was already settled
        if node == target:
            return time
        for nxt, minutes in graph.neighbors(node):
            candidate = time + minutes
            if candidate < best.get(nxt, candidate + 1):
                best[nxt] = candidate
                heapq.heappush(heap, (candidate, nxt))
    return None
