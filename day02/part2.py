from __future__ import annotations

import argparse
import os.path

import pytest
import sympy

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    total = 0
    lines = s.splitlines()
    for line in lines:
        ranges = line.split(',')
        for rng in ranges:
            start_s, end_s = rng.split('-')
            start, end = int(start_s), int(end_s)
            for n in range(start, end + 1):
                n_s = str(n)
                divisors = sympy.divisors(len(n_s))
                for divisor in divisors:
                    parts = [
                        ''.join(chunk) for chunk in zip(
                            *[iter(n_s)] * divisor,
                        )
                    ]
                    if len(parts) > 1 and len(set(parts)) == 1:
                        total += n
                        break
    return total


INPUT_S = '''\
11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124
'''

EXPECTED = 4174379265


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
