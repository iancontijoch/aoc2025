from __future__ import annotations

import argparse
import itertools
import os.path
import random
from collections import deque
from collections.abc import Sequence

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def done(ranges: Sequence[range]) -> bool:
    statuses = []
    for rng, other in itertools.combinations(ranges, 2):
        before = rng.stop <= other.start
        after = rng.start > other.stop
        statuses.append(before or after)

    return all(statuses)


def do(rng: range, other: range) -> Sequence[range]:
    # rng fully embedded
    if rng.start >= other.start and rng.stop <= other.stop:
        return (other,)
    # other fully embedded
    if other.start >= rng.start and other.stop <= rng.stop:
        return (rng,)
    # rng starts before but ends inside
    elif (
        rng.start <= other.start
        and (other.start <= rng.stop)
        and (rng.stop <= other.stop)
    ):
        return (range(rng.start, other.stop),)
    # rng starts inside but ends after
    elif (
        rng.start >= other.start
        and (rng.start <= other.stop)
        and (rng.stop >= other.stop)
    ):
        return (range(other.start, rng.stop),)
    # rng all before
    elif rng.stop <= other.start:
        return (rng, other)
    # rng all after
    elif rng.start > other.stop:
        return (other, rng)
    else:
        raise NotImplementedError


def compute(s: str) -> int:
    ranges_s, _ = s.split('\n\n')

    ranges = [
        range(start, end + 1)
        for start, end in (
            map(int, line.split('-'))
            for line in ranges_s.splitlines()
        )
    ]

    q = deque(ranges)
    while not done(q):
        rng1, rng2 = q.popleft(), q.popleft()
        res = do(rng1, rng2)
        random.shuffle(list(res))
        for rng in res:
            if random.randint(0, 1):
                q.append(rng)
            else:
                q.appendleft(rng)

    consolidated_ranges = sorted(q, key=lambda x: x.start)
    return sum(len(rng) for rng in consolidated_ranges)


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
EXPECTED = 14


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, EXPECTED),
    ),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


@pytest.mark.parametrize(
    ('ranges', 'expected'),
    (
        # rng starts before but ends inside
        ((range(10, 14), range(12, 18)), ((range(10, 18),))),
        # rng starts after but ends after
        ((range(10, 14), range(8, 12)), ((range(8, 14),))),
        # rng starts inside but ends after
        ((range(10, 20), range(9, 14)), ((range(9, 20),))),
        ((range(2, 5), range(7, 10)), ((range(2, 5), range(7, 10)))),
        ((range(10, 20), range(10, 20)), ((range(10, 20),))),
        ((range(10, 20), range(7, 9)), ((range(7, 9), range(10, 20)))),
        ((range(10, 15), range(12, 21)), ((range(10, 21),))),

    ),
)
def test_do(ranges: tuple[range, range], expected: Sequence[range]) -> None:
    assert do(*ranges) == expected


@pytest.mark.parametrize(
    ('ranges', 'expected'),
    (
        ([range(3, 6), range(10, 15), range(12, 19), range(16, 21)], False),
        ([range(3, 6), range(10, 15)], True),
        ([range(10, 15), range(12, 21)], False),
    ),
)
def test_done(ranges: Sequence[range], expected: bool) -> None:
    assert done(ranges) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
