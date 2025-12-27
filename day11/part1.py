from __future__ import annotations

import argparse
import os.path
from collections import defaultdict
from collections import deque

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

    start, end = 'you', 'out'

    def bfs(
        start: str, end: str, seen: set[str] | None = None,
        path: list[str] | None = None,
    ) -> list[list[str]]:
        if path is None:
            path = []
        if seen is None:
            seen = set()
        paths = []
        q = deque([(start, seen, path)])
        while q:
            pos, seen, path = q.popleft()
            if pos == end:
                paths.append(path)
            if pos in seen:
                continue
            seen.add(pos)
            for cand in graph[pos]:
                q.append((cand, seen.copy(), path + [pos]))
        return paths

    paths = bfs(start, end)
    return len(paths)


INPUT_S = '''\
aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out
'''
EXPECTED = 5


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
