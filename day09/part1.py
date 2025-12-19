from __future__ import annotations

import argparse
import itertools
import os.path
from typing import NamedTuple

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


class Point(NamedTuple):
    x: int
    y: int


def rect(a: Point, b: Point) -> int:
    return (1 + abs(a.x - b.x)) * (1 + abs(a.y - b.y))


def compute(s: str) -> int:
    lines = s.splitlines()
    points = set()
    for line in lines:
        points.add(Point(*map(int, line.split(','))))

    return max(
        rect(a, b)
        for a, b in itertools.combinations(points, r=2)
    )


INPUT_S = '''\
7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3
'''
EXPECTED = 50


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
