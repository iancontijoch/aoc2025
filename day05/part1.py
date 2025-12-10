from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    total = 0
    ranges_s, ids_s = s.split('\n\n')

    ranges = [
        range(start, end + 1)
        for start, end in (
            map(int, line.split('-'))
            for line in ranges_s.splitlines()
        )
    ]

    numbers = support.parse_numbers_split(ids_s)
    for n in numbers:
        for rng in ranges:
            if n in rng:
                total += 1
                break

    return total


INPUT_S = '''\
3-5
10-14
16-20
12-18

1
5
8
11
17
32
'''
EXPECTED = 3


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
