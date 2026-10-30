"""Hidden verifier for Task 2 (fail-to-pass). Do not read before solving."""

import time

from route_planner import RoadGraph


def k_nearest_depots(*args):
    from route_planner import k_nearest_depots as impl

    return impl(*args)


def town():
    g = RoadGraph()
    g.add_road("home", "a", 4)
    g.add_road("home", "b", 1)
    g.add_road("b", "a", 1)
    g.add_road("a", "c", 5)
    g.add_road("b", "d", 7)
    g.add_road("x", "y", 1)  # disconnected
    return g


def test_sorted_by_minutes_and_limited_to_k():
    assert k_nearest_depots(town(), "home", ["c", "a", "d"], 2) == [("a", 2), ("c", 7)]


def test_ties_broken_by_name():
    g = RoadGraph()
    g.add_road("o", "zeta", 3)
    g.add_road("o", "alpha", 3)
    assert k_nearest_depots(g, "o", ["zeta", "alpha"], 2) == [("alpha", 3), ("zeta", 3)]


def test_unreachable_left_out():
    assert k_nearest_depots(town(), "home", ["y", "a"], 3) == [("a", 2)]


def test_k_zero_or_negative():
    assert k_nearest_depots(town(), "home", ["a"], 0) == []
    assert k_nearest_depots(town(), "home", ["a"], -2) == []


def test_origin_counts_as_zero():
    assert k_nearest_depots(town(), "home", ["home", "a"], 1) == [("home", 0)]


def test_k_larger_than_depots():
    assert k_nearest_depots(town(), "home", ["d", "a"], 10) == [("a", 2), ("d", 8)]


def test_grid_is_fast():
    g = RoadGraph()
    n = 120
    for r in range(n):
        for c in range(n):
            if r + 1 < n:
                g.add_road(f"{r},{c}", f"{r + 1},{c}", 1 + (r * c) % 3)
            if c + 1 < n:
                g.add_road(f"{r},{c}", f"{r},{c + 1}", 1 + (r + c) % 3)
    depots = [f"{(i * 37) % n},{(i * 91) % n}" for i in range(300)]
    start = time.perf_counter()
    out = k_nearest_depots(g, "0,0", depots, 5)
    assert time.perf_counter() - start < 3.0
    assert len(out) == 5
    assert out == sorted(out, key=lambda p: (p[1], p[0]))
