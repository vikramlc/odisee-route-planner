from __future__ import annotations

from .graph import RoadGraph, shortest_time


class UnreachableStop(Exception):
    def __init__(self, src: str, dst: str) -> None:
        super().__init__(f"no road from {src} to {dst}")
        self.src = src
        self.dst = dst


def plan_route(graph: RoadGraph, stops: list[str]) -> int:
    """Total minutes to visit `stops` in the given order (each leg is a shortest path)."""
    total = 0
    for src, dst in zip(stops, stops[1:]):
        leg = shortest_time(graph, src, dst)
        if leg is None:
            raise UnreachableStop(src, dst)
        total += leg
    return total
