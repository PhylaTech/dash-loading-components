"""premium-react-loaders 4.2.0 animates `transform` over inline `transform`.

Three of its loaders set a static `transform` inline (centering, or a
per-element rotation) and then run a keyframe animation on the same property,
which replaces the inline value outright. src/lib/premium-fixes.css restates
the missing piece in each keyframe. These are the invariants those overrides
restore, checked in a browser because the bug only exists once the animation
is running.
"""
import math

import dash
from dash import Dash, html

import dash_loading_components as dlc

dash._dash_renderer._set_react_version("19.2.4")

SIZE = 48
SPEED_MS = 1000


def _app():
    app = Dash(__name__)
    app.layout = html.Div(
        [
            html.Div(dlc.premium.OrbitRings(size=SIZE, color="#f97316", speed=SPEED_MS), id="rings"),
            html.Div(dlc.premium.AtomLoader(size=SIZE, color="#f97316", speed=SPEED_MS), id="atom"),
            html.Div(dlc.premium.MobiusLoader(size=SIZE, color="#f97316", speed=SPEED_MS), id="mobius"),
        ]
    )
    return app


def _matrix(driver, selector, index=0):
    """Computed 2D transform of the n-th match as (a, b, c, d, tx, ty)."""
    raw = driver.execute_script(
        "return getComputedStyle(document.querySelectorAll(arguments[0])[arguments[1]]).transform;",
        selector,
        index,
    )
    assert raw.startswith("matrix("), raw
    return [float(v) for v in raw[len("matrix("):-1].split(",")]


def test_orbit_rings_stay_centred(dash_duo):
    """Each ring is centred by an inline translate(-50%, -50%) that the
    animation used to discard, leaving the rings orbiting the container's
    top-left corner instead of spinning in place."""
    dash_duo.start_server(_app())
    dash_duo.wait_for_element('[data-testid="orbit-rings"]')

    sizes = dash_duo.driver.execute_script(
        """
        return [...document.querySelectorAll('[data-testid="orbit-rings"] .absolute')]
          .map((d) => [d.offsetWidth, d.offsetHeight]);
        """
    )
    assert len(sizes) == 3, sizes
    for index, (width, height) in enumerate(sizes):
        *_, tx, ty = _matrix(dash_duo.driver, '[data-testid="orbit-rings"] .absolute', index)
        assert (tx, ty) == (-width / 2, -height / 2), (index, width, height, tx, ty)


def test_mobius_segments_keep_their_own_angle(dash_duo):
    """Every segment carries its own inline rotation. The upstream keyframe
    rotated by `var(--angle, 90deg)`, a variable the component never sets, so
    all segments snapped to 90deg and the ribbon collapsed into parallel
    dashes."""
    dash_duo.start_server(_app())
    dash_duo.wait_for_element('[data-testid="mobius-loader"]')

    # Run every segment at the same point in its cycle. Upstream staggers them
    # with animation-delay, and a segment still inside its delay shows its
    # inline rotation whether or not the keyframe is fixed.
    matrices = dash_duo.driver.execute_script(
        """
        const segs = [...document.querySelectorAll('[data-testid="mobius-loader"] .absolute')];
        segs.forEach((s) => {
          s.style.animationPlayState = 'paused';
          s.style.animationDelay = `${-0.25 * arguments[0]}ms`;
        });
        return segs.map((s) => getComputedStyle(s).transform);
        """,
        SPEED_MS,
    )
    assert len(matrices) >= 6, matrices

    angles = []
    for raw in matrices:
        assert raw.startswith("matrix("), raw
        a, b = [float(v) for v in raw[len("matrix("):-1].split(",")][:2]
        angles.append(round(math.degrees(math.atan2(b, a))) % 180)

    assert len(set(angles)) > 1, f"every segment rendered at the same angle: {angles}"


