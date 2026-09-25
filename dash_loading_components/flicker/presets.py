"""Original flip-dot presets for dlc.flicker, designed by PhylaTech.

Every preset is a loop of frames on flicker-dot's 7x7 grid, one frame per
150ms at rate 1.0. A frame is seven strings of seven characters, ``#`` lit
and ``.`` dark; that is also a grid format ``dlc.flicker.Spinner`` accepts,
so any preset can be copied out and edited::

    frames = [list(f) for f in dlc.flicker.PRESETS["Mycelium"].frames]
    frames[0][3] = "...#..."
    dlc.flicker.Spinner(grids=frames)

The designs are our own, drawn for this package and MIT licensed with it.
They are built from the helpers below rather than typed out, so a loop stays
seamless when one is retuned. tests/test_flicker_presets.py holds every
preset to the same rules: a lit dot in every frame, motion inside the 5x5
safe area, no stutter where the loop wraps, and no preset that duplicates
another.
"""
from __future__ import annotations

import itertools
import math
from typing import Iterable, NamedTuple

N = 7
MID = 3

Cell = tuple[int, int]
Frame = tuple[str, ...]


class Preset(NamedTuple):
    category: str
    blurb: str
    frames: tuple[Frame, ...]


def draw(cells: Iterable[Cell]) -> Frame:
    lit = {(r, c) for r, c in cells if 0 <= r < N and 0 <= c < N}
    return tuple("".join("#" if (r, c) in lit else "." for c in range(N)) for r in range(N))


def art(*rows: str) -> set[Cell]:
    """Cells from a hand-drawn picture, one string per row."""
    return {(r, c) for r, row in enumerate(rows) for c, ch in enumerate(row) if ch == "#"}


def shift(cells: Iterable[Cell], dr: int = 0, dc: int = 0) -> set[Cell]:
    return {(r + dr, c + dc) for r, c in cells}


def ring_path(k: int) -> list[Cell]:
    """The square ring k steps out from the center, clockwise from top left."""
    if k == 0:
        return [(MID, MID)]
    lo, hi = MID - k, MID + k
    top = [(lo, c) for c in range(lo, hi)]
    right = [(r, hi) for r in range(lo, hi)]
    bottom = [(hi, c) for c in range(hi, lo, -1)]
    left = [(r, lo) for r in range(hi, lo, -1)]
    return top + right + bottom + left


# A round circle of radius ~2, clockwise from 12 o'clock.
ROUND = [(1, 3), (1, 4), (2, 5), (3, 5), (4, 5), (5, 4),
         (5, 3), (5, 2), (4, 1), (3, 1), (2, 1), (1, 2)]


def ray(angle: float, start: float, stop: float) -> set[Cell]:
    """Cells along a ray from the center, angle in degrees clockwise from 12."""
    rad = math.radians(angle)
    out = set()
    steps = int((stop - start) * 4) + 1
    for i in range(steps):
        d = start + (stop - start) * i / max(steps - 1, 1)
        out.add((round(MID - d * math.cos(rad)), round(MID + d * math.sin(rad))))
    return out


def bounce(seq: list) -> list:
    """seq followed by its reverse, without repeating either end."""
    return seq + seq[-2:0:-1]


# ---------------------------------------------------------------------------
# Field: the naturalist set
# ---------------------------------------------------------------------------

def mycelium():
    # Hyphae branch out from a spore, then the colony hollows from its old
    # center, leaving only the growing tips before a new spore lands.
    age = {
        (3, 3): 0,
        (2, 3): 1, (3, 4): 1, (4, 2): 1,
        (1, 2): 2, (2, 5): 2, (4, 4): 2, (5, 1): 2,
        (0, 2): 3, (1, 1): 3, (1, 5): 3, (5, 5): 3, (6, 1): 3, (5, 0): 3,
        (0, 0): 4, (0, 6): 4, (6, 5): 4, (5, 6): 4, (6, 0): 4,
    }
    grow = [{c for c, a in age.items() if a <= t} for t in range(5)]
    hollow = [{c for c, a in age.items() if a >= t} for t in range(1, 5)]
    return grow + [grow[-1]] + hollow


def spore_ring():
    # Spores thrown off in rings, two rings in flight at once.
    def band(k):
        return {(r, c) for r in range(N) for c in range(N)
                if round(math.hypot(r - MID, c - MID)) == k and (r + c + k) % 2 == 0}
    # Radius 4 is the corners, so a ring leaves the grid before the next
    # one starts; each position holds two frames so the rings read as moving.
    frames = []
    for step in range(5):
        frame = band(step) | band((step + 2) % 5)
        frames += [frame, frame]
    return frames


def firefly():
    # Fireflies drifting as they glow, never more than two at once.
    flies = [
        (0, [(2, 1), (1, 1), (1, 2)]),
        (2, [(5, 4), (4, 4), (4, 5)]),
        (5, [(1, 4), (2, 4), (2, 5)]),
        (8, [(5, 1), (4, 2), (4, 1)]),
        (10, [(3, 3), (2, 3), (2, 2)]),
        (13, [(4, 3), (5, 3), (5, 2)]),
    ]
    frames = [set() for _ in range(16)]
    for start, path in flies:
        for i, cell in enumerate(path):
            frames[(start + i) % 16].add(cell)
    return frames


