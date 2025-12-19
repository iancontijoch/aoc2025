from __future__ import annotations

import argparse
import itertools
import math
import os.path
from typing import NamedTuple

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


class Point(NamedTuple):
    x: int
    y: int
    z: int

    def __repr__(self) -> str:
        return str((self.x, self.y, self.z))


def compute(s: str) -> int:
    lines = s.splitlines()
    points = set()
    graphs: list[set[Point]] = []

    def dist(a: Point, b: Point) -> float:
        return math.sqrt(
            (a.x - b.x) ** 2 +
            (a.y - b.y) ** 2 +
            (a.z - b.z) ** 2,
        )

    for line in lines:
        x, y, z = map(int, line.split(','))
        pt = Point(x, y, z)
        points.add(pt)
        graphs.append({pt})

    dists = sorted(
        [
            (a, b) for a, b in itertools.combinations(points, r=2)
        ], key=lambda x: dist(x[0], x[1]),
    )

    def find_graph(pt: Point, graphs: list[set[Point]]) -> int:
        for i, graph in enumerate(graphs):
            if pt in graph:
                return i
        return -1

    def connected(graphs: list[set[Point]]) -> bool:
        return len([g for g in graphs if len(g) != 0]) == 1

    for (a, b) in dists:
        a_idx, b_idx = find_graph(a, graphs), find_graph(b, graphs)
        if a_idx != -1 and b_idx == -1:
            graphs[a_idx].add(b)
        elif a_idx == -1 and b_idx != -1:
            graphs[b_idx].add(a)
        elif a_idx != -1 and b_idx != -1:
            if a_idx != b_idx:
                graphs[a_idx].update(graphs[b_idx])
                graphs[b_idx].clear()
        else:
            raise NotImplementedError

        if connected(graphs):
            return a.x * b.x

    return 0


INPUT_S = '''\
162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689
'''
EXPECTED = 25272


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, EXPECTED),
    ),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
