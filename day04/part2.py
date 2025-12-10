from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

Coords = dict[tuple[int, int], str]


def compute(s: str) -> int:
    lines = s.splitlines()

    coords = {
        (x, y): c
        for y, line in enumerate(lines)
        for x, c in enumerate(line)
    }

    def do(coords: Coords) -> tuple[Coords, int]:
        total: int = 0
        seen = set()
        for pos in coords:
            if pos in coords and coords[pos] == '@':
                cands = [
                    adj for adj in support.adjacent_8(
                        *pos,
                    ) if adj in coords
                ]
                if ''.join(coords[c] for c in cands).count('@') < 4:
                    seen.add(pos)
                    total += 1

        for pos in coords:
            if pos in seen:
                coords[pos] = '.'

        return coords, total

    total = 0
    while True:
        prev = coords.copy()
        coords, count = do(coords)
        if coords == prev:
            break
        total += count

    return total


INPUT_S = '''\
..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.
'''
EXPECTED = 43


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
