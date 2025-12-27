from __future__ import annotations

import argparse
import os.path
import re

import pytest
import z3

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    lines = s.splitlines()
    total = 0

    for line in lines:
        _, *buttons_s, joltage = line.split()
        buttons = tuple(
            tuple(
                map(int, re.findall(r'\d+', b)),
            )
            for b in buttons_s
        )

        joltage_lst = tuple(map(int, joltage[1:-1].split(',')))
        # highest button
        dim = max(x for sublist in buttons for x in sublist) + 1

        sol = z3.Optimize()
        X = [z3.IntVector(f'x{i}', dim) for i in range(len(buttons))]
        B = z3.IntVector('b', len(buttons))  # vector with number of presses
        J = z3.IntVector('j', len(joltage_lst))

        for i, j in enumerate(joltage_lst):
            # setup solution vector
            sol.add(J[i] == j)

        for seq, x in zip(buttons, X):
            # setup button vectors
            for i in seq:
                sol.add(x[i] == 1)
            for i in range(len(x)):
                if i not in seq:
                    sol.add(x[i] == 0)

        for i in range(dim):
            # require that b0 * x0[0] + b1 * x1[0] + ... = j[0]
            # b0 * x0[1] + b1 * x1[1] + b2 * x2[1] + ... = j[1]
            sol.add(
                z3.Sum(
                    X[j][i] * B[j]
                    for j in range(len(buttons))
                ) == J[i],
            )

        sol.add([b >= 0 for b in B])
        presses = z3.Int('presses')
        sol.add(presses == z3.Sum(B))
        sol.minimize(presses)

        if sol.check() == z3.sat:
            m = sol.model()
            num_presses = m[presses].as_long()
            total += num_presses

    return total


INPUT_S = '''\
[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
'''
EXPECTED = 33


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
