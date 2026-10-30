"""Hidden verifier for Task 1 (fail-to-pass). Do not read before solving."""

import random

from route_planner import RoadGraph, plan_route, shortest_time


def test_reported_detour():
    g = RoadGraph()
    g.add_road("depot", "market", 10)
    g.add_road("depot", "bridge", 2)
    g.add_road("bridge", "market", 3)
    assert shortest_time(g, "depot", "market") == 5


def test_detour_to_an_intermediate_stop():
    g = RoadGraph()
    g.add_road("depot", "a", 10)
    g.add_road("depot", "b", 1)
    g.add_road("b", "a", 1)
    g.add_road("a", "market", 1)
    assert shortest_time(g, "depot", "market") == 3


def _floyd(nodes, edges):
    inf = float("inf")
    d = {u: {v: (0 if u == v else inf) for v in nodes} for u in nodes}
    for a, b, w in edges:
        d[a][b] = min(d[a][b], w)
        d[b][a] = min(d[b][a], w)
    for k in nodes:
        for i in nodes:
            for j in nodes:
                if d[i][k] + d[k][j] < d[i][j]:
                    d[i][j] = d[i][k] + d[k][j]
    return d


def test_random_graphs_match_floyd_warshall():
    rng = random.Random(12)
    mismatches = 0
    for _ in range(60):
        nodes = [f"n{i}" for i in range(9)]
        edges = [(rng.choice(nodes), rng.choice(nodes), rng.randint(0, 20)) for _ in range(16)]
        g = RoadGraph()
        for a, b, w in edges:
            g.add_road(a, b, w)
        d = _floyd(nodes, edges)
        for u in nodes:
            for v in nodes:
                want = d[u][v]
                got = shortest_time(g, u, v)
                mismatches += got != (None if want == float("inf") else want)
    assert mismatches == 0


def test_plan_route_uses_true_shortest_legs():
    g = RoadGraph()
    g.add_road("depot", "clinic", 30)
    g.add_road("depot", "park", 4)
    g.add_road("park", "mill", 4)
    g.add_road("mill", "clinic", 4)
    assert plan_route(g, ["depot", "clinic", "depot"]) == 24
