from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    lines = s.splitlines()
    total = 0
    for line in lines:
        lst = list(map(int, line))
        i, j = 0, len(lst) - 1
        max_left, max_right = 0, 0
        max_i, max_j = i, j
        first, second = None, None

        while i < len(lst):
            if lst[i] > max_left:
                max_left = lst[i]
                max_i = i
            i += 1

        while j > max_i:
            if lst[j] > max_right:
                max_right = lst[j]
                max_j = j
            j -= 1

        if max_i == max_j:  # overlap, find next largest num on left
            max_left = 0
            i = 0
            max_right = lst[-1]
            while i < max_j:
                if lst[i] > max_left:
                    max_left = lst[i]
                    max_i = i
                i += 1

        first, second = str(max_left), str(max_right)
        total += int(first + second)

    return total


INPUT_S = '''\
987654321111111
811111111111119
234234234234278
818181911112111
'''
EXPECTED = 357


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
