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


_DESIGNS = [
    ("Mycelium", "field", mycelium, "Hyphae branching out from a spore, then the colony hollowing from its old center."),
    ("SporeRing", "field", spore_ring, "Spores thrown off in rings, two rings in flight at once."),
    ("Firefly", "field", firefly, "Fireflies drifting as they glow, never more than two at once."),
    ("Tide", "field", tide, "Water rising and falling, its surface rolling as it goes."),
    ("MassSpec", "field", mass_spec, "A mass spectrum being acquired: peaks and their isotope patterns landing as the scan runs up the m/z axis."),
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
    ("Cart", "everyday", cart, "A shopping cart rolling in, an item dropping into it, and off it goes."),
    ("Upload", "everyday", upload, "Arrows streaming up out of a tray."),
    ("Magnifier", "everyday", magnifier, "A magnifying glass circling as it searches."),
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
]

# category key -> (title, note), in gallery order.
CATEGORIES = {
    "field": ("Field", "the naturalist set"),
    "data": ("Data", "charts drawing themselves"),
    "everyday": ("Everyday", "carts, uploads and searches"),
    "board": ("Board", "what flip-dot panels do in stations and stadiums"),
    "geometry": ("Geometry", "shapes in motion"),
}

PRESETS: dict[str, Preset] = {
    name: Preset(category, blurb, tuple(draw(frame) for frame in build()))
    for name, category, build, blurb in _DESIGNS
}
