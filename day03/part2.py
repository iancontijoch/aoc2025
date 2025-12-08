from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
SLOTS = 12


def compute(s: str) -> int:
    lines = s.splitlines()
    total = 0
    for line in lines:
        digits = {}
        lst = list(enumerate(map(int, line)))
        window_size = len(line) - (SLOTS - 1)

        windows = [
            lst[-i - window_size: len(lst) - i]
            for i in range(SLOTS)
        ][::-1]

        start_idx = 0
        for i, window in enumerate(windows):
            val_idx, max_val = max(window[start_idx:], key=lambda x: x[1])
            start_idx = val_idx - i
            digits[SLOTS - i] = max_val

        num_lst = [x[1] for x in sorted(digits.items())]
        num = sum(x * 10 ** i for (i, x) in enumerate(num_lst))
        total += num
    return total


INPUT_S = '''\
987654321111111
811111111111119
234234234234278
818181911112111
'''

EXPECTED = 3121910778619


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
