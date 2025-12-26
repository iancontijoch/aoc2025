from __future__ import annotations

import argparse
import itertools
import os.path
import re

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def press(button: tuple[int, ...], state: list[int]) -> list[int]:
    new_state = list(state)
    for i in button:
        new_state[i] = 0 if new_state[i] == 1 else 1
    return new_state


def compute(s: str) -> int:
    lines = s.splitlines()
    total = 0

    for line in lines:
        lights_s, *buttons_s, _ = line.split()
        lights = list(
            map(
                int, lights_s[1:-1]
                .replace('.', '0')
                .replace('#', '1'),
            ),
        )
        buttons = tuple(
            tuple(
                map(int, re.findall(r'\d+', b)),
            )
            for b in buttons_s
        )

        dim = max(x for sublist in buttons for x in sublist) + 1
        start = [0] * dim
        n_buttons = len(buttons)
        min_buttons = 10 ** 6

        for button in buttons:
            other_buttons = [b for b in buttons if b != button]
            for j in range(1, n_buttons):
                sequences = list(itertools.combinations(other_buttons, r=j))
                for seq in sequences:
                    state = start.copy()
                    for b in seq:
                        state = press(b, state)
                    if state == lights:
                        min_buttons = min(min_buttons, j)
                        break
        total += min_buttons
    return total


INPUT_S = '''\
[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
'''
EXPECTED = 7


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
