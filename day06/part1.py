from __future__ import annotations

import argparse
import math
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    lines = s.splitlines()[:-1]
    ops_s = s.splitlines()[-1]

    nums = [
        list(map(int, line.strip().split()))
        for line in lines
    ]

    ops = ops_s.strip().split()
    groups = list(zip(*nums))
    todo = zip(groups, ops)

    return sum(
        math.prod(group)
        if op == '*' else sum(group)
        for group, op in todo
    )


INPUT_S = '''\
123 328  51 64
 45 64  387 23
  6 98  215 314
*   +   *   +
'''
EXPECTED = 4277556


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