def tide():
    # Water rising and falling, its surface rolling as it goes.
    frames = []
    for f, level in enumerate([1, 2, 3, 3, 2, 1]):
        body = {(r, c) for r in range(N - level, N) for c in range(N)}
        crest = {(N - level - 1, c) for c in range(N) if (c + f) % 3 == 0}
        frames.append(body | crest)
    return frames


def mass_spec():
    # A mass spectrum being acquired: the scan runs up the m/z axis and each
    # centroid peak lands as it passes, a tall monoisotopic peak trailed by
    # its smaller isotope peaks. Thin sticks on a baseline, unlike Equalizer's
    # bouncing bars.
    baseline = {(6, c) for c in range(N)}
    peaks = {1: 5, 2: 2, 3: 1, 5: 3, 6: 1}
    frames, acquired = [], set()
    for col in range(N):
        acquired = acquired | {(r, col) for r in range(6 - peaks.get(col, 0), 6)}
        frames.append(baseline | acquired | {(5, col)})
    return frames + [baseline | acquired] * 3


def jellyfish():
    # A jellyfish pulsing: the bell squeezes narrow and it rises, then opens
    # wide, its tentacles swaying, and it sinks back as it drifts.
    open_bell = art(".#####.", "#.....#", ".#.#.#.", "#.#.#..", ".#.#.#.")
    closing = art("..###..", ".#...#.", ".#.#.#.", "..#.#..", "..#.#..")
    closed = art("..###..", ".#...#.", ".#...#.", "..#.#..", "..#.#..", "..#.#..")
    sway = art(".#####.", "#.....#", ".#.#.#.", "..#.#.#", ".#.#.#.")
    return [shift(open_bell, 1), shift(closing, 1), shift(closed, 0), shift(closed, 0),
            shift(closing, 0), shift(open_bell, 0), shift(sway, 1), shift(open_bell, 2), shift(sway, 2)]


def test_tube():
    # A test tube on the bench, bubbles rising through it and off the rim.
    tube = {(r, 1) for r in range(6)} | {(r, 5) for r in range(6)} | {(6, 2), (6, 3), (6, 4)}
    liquid = {(r, c) for r in (4, 5) for c in (2, 3, 4)}
    bubbles = [(2, 0), (4, 3), (3, 6)]  # (column, frame it leaves the liquid)
    frames = []
    for f in range(8):
        cells = set(tube | liquid)
        for col, start in bubbles:
            r = 3 - (f - start) % 8
            if r >= 0:
                cells.add((r, col))
        frames.append(cells)
    return frames


def fish():
    # A fish swimming across, its tail beating as it goes.
    tail_out = art("#..##..", ".#####.", "#..##..")
    tail_in = art("...##..", "######.", "...##..")
    return [shift(tail_out if i % 2 == 0 else tail_in, 2, dc) for i, dc in enumerate(range(-5, 7))]


