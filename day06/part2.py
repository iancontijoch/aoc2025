from __future__ import annotations

import argparse
import math
import os.path
from collections import defaultdict

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    total = 0
    lines = s.splitlines()[:-1]
    ops_s = s.splitlines()[-1]
    ops = ops_s.split()
    spaces = [True] * len(lines[0])

    for line in lines:
        for i, c in enumerate(line):
            if not c.isspace():
                spaces[i] = False

    gutters = [i for i, flag in enumerate(spaces) if flag] + [len(lines[0])]

    nums = defaultdict(list)
    for line in lines:
        for i, gutter in enumerate(gutters):
            if i == 0:
                nums[i].append(line[0:gutter])
            else:
                nums[i].append(line[gutters[i-1] + 1: gutter])

    lst = list(nums.values())
    groups = [list(zip(*x)) for x in lst]
    instructions = list(zip(groups, ops))

    for group, op in instructions:
        collection = []
        for g in group:
            num = int(''.join(g).strip())
            collection.append(num)
        total += math.prod(collection) if op == '*' else sum(collection)

    return total


INPUT_S = '''\
123 328  51 64
 45 64  387 23
  6 98  215 314
*   +   *   +
'''
EXPECTED = 3263827


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
