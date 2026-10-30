import pytest

from route_planner import RoadGraph, shortest_time


def line_graph():
    g = RoadGraph()
    g.add_road("depot", "a", 4)
    g.add_road("a", "b", 6)
    g.add_road("b", "c", 1)
    return g


def test_same_node_is_zero():
    assert shortest_time(line_graph(), "a", "a") == 0


def test_line_distance():
    assert shortest_time(line_graph(), "depot", "c") == 11


def test_roads_are_undirected():
    assert shortest_time(line_graph(), "c", "depot") == 11


def test_unreachable_is_none():
    g = line_graph()
    g.add_road("x", "y", 2)
    assert shortest_time(g, "depot", "y") is None


def test_unknown_node_is_none():
    assert shortest_time(line_graph(), "depot", "nowhere") is None


def test_negative_minutes_rejected():
    with pytest.raises(ValueError):
        RoadGraph().add_road("a", "b", -1)


def test_zero_minute_road():
    g = RoadGraph()
    g.add_road("a", "b", 0)
    assert shortest_time(g, "a", "b") == 0


def test_detour_through_intermediate_stop():
    g = RoadGraph()
    g.add_road("depot", "a", 10)
    g.add_road("depot", "b", 1)
    g.add_road("b", "a", 1)
    g.add_road("a", "market", 1)
    assert shortest_time(g, "depot", "market") == 3