def test_atom_electrons_ride_their_orbit(dash_duo):
    """Electrons used to trace a circle of the orbit box's half-height while
    the ring behind them is an ellipse as wide as the loader, so they cut
    across the inside of their own orbit. They must now reach the ellipse's
    long axis, and stay round while doing it."""
    dash_duo.start_server(_app())
    dash_duo.wait_for_element('[data-testid="atom-loader"]')

    # Pause the orbits and seek them by hand. Polling a running animation
    # through the driver samples too coarsely to land on the extremes. Seek
    # through the Web Animations API: each orbit has its own period (upstream
    # adds 150ms per ring), and shifting animation-delay on a running
    # animation lands wherever it had already got to.
    def reach_at(fraction):
        return dash_duo.driver.execute_script(
            """
            const frac = arguments[0];
            document.querySelectorAll('[data-testid="atom-loader"] [style*="atom-orbit"]')
              .forEach((c) => c.getAnimations().forEach((a) => {
                a.pause();
                a.currentTime = frac * a.effect.getTiming().duration;
              }));
            const root = document.querySelector('[data-testid="atom-loader"] .relative');
            const pr = root.getBoundingClientRect();
            return [...root.querySelectorAll('div[style*="background-color"]')]
              .slice(1)  // skip the nucleus
              .map((d) => { const r = d.getBoundingClientRect();
                return [r.left + r.width / 2 - pr.left, r.top + r.height / 2 - pr.top,
                        r.width, r.height]; });
            """,
            fraction,
        )

    # At the start of the cycle every electron sits on the ellipse's short
    # semi-axis; a quarter of the way round it is out on the long one.
    at_start = reach_at(0.0)
    at_quarter = reach_at(0.25)

    def distances(boxes):
        out = []
        for cx, cy, w, h in boxes:
            # A stretched electron would be an oval; its box stays square.
            assert abs(w - h) < 0.5, (w, h)
            out.append(math.hypot(cx - SIZE / 2, cy - SIZE / 2))
        return out

    short_axis = distances(at_start)
    long_axis = distances(at_quarter)
    assert short_axis and long_axis

    # The orbit box is 60% as tall as the loader is wide, so the ring's semi
    # axes are 0.3 * SIZE and 0.5 * SIZE. The old circular path stayed at the
    # short one for the whole cycle.
    for d in short_axis:
        assert abs(d - SIZE * 0.3) < 1.5, d
    for d in long_axis:
        assert abs(d - SIZE * 0.5) < 1.5, d


def test_speed_tokens_are_not_read_as_milliseconds(dash_duo):
    """Upstream resolves its speed tokens to CSS times ("1s") and four
    loaders parseInt that as milliseconds, so the default speed ran them as a
    1ms loop: a blur in the overview, where no speed is passed. The wrappers
    resolve tokens to milliseconds before upstream sees them."""
    app = Dash(__name__)
    app.layout = html.Div(
        [
            dlc.premium.OrbitRings(size=SIZE, id="orbit-rings"),
            dlc.premium.AtomLoader(size=SIZE, id="atom-loader"),
            dlc.premium.MobiusLoader(size=SIZE, id="mobius-loader"),
            dlc.premium.ButtonSpinner(size=SIZE, id="button-spinner"),
            dlc.premium.OrbitRings(size=SIZE, speed="slow", id="slow"),
            dlc.premium.OrbitRings(size=SIZE, speed="fast", id="fast"),
        ]
    )
    dash_duo.start_server(app)
    dash_duo.wait_for_element("#fast [data-testid]")

    def shortest(selector):
        return dash_duo.driver.execute_script(
            """
            return Math.min(...[...document.querySelectorAll(arguments[0])]
              .map((e) => getComputedStyle(e))
              .filter((c) => c.animationName !== 'none')
              .map((c) => parseFloat(c.animationDuration) * 1000));
            """,
            selector,
        )

    for loader in ("orbit-rings", "atom-loader", "mobius-loader", "button-spinner"):
        assert shortest(f"#{loader} *") == 1000, loader
    assert shortest("#slow *") == 2000
    assert shortest("#fast *") == 500
