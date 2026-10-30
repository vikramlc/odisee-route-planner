from __future__ import annotations

import heapq

from .graph import RoadGraph


def _times_from(graph: RoadGraph, origin: str) -> dict[str, int]:
    """Single-source shortest times (Dijkstra with lazy deletion)."""
    best: dict[str, int] = {origin: 0}
    heap: list[tuple[int, str]] = [(0, origin)]
    while heap:
        time, node = heapq.heappop(heap)
        if time > best[node]:
            continue
        for nxt, minutes in graph.neighbors(node):
            candidate = time + minutes
            if candidate < best.get(nxt, candidate + 1):
                best[nxt] = candidate
                heapq.heappush(heap, (candidate, nxt))
    return best


def k_nearest_depots(graph: RoadGraph, origin: str, depots: list[str], k: int) -> list[tuple[str, int]]:
    """Up to k reachable depots with their minutes from origin, nearest first, ties by name.

    One Dijkstra run from origin: O((V + E) log V) time, O(V) space; then
    O(D log k) to keep the k best of D depots.
    """
    if k <= 0:
        return []
    times = _times_from(graph, origin)
    reachable = ((times[d], d) for d in set(depots) if d in times)
    return [(name, minutes) for minutes, name in heapq.nsmallest(k, reachable)]
