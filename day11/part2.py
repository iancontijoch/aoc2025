from __future__ import annotations

import argparse
import math
import os.path
from collections import defaultdict
from functools import lru_cache

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    lines = s.splitlines()
    graph = defaultdict(list)
    for line in lines:
        parent, children_s = line.split(':')
        children = children_s.split()
        graph[parent].extend(children)

    start, end = 'svr', 'out'

    def count_paths(start: str, end: str) -> int:
        @lru_cache(maxsize=None)
        def dfs(u: str) -> int:
            if u == end:
                return 1
            else:
                return sum(dfs(v) for v in graph[u])
        return dfs(start)

    dac_to_out = count_paths('dac', end)
    fft_to_dac = 0 if dac_to_out == 0 else count_paths('fft', 'dac')
    svr_to_fft = (
        0 if dac_to_out == 0 or fft_to_dac == 0
        else count_paths(start, 'fft')
    )

    svr_to_dac = count_paths(start, 'dac')
    dac_to_fft = 0 if svr_to_dac == 0 else count_paths('dac', 'fft')
    fft_to_out = (
        0 if svr_to_dac == 0 or dac_to_fft == 0
        else count_paths('fft', end)
    )

    return (
        math.prod((svr_to_fft, fft_to_dac, dac_to_out)) +
        math.prod((svr_to_dac, dac_to_fft, fft_to_out))
    )


INPUT_S = '''\
svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out
'''
EXPECTED = 2


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
