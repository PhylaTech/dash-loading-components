"""Every dlc component honours the same `rate` and `playing`.

`rate=1.0` must be each spinner's own tempo, what it does with no tempo prop
at all, and `rate=2.0` half that period. The baseline is per spinner for
loading-dev, ldrs and epic (Compass loops in 500ms, Slide in 2400ms), so a
family-wide constant would silently retime most of the catalog; the table in
src/lib/contract.js is checked here against what actually renders.
`playing=False` must stop the motion, whether the family has a pause prop or
not.
"""
import dash
import pytest
from dash import Dash, html

import dash_loading_components as dlc
from dash_loading_components.registry import FAMILIES

dash._dash_renderer._set_react_version("19.2.4")

# The shortest animation under each [data-probe] root, in ms, CSS and SMIL
# alike. Loaders layer several animations (a rotation and a stretch, rings
# with staggered periods, a pulse of fixed length); the shortest is the one
# the tempo prop drives in every family.
SHORTEST_MS = """
const out = {};
document.querySelectorAll('[data-probe]').forEach((root) => {
  let shortest = Infinity;
  const ms = (list) => list.split(',').map((d) => parseFloat(d) * (d.trim().endsWith('ms') ? 1 : 1000)).filter((d) => d > 0);
  root.querySelectorAll('*').forEach((el) => {
    for (const pseudo of [null, '::before', '::after']) {
      shortest = Math.min(shortest, ...ms(getComputedStyle(el, pseudo).animationDuration));
    }
    const dur = el.getAttribute && el.getAttribute('dur');
    if (dur) shortest = Math.min(shortest, parseFloat(dur) * (dur.endsWith('ms') ? 1 : 1000));
  });
  out[root.dataset.probe] = shortest === Infinity ? 0 : shortest;
});
return out;
"""

PLAY_STATE = """
const out = {};
document.querySelectorAll('[data-probe]').forEach((root) => {
  const states = new Set();
  const visit = (el) => {
    for (const pseudo of [null, '::before', '::after']) {
      const c = getComputedStyle(el, pseudo);
      if (c.animationName !== 'none') states.add(c.animationPlayState);
    }
    const c = getComputedStyle(el);
    if (el.parentElement === root && (c.display === 'none' || c.visibility === 'hidden')) states.add('hidden');
    if (el.tagName === 'svg' && el.querySelector('animate, animateTransform')) states.add(el.animationsPaused() ? 'paused' : 'running');
    if (el.shadowRoot) [...el.shadowRoot.querySelectorAll('*')].forEach(visit);
  };
  [...root.querySelectorAll('*')].forEach(visit);
  if (!root.querySelector('*')) states.add('unmounted');
  out[root.dataset.probe] = [...states];
});
return out;
"""

# Tempo is drawn on a canvas by requestAnimationFrame; nothing to measure.
NO_CSS_TEMPO = {"m3"}
# No tempo prop upstream: rate is documented as a no-op here.
NO_TEMPO = {"loader_spinner"}
# Native `speedPlus` is a coarse integer offset, so 2.0 maps to +5, not an exact halving.
COARSE_TEMPO = {"indicators"}


def _all():
    for family, _label, items in FAMILIES:
        for name, component in items:
            yield family, name, component


def _render(dash_duo, probes, script):
    app = Dash(__name__)
    # react-spinners' GridLoader draws random delays; pin them so renders agree.
    app.index_string = app.index_string.replace("<head>", "<head><script>Math.random = () => 0.5</script>", 1)
    app.layout = html.Div([html.Div(node, **{"data-probe": key}) for key, node in probes])
    dash_duo.start_server(app)
    dash_duo.wait_for_element("[data-probe]")
    dash_duo.driver.execute_script("return new Promise((r) => setTimeout(r, 1000));")
    return dash_duo.driver.execute_script(script)


def test_rate_scales_each_spinners_own_tempo(dash_duo):
    probes = []
    for family, name, component in _all():
        if family in NO_CSS_TEMPO | NO_TEMPO:
            continue
        probes += [
            (f"{family}/{name}/default", component(size=48)),
            (f"{family}/{name}/1.0", component(size=48, rate=1.0)),
            (f"{family}/{name}/2.0", component(size=48, rate=2.0)),
        ]
    shortest = _render(dash_duo, probes, SHORTEST_MS)

    wrong = {}
    for family, name, _component in _all():
        if family in NO_CSS_TEMPO | NO_TEMPO:
            continue
        base = shortest[f"{family}/{name}/default"]
        assert base > 0, (family, name)
        normal = shortest[f"{family}/{name}/1.0"]
        double = shortest[f"{family}/{name}/2.0"]
        if abs(normal - base) > 1:
            wrong[f"{family}/{name}"] = f"rate=1.0 gives {normal}ms, upstream runs at {base}ms"
        elif family not in COARSE_TEMPO and abs(double - base / 2) > 1:
            wrong[f"{family}/{name}"] = f"rate=2.0 gives {double}ms, expected {base / 2}ms"
        elif family in COARSE_TEMPO and double >= base:
            wrong[f"{family}/{name}"] = f"rate=2.0 gives {double}ms, no faster than {base}ms"
    assert not wrong, wrong


def test_native_tempo_wins_over_rate(dash_duo):
    shortest = _render(dash_duo, [
        ("arc", dlc.loading_dev.Arc(size=48, rate=2.0, duration=1600)),
        ("ring", dlc.ldrs.Ring(size=48, rate=2.0, speed=4)),
    ], SHORTEST_MS)
    # ldrs Ring's stretch runs at 0.75 of its rotation, so 4s → 3s.
    assert shortest == {"arc": 1600, "ring": 3000}


def test_playing_false_stops_every_spinner(dash_duo):
    probes = []
    for family, name, component in _all():
        if family in NO_CSS_TEMPO:
            continue
        probes += [
            (f"{family}/{name}/on", component(size=48)),
            (f"{family}/{name}/off", component(size=48, playing=False)),
        ]
    states = _render(dash_duo, probes, PLAY_STATE)

    still_running = [
        key for key, found in states.items()
        if key.endswith("/off") and "running" in found
    ]
    assert not still_running, still_running
    # Paused means frozen in place, not gone.
    hidden = [
        key for key, found in states.items()
        if key.endswith("/off") and ("hidden" in found or "unmounted" in found)
    ]
    assert not hidden, hidden
    # SMIL loaders (react-loader-spinner, some indicators) never report a CSS
    # play state, so the control is only that nothing starts out paused.
    paused_at_rest = [
        key for key, found in states.items()
        if key.endswith("/on") and "paused" in found
    ]
    assert not paused_at_rest, paused_at_rest


@pytest.mark.parametrize("family", sorted(NO_CSS_TEMPO))
def test_canvas_families_pass_rate_and_playing_through(family):
    """m3 draws on a canvas, so the contract is checked at the prop level."""
    node = dlc.m3.LoadingIndicator(rate=2.0, playing=False).to_plotly_json()["props"]
    assert node == {"rate": 2.0, "playing": False}
