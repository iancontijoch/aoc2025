from __future__ import annotations

import argparse
import os.path
from collections import deque

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    lines = s.splitlines()
    coords = {
        (x, y): c
        for y, line in enumerate(lines)
        for x, c in enumerate(line)
    }

    seen = set()
    splitters = set()
    start = next(pos for pos, c in coords.items() if c == 'S')

    q = deque([start])
    while q:
        pos = q.popleft()
        if pos in seen:
            continue
        seen.add(pos)
        cand = support.Direction4.apply(support.Direction4.DOWN, *pos)
        if cand in coords:
            if coords[cand] == '^':
                splitters.add(cand)
                for dir in (support.Direction4.LEFT, support.Direction4.RIGHT):
                    split = support.Direction4.apply(dir, *cand)
                    if split in coords and split not in seen:
                        q.append(split)
            else:
                q.append(cand)

    return len(splitters)


INPUT_S = '''\
.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
...............
'''
EXPECTED = 21


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
