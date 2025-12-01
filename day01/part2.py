from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    total = 0
    pos = 50
    lines = s.splitlines()
    for line in lines:
        dir, n = line[0], int(line[1:])
        for _ in range(n):
            pos += 1 if dir == 'R' else -1
            pos = pos % 100
            if pos == 0:
                total += 1
    return total


INPUT_S = '''\
L68
L30
R48
L5
R60
L55
L1
L99
R14
L82
'''
EXPECTED = 6


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