def snail():
    # A snail gliding along, feelers waving, as the ground slides beneath.
    shell = shift(art(".###...", "#...#..", "#.#.#..", "#..##.."), 1)
    body = {(5, c) for c in range(N)}
    feelers = [{(4, 6), (3, 6)}, {(4, 6), (3, 5)}]
    frames = []
    for f in range(6):
        ground = {(6, c) for c in range(N) if (c + f) % 3 != 0}
        frames.append(shell | body | feelers[(f // 2) % 2] | ground)
    return frames


def leaf():
    # A leaf falling, swaying side to side and tipping at each turn.
    tip_right = {(0, 0), (0, 1), (1, 1)}
    tip_left = {(0, 0), (0, 1), (1, 0)}
    sway = [1, 2, 3, 4, 3, 2, 1]
    frames = []
    for r, c in enumerate(sway):
        heading_right = r < len(sway) - 1 and sway[r + 1] > c
        frames.append(shift(tip_right if heading_right else tip_left, r - 1, c))
    return frames


def ant():
    # An ant walking on the spot, its legs stepping in alternate tripods. A
    # one-dot gap keeps legs and body apart, so only the legs read as moving.
    body = art(".......", "..#.#..", "...#...", "...#...", "...#...", "...#...")
    tripod_a = {(2, 1), (4, 1), (3, 5)}
    tripod_b = {(2, 5), (4, 5), (3, 1)}
    return [body | legs for legs in (tripod_a, tripod_a, tripod_b, tripod_b)]


def frond():
    # A fern: the rachis grows, leaflets open in pairs from the base up.
    stem = [(r, 3) for r in range(5, 0, -1)]
    inner = [{(r, 2), (r, 4)} for r in range(5, 0, -1)]
    outer = [{(r, 1), (r, 5)} for r in range(5, 2, -1)]
    frames, lit = [], set()
    for cell in stem:
        lit = lit | {cell}
        frames.append(lit)
    for pair in inner + outer:
        lit = lit | pair
        frames.append(lit)
    return frames + [lit]


def diatom():
    # A centric diatom: striae turning slowly inside the round frustule.
    inner = ring_path(1)
    frames = []
    for f in range(4):
        striae = {inner[f], inner[f + 4], (3, 3)}
        frames += [set(ROUND) | striae] * 2
    return frames


def cladogram():
    # A tree of life drawn from the root up to its tips, then pruned back.
    tree = art(
        "#.#.#.#",
        "#.#.#.#",
        "###.###",
        ".#...#.",
        ".#####.",
        "...#...",
        "...#...",
    )
    depth = {(6, 3): 0}
    queue = [(6, 3)]
    while queue:
        r, c = queue.pop(0)
        for nb in ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)):
            if nb in tree and nb not in depth:
                depth[nb] = depth[(r, c)] + 1
                queue.append(nb)
    # One depth per frame, so every branch appears after the one it grows
    # from, and pruning takes the tips first.
    grown = [{c for c, d in depth.items() if d <= t} for t in range(max(depth.values()) + 1)]
    return bounce(grown + [grown[-1]])


def helix():
    # DNA turning: two strands crossing, base pairs where they stand apart.
    frames = []
    for f in range(8):
        cells = set()
        for r in range(N):
            phase = 2 * math.pi * (r + f) / 8
            dx = round(2 * math.sin(phase))
            cells |= {(r, MID + dx), (r, MID - dx)}
            if abs(dx) == 2:
                cells |= {(r, MID - 1), (r, MID), (r, MID + 1)}
        frames.append(cells)
    return frames


def colony():
    # A petri dish: colonies land, grow, and die back in the order they came.
    seeds = [(2, 2), (4, 4), (2, 5), (5, 1)]
    plus = lambda r, c: {(r, c), (r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)}
    stage = [0] * len(seeds)
    frames = []

    def snapshot():
        cells = set()
        for (r, c), s in zip(seeds, stage):
            cells |= {(r, c)} if s == 1 else plus(r, c) if s == 2 else set()
        return cells

    for i in range(len(seeds)):
        for s in (1, 2):
            stage[i] = s
            frames.append(snapshot())
    frames.append(snapshot())
    for i in range(len(seeds)):
        for s in (1, 0):
            stage[i] = s
            if s or i < len(seeds) - 1:
                frames.append(snapshot())
    return frames


def waggle():
    # A honeybee's waggle dance: a shaking run up the middle, a loop back
    # round one side, another run, a loop round the other.
    run = [(5, 3), (4, 2), (3, 3), (2, 4), (1, 3)]
    right = [(1, 4), (2, 5), (3, 5), (4, 5), (5, 4)]
    left = [(1, 2), (2, 1), (3, 1), (4, 1), (5, 2)]
    path = run + right + run + left
    return [{path[i], path[i - 1]} for i in range(len(path))]


def mitosis():
    # A cell pinching in two and the daughters drawing back together.
    one = art(".......", "..###..", ".#...#.", ".#.#.#.", ".#...#.", "..###..", ".......")
    long = art(".......", ".#####.", "#.....#", "#.#.#.#", "#.....#", ".#####.", ".......")
    pinch = art(".......", ".##.##.", "#..#..#", "#.#.#.#", "#..#..#", ".##.##.", ".......")
    two = art(".......", ".......", ".#...#.", "#.#.#.#", ".#...#.", ".......", ".......")
    return [one, one, long, pinch, two, two, pinch, long]


def seedling():
    # A seed in the soil sending up a shoot that opens its first leaves.
    soil = {(6, c) for c in range(N)}
    stages = [
        {(5, 3)},
        {(5, 3), (4, 3)},
        {(5, 3), (4, 3), (3, 3)},
        {(5, 3), (4, 3), (3, 3), (2, 2), (2, 4)},
        {(5, 3), (4, 3), (3, 3), (2, 3), (2, 2), (2, 4), (1, 1), (1, 5)},
        {(5, 3), (4, 3), (3, 3), (2, 3), (2, 2), (2, 4), (1, 1), (1, 2), (1, 4), (1, 5)},
    ]
    frames = [soil | s for s in stages]
    return frames + [frames[-1], frames[-1]]


def chromatogram():
    # Thin-layer chromatography: three lanes of spots climbing the plate at
    # their own retention factors until the solvent front stops them.
    lanes = [(1, (1.0, 0.25)), (3, (0.75, 0.5)), (5, (1.0, 0.5))]
    frames = []
    for t in range(5):
        cells = set()
        for col, rates in lanes:
            cells |= {(round(5 - t * rate), col) for rate in rates}
        frames.append(cells)
    return frames + [frames[-1], frames[-1]]


# ---------------------------------------------------------------------------
# Data: charts drawing themselves, for dashboards waiting on a query
# ---------------------------------------------------------------------------

def scatter():
    # Points landing one by one along a rising trend, on a pair of axes.
    axes = {(r, 0) for r in range(N)} | {(6, c) for c in range(N)}
    points = [(5, 2), (4, 1), (3, 3), (4, 4), (2, 4), (3, 5), (1, 5), (2, 6), (1, 3)]
    frames = [axes | set(points[:i]) for i in range(1, len(points) + 1)]
    return frames + [frames[-1], frames[-1], axes]


def histogram():
    # Bins filling left to right into a bell curve, then emptying.
    heights = [1, 2, 4, 6, 4, 2, 1]
    bars = [{(r, c) for r in range(N - h, N)} for c, h in enumerate(heights)]
    grow = [set().union(*bars[: i + 1]) for i in range(N)]
    return grow + [grow[-1], grow[-1]] + [set().union(*bars[i:]) for i in range(1, N)]


def pie_chart():
    # A pie filling slice by slice, clockwise from twelve, then emptying the
    # same way round.
    disc = [(r, c) for r in range(N) for c in range(N) if math.hypot(r - MID, c - MID) <= 2.6]
    angle = {cell: math.degrees(math.atan2(cell[1] - MID, MID - cell[0])) % 360 for cell in disc}
    center = {(MID, MID)}
    fill = [center | {c for c in disc if angle[c] < 45 * (i + 1)} for i in range(8)]
    empty = [center | {c for c in disc if angle[c] >= 45 * (i + 1)} for i in range(7)]
    return fill + [fill[-1]] + empty


def heatmap():
    # A hot spot wandering a heat map: dense at its core, thinning to a
    # sparse speckle at the edge.
    frames = []
    for f in range(8):
        a = 2 * math.pi * f / 8
        hr, hc = MID + 1.2 * math.sin(a), MID + 1.2 * math.cos(a)
        cells = set()
        for r in range(N):
            for c in range(N):
                d = math.hypot(r - hr, c - hc)
                if d < 1.2 or (d < 2.4 and (r + c) % 2 == 0) or (d < 3.4 and r % 2 == 0 and c % 2 == 0):
                    cells.add((r, c))
        frames.append(cells)
    return frames


def line_chart():
    # A line drawn point to point across a pair of axes.
    axes = {(r, 0) for r in range(N)} | {(6, c) for c in range(N)}
    ys = [5, 4, 4, 2, 3, 1]
    frames, line = [], set()
    for i, y in enumerate(ys):
        col = i + 1
        prev = ys[i - 1] if i else y
        line |= {(r, col) for r in range(min(prev, y), max(prev, y) + 1)} if i else {(y, col)}
        frames.append(axes | line)
    return frames + [frames[-1], frames[-1], axes]


def database():
    # A database filling up, disk by disk from the bottom.
    disks = art(".#####.", "#.....#", ".#####.", "#.....#", ".#####.", "#.....#", ".#####.")
    bands = [{(r, c) for c in range(1, 6)} for r in (5, 3, 1)]
    frames = [disks | set().union(*bands[:i]) for i in range(len(bands) + 1)]
    return frames + [frames[-1]]


# ---------------------------------------------------------------------------
# Everyday: the waits people meet in any app
# ---------------------------------------------------------------------------

def cart():
    # A shopping cart rolling in, an item dropping into it, and off it goes.
    body = art("#......", ".#####.", ".#...#.", ".#####.", "..#.#..")
    item = [(0, 3), (1, 3), (3, 3)]
    at_rest = shift(body, 2)
    frames = [shift(at_rest, 0, dc) for dc in (-5, -3, -1)]
    frames += [at_rest | {cell} for cell in item[:2]] + [at_rest | {(4, 3)}, at_rest | {(4, 3)}]
    frames += [shift(at_rest | {(4, 3)}, 0, dc) for dc in (2, 4, 6)]
    return frames


def upload():
    # Arrows streaming up out of a tray.
    tray = {(5, 0), (5, 6)} | {(6, c) for c in range(N)}
    arrow = art("...#...", "..###..", ".#.#.#.", "...#...")
    return [tray | {(r, c) for r, c in shift(arrow, -f) | shift(arrow, 5 - f) if 0 <= r < 5} for f in range(5)]


def magnifier():
    # A magnifying glass circling as it searches.
    glass = set(ring_path(1)) - {(MID, MID)}
    handle = {(MID + 2, MID + 2), (MID + 3, MID + 3)}
    path = [(-1, -1), (-1, 0), (0, 0), (0, -1)]
    return [shift(glass | handle, dr, dc) for dr, dc in path for _ in range(2)]


def download():
    # Arrows streaming down into a tray.
    tray = {(5, 0), (5, 6)} | {(6, c) for c in range(N)}
    arrow = art("...#...", ".#.#.#.", "..###..", "...#...")
    return [tray | {(r, c) for r, c in shift(arrow, f) | shift(arrow, f - 5) if 0 <= r < 5} for f in range(5)]


def walker():
    # A figure walking on the spot. Head and shoulders never move; only the
    # limbs do, through a four-pose cycle (stride, closing, passing, closing),
    # so the legs open and close instead of the whole figure jumping between
    # two shapes.
    stride = art("...#...", "..###..", ".#.#.#.", "...#...", "..#.#..", ".#...#.", ".#...#.")
    closing = art("...#...", "..###..", ".#.#.#.", "...#...", "..#.#..", "..#.#..", ".#...#.")
    passing = art("...#...", "..###..", "..###..", "...#...", "...#...", "...##..", "...#...")
    return [stride, closing, passing, closing]


def runner():
    # A figure running on the spot, leaning into it. As with Walker the head
    # and torso hold still; the arms pump bent at the elbow and the legs run
    # a four-pose cycle: flight (both feet up, full split), landing, passing
    # (knee driven high) and toe-off.
    body = {(0, 4), (1, 3), (1, 4), (2, 3), (3, 3)}
    poses = [
        ({(2, 2), (3, 1), (2, 4), (1, 5)}, {(4, 2), (5, 1), (4, 4), (4, 5), (5, 6)}),
        ({(2, 2), (3, 2), (2, 4), (3, 5)}, {(4, 2), (5, 2), (6, 1), (4, 4), (5, 4), (6, 4)}),
        ({(2, 2), (2, 4)}, {(4, 3), (5, 3), (6, 3), (4, 4), (4, 5), (5, 5)}),
        ({(2, 4), (3, 5), (2, 2), (1, 1)}, {(4, 3), (5, 2), (6, 1), (4, 4), (3, 5)}),
    ]
    return [body | arms | legs for arms, legs in poses]


def mail():
    # A letter dropping into its envelope and the flap folding shut.
    envelope = art(".......", ".......", "#######", "#.....#", "#.....#", "#.....#", "#######")
    flap = {(3, 1), (4, 2), (5, 3), (4, 4), (3, 5)}
    letter = art("..###..", "..###..")
    frames = [envelope | shift(letter, dr) for dr in (-1, 0, 1)]
    return frames + [envelope, envelope | flap, envelope | flap, envelope | flap]


def wifi():
    # A signal finding its bars, arc by arc, then searching again.
    def arc(k):
        return {(r, c) for r in range(N) for c in range(N)
                if r < 6 and round(math.hypot(r - 6, c - MID)) == k and abs(c - MID) <= r - 6 + k + 1}
    levels = [{(6, 3)}]
    for k in (2, 4, 6):
        levels.append(levels[-1] | arc(k))
    return levels + [levels[-1]]


def battery():
    # A battery charging, one cell at a time.
    case = {(1, c) for c in range(6)} | {(5, c) for c in range(6)} | {(r, 0) for r in range(1, 6)} \
        | {(r, 5) for r in range(1, 6)} | {(2, 6), (3, 6), (4, 6)}
    cells = [{(r, c) for r in (2, 3, 4)} for c in range(1, 5)]
    frames = [case | set().union(*cells[:i]) for i in range(len(cells) + 1)]
    return frames + [frames[-1]]


def truck():
    # A delivery truck on its way, the road markings rushing past.
    # The road runs on row 5, inside the 5x5 safe area, so variant="5x5" moves too.
    body = art("####...", "####.#.", "######.", "######.", ".#..#..")
    return [body | {(5, c) for c in range(N) if (c + f) % 3 != 2} for f in range(3)]


def bell():
    # A bell ringing: the clapper swings and strikes, a ring on each side.
    body = art("...#...", "..###..", ".#...#.", ".#...#.", "#######")
    clapper = [(5, 3), (5, 2), (5, 3), (5, 4)]
    rings = [set(), {(1, 0), (0, 1)}, set(), {(1, 6), (0, 5)}]
    return [body | {clapper[i]} | rings[i] for i in range(4) for _ in range(2)]


def heart():
    # A heart beating, lub-dub, then resting before the next beat.
    small = art(".......", ".......", "..#.#..", ".#####.", "..###..", "...#...")
    big = art(".......", ".##.##.", "#######", ".#####.", "..###..", "...#...")
    # Starts on the beat, so the rest at the end runs straight into it.
    return [big, small, big, small, small, small, small, small]


def chat():
    # A speech bubble with someone typing: three dots rising in turn.
    bubble = art(".#####.", "#.....#", "#.....#", "#.....#", ".#####.", ".#.....", "#......")
    return [bubble | {(3 - (c == col), c) for c in (2, 3, 4)} for col in (2, 3, 4, None)]


def cloud_sync():
    # A cloud syncing: a ring turning beneath it, its gap chasing round.
    cloud = art("..##...", ".#..##.", "#.....#", "#######")
    ring = shift(ring_path(1), 2) - {(5, 3)}
    order = [(4, 2), (4, 3), (4, 4), (5, 4), (6, 4), (6, 3), (6, 2), (5, 2)]
    return [cloud | (ring - {order[f], order[(f + 1) % 8]}) for f in range(8)]


def lock():
    # A padlock opening: the shackle lifts and swings free, then locks again.
    body = art(".......", ".......", ".......", ".......", ".#####.", ".##.##.", ".#####.")
    shut = {(1, 2), (1, 3), (1, 4), (2, 2), (2, 4), (3, 2), (3, 4)}
    lifted = shift(shut, -1) - {(2, 4)}
    open_ = lifted - {(1, 4)}
    return [body | shut] * 3 + [body | lifted] + [body | open_] * 3 + [body | lifted]


# ---------------------------------------------------------------------------
# Board: what a flip-dot panel does in a station or a stadium
# ---------------------------------------------------------------------------

def departures():
    # Three lines of a departure board ticking past at their own pace.
    lines = [(2, "##.#...", 1), (3, "#.###..", 2), (4, "###.#..", 1)]
    frames = []
    for f in range(7):
        cells = set()
        for r, pattern, speed in lines:
            cells |= {(r, c) for c in range(N) if pattern[(c + f * speed) % N] == "#"}
        frames.append(cells)
    return frames


def split_flap():
    # A split-flap sign cycling through its glyphs. Mid-flip, the top half
    # already shows the next glyph, the bottom half the last, and the flap
    # itself is a bar across the hinge.
    glyphs = [
        set(ROUND),
        {(r, c) for r in range(N) for c in range(N) if abs(r - MID) + abs(c - MID) == 2},
        set(ring_path(2)),
        {(MID + d, MID + e) for d in (-2, -1, 1, 2) for e in (d, -d)} | {(MID, MID)},
    ]
    hinge = {(MID, c) for c in range(1, 6)}
    frames = []
    for i, glyph in enumerate(glyphs):
        nxt = glyphs[(i + 1) % len(glyphs)]
        flip = {(r, c) for r, c in nxt if r < MID} | {(r, c) for r, c in glyph if r > MID} | hinge
        frames += [glyph, glyph, flip]
    return frames


def marquee():
    # Chase lights running round a theatre sign.
    ring = ring_path(2)
    return [{cell for i, cell in enumerate(ring) if (i + f) % 4 < 2} | {(3, 3)} for f in range(4)]


def scanline():
    # A scan bar sweeping down the panel and back up.
    rows = bounce(list(range(1, 6)))
    return [{(r, c) for c in range(N)} for r in rows]


def equalizer():
    # Five level meters, each on its own beat.
    beats = [(1, 0.0), (2, 1.2), (1, 2.4), (3, 0.6), (2, 3.3)]
    frames = []
    for f in range(12):
        cells = set()
        for i, (k, phase) in enumerate(beats):
            h = 1 + round(2 + 2 * math.sin(2 * math.pi * k * f / 12 + phase))
            cells |= {(r, i + 1) for r in range(6 - h, 6)}
        frames.append(cells)
    return frames


def typewriter():
    # Lines typed out a character at a time, the cursor blinking at the end,
    # then the carriage returns.
    lines = [(1, 5), (3, 4), (5, 3)]
    frames, typed = [], set()
    for r, length in lines:
        for c in range(1, 1 + length):
            typed = typed | {(r, c)}
            frames.append(typed)
    cursor = (5, 5)
    frames += [typed | {cursor}, typed, typed | {cursor}]
    return frames


def rain():
    # Streaks of rain falling at two speeds.
    drops = [(1, 0, 1), (3, 3, 1), (5, 5, 1), (2, 1, 2), (4, 4, 2)]
    frames = []
    for f in range(14):
        cells = set()
        for col, offset, speed in drops:
            head = (offset + f * speed) % 14
            cells |= {(head - k, col) for k in range(2) if 0 <= head - k < N}
        frames.append(cells)
    return frames


def stack():
    # Rows dropping one at a time, gathering speed as they fall, each landing
    # on the last until the panel is full; then it empties and starts over.
    frames, landed = [], set()
    for floor in range(N - 1, -1, -1):
        drop = sorted({min(floor, n * (n + 1) // 2) for n in range(N)})
        for r in drop:
            frames.append(landed | {(r, c) for c in range(N)})
        landed = landed | {(floor, c) for c in range(N)}
    return frames + [landed]


def bricklayer():
    # Blocks dropped in one at a time, two rows a frame, laying each course
    # left to right before starting the next, until the wall is built.
    frames, landed = [], set()
    for floor in range(5, 0, -1):
        for col in range(1, 6):
            for r in range(floor % 2, floor + 1, 2):
                frames.append(landed | {(r, col)})
            landed = landed | {(floor, col)}
    return frames + [landed, landed]


# ---------------------------------------------------------------------------
# Geometry: loaders that are shapes first
# ---------------------------------------------------------------------------

def orbit():
    # A moon with a short tail circling its planet.
    return [{ROUND[(f - k) % 12] for k in range(3)} | {(3, 3)} for f in range(12)]


def pinwheel():
    # A bar turning about its middle, half a turn per loop.
    return [ray(i * 22.5, -3, 3) for i in range(8)]


def beacon():
    # A lighthouse throwing its beam out to sea on either side.
    tower = {(r, 3) for r in range(3, 7)} | {(6, 2), (6, 4)}
    lamp = {(2, 3)}
    beams = [
        {(2, 4), (2, 5), (2, 6)},
        {(2, 4), (2, 5)},
        {(1, 3), (2, 2), (2, 4)},
        {(2, 2), (2, 1)},
        {(2, 2), (2, 1), (2, 0)},
        {(2, 2), (2, 1)},
        {(1, 3), (2, 2), (2, 4)},
        {(2, 4), (2, 5)},
    ]
    return [tower | lamp | b for b in beams]


def rebound():
    # A ball that hangs at the top, stretches as it drops fast, and squashes
    # on the floor.
    floor = {(6, c) for c in range(1, 6)}
    ball = lambda r: {(r, 3)}
    stretched = lambda r: {(r, 3), (r - 1, 3)}
    squash = {(5, 2), (5, 3), (5, 4)}
    poses = [ball(1), ball(1), ball(2), stretched(3), stretched(5), squash, stretched(3), ball(2)]
    return [floor | pose for pose in poses]


def coil():
    # A square spiral wound into the center and unwound again.
    path = ring_path(2) + ring_path(1) + ring_path(0)
    wound = [set(path[: min(len(path), 4 * (i + 1))]) for i in range(7)]
    unwound = [set(path[4 * i:]) for i in range(1, 7)]
    return wound + unwound


def sandglass():
    # Sand running from the top bulb to the bottom, one grain at a time. A
    # full bottom bulb turned over is the full top bulb, so it loops.
    top = [(2, 3), (2, 2), (2, 4), (1, 3), (1, 2), (1, 4), (1, 1), (1, 5)]
    bottom = [(5, 3), (5, 2), (5, 4), (5, 1), (5, 5), (4, 3), (4, 2), (4, 4)]
    frames = []
    for i in range(len(top) + 1):
        frames.append(set(top[i:]) | set(bottom[:i]) | {(3, 3)})
    return frames


def sweep():
    # A radar arm turning round its scope.
    return [ray(f * 45, 0, 3) for f in range(8)]


def lemniscate():
    # A dot running a figure of eight, trailing two more.
    path = [(3, 3), (2, 4), (2, 5), (3, 6), (4, 5), (4, 4),
            (3, 3), (2, 2), (2, 1), (3, 0), (4, 1), (4, 2)]
    return [{path[(f - k) % 12] for k in range(3)} for f in range(12)]


# ---------------------------------------------------------------------------
# Solids: the five Platonic solids turning in space
# ---------------------------------------------------------------------------

PHI = (1 + 5 ** 0.5) / 2
_SIGNS = (-1, 1)
SOLID_VERTICES = {
    "tetrahedron": [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)],
    "cube": list(itertools.product(_SIGNS, repeat=3)),
    "octahedron": [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)],
    "icosahedron": [p for a in _SIGNS for b in _SIGNS
                    for p in ((0, a, b * PHI), (a, b * PHI, 0), (b * PHI, 0, a))],
    "dodecahedron": list(itertools.product(_SIGNS, repeat=3))
    + [p for a in _SIGNS for b in _SIGNS for p in ((0, a / PHI, b * PHI), (a / PHI, b * PHI, 0), (b * PHI, 0, a / PHI))],
}


def solid(name: str, symmetry: float, wire: bool):
    """A Platonic solid spinning about the vertical, tipped toward the viewer,
    projected flat. A 7x7 grid cannot draw a full wireframe without it
    filling in, so the simpler solids show their vertices and edge midpoints
    (a dotted wireframe) and the icosahedron and dodecahedron their vertices.
    Each loop turns only as far as the solid's own symmetry (`symmetry`
    radians), where it looks as it started, at 11.25 degrees a frame."""
    raw = SOLID_VERTICES[name]
    size = max(math.dist(v, (0, 0, 0)) for v in raw)
    unit = [tuple(x / size for x in v) for v in raw]
    shortest = min(math.dist(a, b) for a, b in itertools.combinations(unit, 2))
    edges = [(a, b) for a, b in itertools.combinations(unit, 2) if math.isclose(math.dist(a, b), shortest)]
    tilt = 0.45 if wire else 0.35

    def turn(v, spin):
        x, y, z = v
        x, z = x * math.cos(spin) + z * math.sin(spin), -x * math.sin(spin) + z * math.cos(spin)
        return x, y * math.cos(tilt) - z * math.sin(tilt)

    def dot(x, y):
        return round(MID - MID * y), round(MID + MID * x)

    steps = round(math.degrees(symmetry) / 11.25)
    frames = []
    for f in range(steps):
        spin = symmetry * f / steps
        cells = {dot(*turn(v, spin)) for v in unit}
        if wire:
            for a, b in edges:
                (ax, ay), (bx, by) = turn(a, spin), turn(b, spin)
                cells.add(dot((ax + bx) / 2, (ay + by) / 2))
        frames.append(cells)
    return frames


_DESIGNS = [
    ("Mycelium", "field", mycelium, "Hyphae branching out from a spore, then the colony hollowing from its old center."),
    ("SporeRing", "field", spore_ring, "Spores thrown off in rings, two rings in flight at once."),
    ("Firefly", "field", firefly, "Fireflies drifting as they glow, never more than two at once."),
    ("Tide", "field", tide, "Water rising and falling, its surface rolling as it goes."),
    ("MassSpec", "field", mass_spec, "A mass spectrum being acquired: peaks and their isotope patterns landing as the scan runs up the m/z axis."),
    ("TestTube", "field", test_tube, "A test tube on the bench, bubbles rising through it and off the rim."),
    ("Fish", "field", fish, "A fish swimming across, its tail beating as it goes."),
    ("Snail", "field", snail, "A snail gliding along, feelers waving, as the ground slides beneath."),
    ("Leaf", "field", leaf, "A leaf falling, swaying side to side and tipping at each turn."),
    ("Ant", "field", ant, "An ant walking on the spot, its legs stepping in alternate tripods."),
    ("Jellyfish", "field", jellyfish, "A jellyfish squeezing its bell to rise, then opening wide and sinking as its tentacles sway."),
    ("Frond", "field", frond, "A fern growing its stem, then opening its leaflets in pairs from the base up."),
    ("Diatom", "field", diatom, "A centric diatom, its striae turning slowly inside the round shell."),
    ("Cladogram", "field", cladogram, "A tree of life drawn from the root up to its tips, then pruned back."),
    ("Helix", "field", helix, "DNA turning, two strands crossing with base pairs where they stand apart."),
    ("Colony", "field", colony, "Colonies landing on a plate, growing, and dying back in the order they came."),
    ("Waggle", "field", waggle, "A honeybee's waggle dance: a shaking run up the middle, then a loop round each side."),
    ("Mitosis", "field", mitosis, "A cell pinching in two and the daughter cells drawing back together."),
    ("Seedling", "field", seedling, "A seed in the soil sending up a shoot that opens its first leaves."),
    ("Chromatogram", "field", chromatogram, "Thin-layer chromatography: spots climbing three lanes at their own retention factors."),
    ("Scatter", "data", scatter, "Points landing one by one along a rising trend."),
    ("Histogram", "data", histogram, "Bins filling left to right into a bell curve, then emptying."),
    ("PieChart", "data", pie_chart, "A pie filling slice by slice from twelve o'clock, then emptying the same way round."),
    ("Heatmap", "data", heatmap, "A hot spot wandering a heat map, dense at its core and speckled at its edge."),
    ("LineChart", "data", line_chart, "A line drawn point to point across a pair of axes."),
    ("Database", "data", database, "A database filling up, disk by disk from the bottom."),
    ("Cart", "everyday", cart, "A shopping cart rolling in, an item dropping into it, and off it goes."),
    ("Upload", "everyday", upload, "Arrows streaming up out of a tray."),
    ("Magnifier", "everyday", magnifier, "A magnifying glass circling as it searches."),
    ("Download", "everyday", download, "Arrows streaming down into a tray."),
    ("Walker", "everyday", walker, "A figure walking on the spot, its legs opening and closing through each stride."),
    ("Runner", "everyday", runner, "A figure running on the spot, leaning in, arms pumping and knees driving high."),
    ("Mail", "everyday", mail, "A letter dropping into its envelope and the flap folding shut."),
    ("Wifi", "everyday", wifi, "A signal finding its bars, arc by arc, then searching again."),
    ("Battery", "everyday", battery, "A battery charging, one cell at a time."),
    ("Truck", "everyday", truck, "A delivery truck on its way, the road markings rushing past."),
    ("Bell", "everyday", bell, "A bell ringing, its clapper swinging to strike each side."),
    ("Heart", "everyday", heart, "A heart beating, lub-dub, then resting before the next beat."),
    ("Chat", "everyday", chat, "A speech bubble with someone typing, three dots rising in turn."),
    ("CloudSync", "everyday", cloud_sync, "A cloud syncing, a ring turning beneath it."),
    ("Lock", "everyday", lock, "A padlock opening, its shackle lifting and swinging free, then locking again."),
    ("Departures", "board", departures, "Three lines of a departure board ticking past at their own pace."),
    ("SplitFlap", "board", split_flap, "A split-flap sign flipping through its glyphs, the flap caught mid-turn."),
    ("Marquee", "board", marquee, "Chase lights running round a theatre sign."),
    ("Scanline", "board", scanline, "A scan bar sweeping down the panel and back up."),
    ("Equalizer", "board", equalizer, "Five level meters, each on its own beat."),
    ("Typewriter", "board", typewriter, "Lines typed out a character at a time before the carriage returns."),
    ("Rain", "board", rain, "Streaks of rain falling at two speeds."),
    ("Stack", "board", stack, "Rows dropping one at a time and stacking up until the panel is full."),
    ("Bricklayer", "board", bricklayer, "Blocks dropped in one at a time, laying each row before the next, until the wall is built."),
    ("Orbit", "geometry", orbit, "A moon with a short tail circling its planet."),
    ("Pinwheel", "geometry", pinwheel, "A bar turning about its middle."),
    ("Beacon", "geometry", beacon, "A lighthouse throwing its beam out to sea on either side."),
    ("Rebound", "geometry", rebound, "A ball that hangs at the top, stretches as it drops, and squashes on the floor."),
    ("Coil", "geometry", coil, "A square spiral wound into the center and unwound again."),
    ("Sandglass", "geometry", sandglass, "Sand running from the top bulb to the bottom, one grain at a time."),
    ("Sweep", "geometry", sweep, "A radar arm turning round its scope."),
    ("Lemniscate", "geometry", lemniscate, "A dot running a figure of eight, trailing two more."),
    ("Tetrahedron", "solids", lambda: solid("tetrahedron", math.pi, True), "A tetrahedron turning, four faces, drawn as a dotted wireframe."),
    ("Cube", "solids", lambda: solid("cube", math.pi / 2, True), "A cube turning, six faces, drawn as a dotted wireframe."),
    ("Octahedron", "solids", lambda: solid("octahedron", math.pi / 2, True), "An octahedron turning, eight faces, drawn as a dotted wireframe."),
    ("Dodecahedron", "solids", lambda: solid("dodecahedron", math.pi, False), "A dodecahedron turning, its twenty vertices wheeling past."),
    ("Icosahedron", "solids", lambda: solid("icosahedron", math.pi, False), "An icosahedron turning, its twelve vertices wheeling past."),
]

# category key -> (title, note), in gallery order.
CATEGORIES = {
    "field": ("Field", "the naturalist set"),
    "data": ("Data", "charts drawing themselves"),
    "everyday": ("Everyday", "the waits people meet in any app"),
    "board": ("Board", "what flip-dot panels do in stations and stadiums"),
    "geometry": ("Geometry", "shapes in motion"),
    "solids": ("Solids", "the five Platonic solids, turning"),
}

PRESETS: dict[str, Preset] = {
    name: Preset(category, blurb, tuple(draw(frame) for frame in build()))
    for name, category, build, blurb in _DESIGNS
}
