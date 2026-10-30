# odisee-route-planner

A small, original practice repository for **Odisee** AI-enabled algorithms
mocks. It plans delivery routes on a weighted, undirected road graph.
Pure Python, standard library only, pytest for tests.

Licence: MIT (see `LICENSE`).

## Setup

Requires Python 3.11+ and [uv](https://docs.astral.sh/uv/) (or plain `pip install pytest`).

```bash
uv run pytest -q
```

On `main`, **one test fails on purpose**: `tests/test_bug_report.py` reproduces bug #12.

## Layout

| Path | What it is |
|---|---|
| `src/route_planner/graph.py` | `RoadGraph` (adjacency lists, whole-minute weights) and `shortest_time(graph, source, target)` |
| `src/route_planner/route.py` | `plan_route(graph, stops)`: total minutes to visit stops in order |
| `tests/` | Visible tests; `test_bug_report.py` fails on `main` |

## Tasks

Each task is graded on its own, starting from `main`. Use any AI assistant
you like, but you own the result: read every edit, run the tests, and never
change a test's expected value to make it pass.

### Task 1 — fix bug #12 (`t1-detour-bug`)

Dispatch reports that the planner sometimes picks a slower direct road over a
faster detour. `tests/test_bug_report.py` reproduces it. Find the root cause in
`shortest_time` and fix it so that it returns the true minimum for **any**
graph with non-negative weights, not only the reported one. Keep the
time complexity at O((V + E) log V). Add at least one more test of your own
that would have caught the bug.

### Task 2 — nearest depots (`t2-nearest-depots`)

Add `k_nearest_depots(graph, origin, depots, k) -> list[tuple[str, int]]` in
a new module `src/route_planner/depots.py`, exported from the package.

* Return up to `k` depots from `depots` with their shortest travel minutes from `origin`,
  sorted by minutes, ties broken by depot name.
* Depots that are unreachable from `origin` are left out. `k <= 0` returns `[]`.
* `origin` itself counts (0 minutes) if it is in `depots`.
* It must run **one** shortest-path search from `origin` (not one per depot):
  O((V + E) log V) for the search plus O(D log k) to pick the results.
* Be ready to state and defend the time and space complexity.

Stage 3 (if time allows): on a grid of 200 x 200 stops with 500 depots, your
function should return in well under a second.

Task 2 builds on a correct `shortest_time`; if you do Task 2 alone, write your
own search in `depots.py`.

## For graders

* Golden solutions: branches `solution/t1-detour-bug` and `solution/t2-nearest-depots`.
* Hidden verifier tests: branch `verifier`, directory `verifier/`.
  * fail-to-pass: `verifier/test_t1_detour.py`, `verifier/test_t2_depots.py`.
  * pass-to-pass: `tests/test_graph.py` and `tests/test_route.py` **as they are on `main`**.

```bash
git checkout <candidate>
git checkout main -- tests/
git checkout verifier -- verifier/
uv run pytest -q verifier/test_t1_detour.py               # fail-to-pass
uv run pytest -q tests/test_graph.py tests/test_route.py  # pass-to-pass
```

Please solve the tasks before looking at those branches.
