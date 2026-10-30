import pytest

from route_planner import RoadGraph, UnreachableStop, plan_route


def city():
    g = RoadGraph()
    g.add_road("depot", "bakery", 5)
    g.add_road("bakery", "school", 7)
    g.add_road("depot", "school", 15)
    g.add_road("school", "clinic", 3)
    return g


def test_single_stop_is_zero():
    assert plan_route(city(), ["depot"]) == 0


def test_route_sums_legs():
    assert plan_route(city(), ["depot", "bakery", "clinic"]) == 5 + 10


def test_unreachable_stop_raises():
    g = city()
    g.add_road("island", "pier", 1)
    with pytest.raises(UnreachableStop):
        plan_route(g, ["depot", "pier"])
