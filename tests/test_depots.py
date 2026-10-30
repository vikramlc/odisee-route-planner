from route_planner import RoadGraph, k_nearest_depots


def test_nearest_depots_sorted_and_limited():
    g = RoadGraph()
    g.add_road("home", "b", 1)
    g.add_road("b", "a", 1)
    g.add_road("home", "a", 4)
    g.add_road("a", "c", 5)
    g.add_road("x", "y", 1)
    assert k_nearest_depots(g, "home", ["c", "a", "y"], 5) == [("a", 2), ("c", 7)]
    assert k_nearest_depots(g, "home", ["c", "a"], 0) == []
