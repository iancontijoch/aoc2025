from __future__ import annotations

import argparse
import os.path

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
    start = next(pos for pos, c in coords.items() if c == 'S')
    vals = {
        pos: 0 if pos != start else 1
        for pos in coords
    }

    for y in range(1, len(lines)):
        row = [pos for pos in vals if pos[1] == y]
        for pos in row:
            above = (
                support.Direction4.apply(support.Direction4.UP, *pos)
            )
            if coords[pos] == '^':
                left = (
                    support.Direction4.apply(support.Direction4.LEFT, *pos)
                )
                right = (
                    support.Direction4.apply(support.Direction4.RIGHT, *pos)
                )
                if left in coords and above in coords:
                    # copy value going into splitter
                    vals[left] += vals[above]
                if right in vals and above in vals:
                    # copy value going into splitter
                    vals[right] += vals[above]
                continue
            if above in coords and coords[above] != '^':
                # descend the value
                vals[pos] += vals[above]
    return sum(v for k, v in vals.items() if k[1] == len(lines) - 1)


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

EXPECTED = 40


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
