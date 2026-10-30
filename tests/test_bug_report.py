"""Bug report #12 from dispatch: the planner picks the direct road even when a
detour through another stop is faster. This test reproduces it and fails on main."""

from route_planner import RoadGraph, shortest_time


def test_prefers_faster_detour():
    g = RoadGraph()
    g.add_road("depot", "market", 10)  # direct road, slow
    g.add_road("depot", "bridge", 2)
    g.add_road("bridge", "market", 3)  # detour: 2 + 3 = 5
    assert shortest_time(g, "depot", "market") == 5
