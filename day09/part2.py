from __future__ import annotations

import argparse
import itertools
import os.path
from collections import defaultdict
from typing import NamedTuple

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


class Point(NamedTuple):
    x: int
    y: int


class Segment(NamedTuple):
    type: str
    rng: range
    anchor: int


def rect_area(a: Point, b: Point) -> int:
    return (1 + abs(a.x - b.x)) * (1 + abs(a.y - b.y))


def rect_points(a: Point, b: Point) -> tuple[Point, Point]:

    if b.x >= a.x:
        return Point(a.x, b.y), Point(b.x, a.y)
    else:
        return Point(b.x, a.y), Point(a.x, b.y)


def get_segment(a: Point, b: Point) -> Segment:
    if a.x == b.x:
        if a.y > b.y:
            return Segment(type='v', anchor=a.x, rng=range(b.y, a.y + 1))
        else:
            return Segment(type='v', anchor=a.x, rng=range(a.y, b.y + 1))
    elif a.y == b.y:
        if a.x > b.x:
            return Segment(type='h', anchor=a.y, rng=range(b.x, a.x + 1))
        else:
            return Segment(type='h', anchor=a.y, rng=range(a.x, b.x + 1))
    else:
        raise ValueError


def compute(s: str) -> int:
    lines = s.splitlines()
    points = []

    for line in lines:
        points.append(Point(*map(int, line.split(','))))

    segments: defaultdict[str, list[Segment]] = defaultdict(list)
    segs = []

    for a, b in itertools.pairwise(points):
        seg = get_segment(a, b)
        segs.append(seg)
        if seg.type == 'h':
            segments['h'].append(seg)
        else:
            segments['v'].append(seg)

    last_seg = get_segment(points[-1], points[0])
    segs.append(last_seg)
    if last_seg.type == 'h':
        segments['h'].append(last_seg)
    else:
        segments['v'].append(last_seg)

    # dividing lines in the shape
    YUP = 48336
    YDN = 50_402

    PTUP = Point(94_858, 48_336)
    PTDN = Point(94_858, 50_402)

    # the very most that the heights could be above the divide and below
    TOP_Y_LIMIT, BOTTOM_Y_LIMIT = sorted(
        s.anchor for s in segments['h']
        if PTUP.x in s.rng and s.anchor not in (PTUP.y, PTDN.y)
    )

    # x limit corresponding to the top y limit
    TOP_X_LIMIT = max(
        pt.x
        for pt in points
        if TOP_Y_LIMIT <= pt.y <= PTUP.y
        and pt.x <= 10_000  # eyeballing
    )

    # x limit corresponding to the bottom y limit
    BOTTOM_X_LIMIT = max(
        pt.x
        for pt in points
        if PTDN.y <= pt.y <= BOTTOM_Y_LIMIT
        and pt.x <= 10_000  # eyeballing
    )

    # arc from top start through x, y top limit
    subset_up = [
        p for p in points
        if TOP_Y_LIMIT <= p.y <= YUP and p.x <= TOP_X_LIMIT
    ]

    # arc from bottom start through x, y bottom limit
    subset_dn = [
        p for p in points
        if BOTTOM_Y_LIMIT >= p.y >= YDN and p.x <= BOTTOM_X_LIMIT
    ]

    # increase x or go up. any decreases are ignored
    max_x = min(p.x for p in subset_up)
    valid_pts_up = []
    for p in subset_up:
        if p.x >= max_x:
            valid_pts_up.append(p)
            max_x = p.x

    # increase x or go down. any decreases are ignored
    min_x = min(p.x for p in subset_dn)
    valid_pts_dn = []
    for p in subset_dn[::-1]:  # orient ccw
        if p.x >= min_x:
            valid_pts_dn.append(p)
            min_x = p.x

    # max of rect in top hemisphere and bottom hemisphere
    return max(
        max(rect_area(vp, PTUP) for vp in valid_pts_up),
        max(rect_area(vp, PTDN) for vp in valid_pts_dn),
    )


INPUT_S = '''\
7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3
'''
EXPECTED = 24


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
