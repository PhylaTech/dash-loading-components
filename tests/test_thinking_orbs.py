"""Tests for the thinking_orbs family wrap.

Checks: prop passthrough, the registry holding exactly the nine states,
namespace exports, and in a real browser that every state paints a canvas
(the component must survive webpack's tree shaking), that `size` picks the
nearest of upstream's three designs and scales to the requested pixels, that
`color` tints the ink, and that `theme="auto"` follows Mantine's colour scheme.
"""
from __future__ import annotations

import time

import pytest
import dash
from dash import Dash, html

import dash_loading_components as dlc

dash._dash_renderer._set_react_version("19.2.4")
from dash_loading_components import thinking_orbs
from dash_loading_components.registry import list_libraries, list_spinners

STATES = [
    "working", "searching", "solving", "listening", "connecting",
    "weaving", "composing", "breathing", "shaping",
]

OPTIONS = {
    "state": "searching",
    "size": 20,
    "theme": "dark",
    "speed": 1.25,
    "paused": True,
    "color": "#123456",
    "dots": 1.5,
    "dot_size": 0.7,
    "aria_label": "Searching",
    "rate": 2.0,
    "playing": False,
}


class TestProps:
    def test_all_options_recorded(self):
        node = dlc.thinking_orbs.Orb(**OPTIONS).to_plotly_json()["props"]
        for prop, value in OPTIONS.items():
            assert node[prop] == value, f"{prop}: expected {value!r}, got {node.get(prop)!r}"

    def test_available_properties_cover_the_api(self):
        available = set(dlc.thinking_orbs.Orb().available_properties)
        assert not set(OPTIONS) - available

    def test_defaults_unset(self):
        node = dlc.thinking_orbs.Orb().to_plotly_json()["props"]
        assert node == {}


class TestRegistry:
    def test_in_libraries(self):
        assert "thinking_orbs" in list_libraries()

    def test_exactly_the_nine_states(self):
        assert list_spinners("thinking_orbs") == STATES
        assert thinking_orbs.ORB_STATES == STATES

    def test_registry_builds_the_state(self):
        from dash_loading_components.registry import COMPONENT_LOOKUP
        node = COMPONENT_LOOKUP[("thinking_orbs", "solving")](size=20).to_plotly_json()["props"]
        assert node == {"state": "solving", "size": 20}

    def test_no_flat_export(self):
        assert not hasattr(dlc, "Orb")
        assert callable(dlc.ThinkingOrbsOrb)


PROBE = """
const out = {};
document.querySelectorAll('[data-probe]').forEach((root) => {
    const c = root.querySelector('canvas');
    if (!c) { out[root.dataset.probe] = {canvas: false}; return; }
    const data = c.getContext('2d').getImageData(0, 0, c.width, c.height).data;
    let ink = 0, sum = 0, tinted = 0;
    for (let i = 0; i < data.length; i += 4) {
        if (data[i + 3] < 128) continue;
        ink++;
        sum += (data[i] + data[i + 1] + data[i + 2]) / 3;
        if (Math.abs(data[i] - data[i + 2]) > 20) tinted++;
    }
    const r = c.getBoundingClientRect();
    out[root.dataset.probe] = {
        canvas: true, width: c.width, height: c.height, ink, tinted,
        mean: ink ? sum / ink : null, cssWidth: r.width, cssHeight: r.height,
        label: c.getAttribute('aria-label'), role: c.getAttribute('role'),
    };
});
return out;
"""


def _start(dash_duo, probes, wait_ms=1000):
    app = Dash(__name__)
    app.layout = html.Div([html.Div(node, **{"data-probe": key}) for key, node in probes])
    dash_duo.start_server(app)
    dash_duo.wait_for_element("[data-probe] canvas")
    dash_duo.driver.execute_script(f"return new Promise((r) => setTimeout(r, {wait_ms}));")
    return app


def test_every_state_paints_a_canvas(dash_duo):
    """A bare import of thinking-orbs can be tree-shaken away; the canvases must paint."""
    _start(dash_duo, [(s, dlc.thinking_orbs.Orb(state=s)) for s in STATES])
    found = dash_duo.driver.execute_script(PROBE)
    for state in STATES:
        info = found[state]
        assert info["canvas"], f"{state}: no canvas"
        assert info["ink"] > 0, f"{state}: blank canvas"
        assert info["role"] == "img"
    assert found["breathing"]["label"] == "Thinking…"
    assert dash_duo.get_logs() == []


def test_size_picks_the_nearest_design_and_scales_to_the_request(dash_duo):
    """Upstream throws on a size other than 64, 32 or 20, so every pixel size
    snaps to the nearest design (in log space) and is scaled to what was asked."""
    sizes = {"s12": 12, "s20": 20, "s24": 24, "s28": 28, "s48": 48, "s64": 64, "s96": 96, "s256": 256}
    _start(dash_duo, [(k, dlc.thinking_orbs.Orb(state="working", size=v)) for k, v in sizes.items()])
    found = dash_duo.driver.execute_script(PROBE)
    dpr = dash_duo.driver.execute_script("return Math.min(2, devicePixelRatio || 1)")
    design = {"s12": 20, "s20": 20, "s24": 20, "s28": 32, "s48": 64, "s64": 64, "s96": 64, "s256": 64}
    for key, px in sizes.items():
        info = found[key]
        assert info["width"] == round(design[key] * dpr), (key, info)
        assert (info["cssWidth"], info["cssHeight"]) == (px, px), (key, info)
        assert info["ink"] > 0, key
    assert dash_duo.get_logs() == []


def test_default_size_is_the_64_design(dash_duo):
    _start(dash_duo, [("d", dlc.thinking_orbs.Orb())])
    info = dash_duo.driver.execute_script(PROBE)["d"]
    assert (info["cssWidth"], info["cssHeight"]) == (64, 64)


def test_color_tints_the_ink(dash_duo):
    """Upstream's stock ink is grey; `color` tints it (hex or rgb() only)."""
    _start(dash_duo, [
        ("stock", dlc.thinking_orbs.Orb(state="searching", theme="dark")),
        ("hex", dlc.thinking_orbs.Orb(state="searching", theme="dark", color="#f97316")),
        ("rgb", dlc.thinking_orbs.Orb(state="searching", theme="dark", color="rgb(249, 115, 22)")),
        ("named", dlc.thinking_orbs.Orb(state="searching", theme="dark", color="orange")),
        ("empty", dlc.thinking_orbs.Orb(state="searching", theme="dark", color="")),
    ])
    found = dash_duo.driver.execute_script(PROBE)
    assert found["stock"]["tinted"] == 0
    assert found["hex"]["tinted"] > 0
    assert found["rgb"]["tinted"] > 0
    # Upstream ignores any other CSS colour syntax, and an empty string means unset.
    assert found["named"]["tinted"] == 0
    assert found["empty"]["tinted"] == 0


SET_SCHEME = """
const [scheme, done] = [arguments[0], arguments[arguments.length - 1]];
if (scheme) document.documentElement.setAttribute('data-mantine-color-scheme', scheme);
else document.documentElement.removeAttribute('data-mantine-color-scheme');
setTimeout(() => done(), 300);
"""


def test_auto_theme_follows_the_mantine_color_scheme(dash_duo):
    """Upstream's auto theme reads data-theme or a dark/light class, which
    Mantine never sets. The wrapper mirrors data-mantine-color-scheme, live."""
    _start(dash_duo, [
        ("auto", dlc.thinking_orbs.Orb(state="searching")),
        ("pinned", dlc.thinking_orbs.Orb(state="searching", theme="light")),
    ])
    driver = dash_duo.driver
    driver.set_script_timeout(10)
    inks = {}
    for scheme in ("dark", "light"):
        driver.execute_async_script(SET_SCHEME, scheme)
        found = driver.execute_script(PROBE)
        inks[scheme] = found["auto"]["mean"]
        # A pinned theme ignores the page.
        assert found["pinned"]["mean"] < 128, found["pinned"]
    # Dark pages get light ink and light pages dark ink.
    assert inks["dark"] > 150, inks
    assert inks["light"] < 128, inks
    assert dash_duo.get_logs() == []


SNAPSHOT = "return Object.fromEntries([...document.querySelectorAll('[data-probe] canvas')].map((c) => [c.parentElement.parentElement.dataset.probe, c.toDataURL()]));"


def test_playing_false_freezes_the_frame(dash_duo):
    """A playing orb animates between two looks; a paused one holds its frame."""
    _start(dash_duo, [
        ("playing", dlc.thinking_orbs.Orb(state="working")),
        ("paused", dlc.thinking_orbs.Orb(state="working", playing=False)),
        ("native", dlc.thinking_orbs.Orb(state="working", playing=False, paused=False)),
    ])
    driver = dash_duo.driver
    first = driver.execute_script(SNAPSHOT)
    driver.execute_script("return new Promise((r) => setTimeout(r, 400));")
    second = driver.execute_script(SNAPSHOT)
    assert first["playing"] != second["playing"]
    assert first["paused"] == second["paused"]
    # An explicit native `paused` wins over `playing`.
    assert first["native"] != second["native"]


class TestGalleryControls:
    """The detail page offers only controls that act, and starts at upstream's look."""

    EXPECTED = ["size", "color", "rate", "playing", "theme", "dots", "dot_size", "aria_label", "className"]

    def _page(self, name="working"):
        import gallery
        props = gallery.configurable_props("thinking_orbs", name, gallery.COMPONENT_LOOKUP[("thinking_orbs", name)])
        return gallery, props, gallery.default_values("thinking_orbs", name, props)

    def test_controls_are_the_live_props(self):
        _gallery, props, _values = self._page()
        assert props == self.EXPECTED

    def test_defaults_match_the_bare_component(self):
        """64 is the design upstream draws with no size, and the ink stays
        stock grey: the gallery accent must not be always-sent."""
        gallery, _props, values = self._page()
        sent = gallery.sent_values("thinking_orbs", "working", values)
        assert sent == {"size": 64}
        snippet = gallery.build_snippet("thinking_orbs", "working", sent)
        assert 'dlc.thinking_orbs.Orb(state="working", size=64)' in snippet

    def test_changed_controls_reach_the_snippet(self):
        gallery, _props, values = self._page("solving")
        sent = gallery.sent_values("thinking_orbs", "solving", {
            **values, "color": "#f97316", "theme": "light", "dots": 1.5, "dot_size": 0.7, "rate": 2.0,
        })
        snippet = gallery.build_snippet("thinking_orbs", "solving", sent)
        for part in ('color="#f97316"', 'theme="light"', "dots=1.5", "dot_size=0.7", "rate=2.0"):
            assert part in snippet, snippet

    def test_every_state_has_a_blurb_and_a_route(self):
        import gallery
        for state in STATES:
            assert gallery.THINKING_ORBS_BLURBS[state] == gallery.description_for("thinking_orbs", state, "thinking-orbs")
            assert gallery.parse_pathname(f"/c/thinking_orbs/{state}") == ("detail", "thinking_orbs", state)

    def test_no_orb_in_the_header_brand_mark(self):
        import gallery
        assert all(skip in gallery.MARK_SKIP for skip in (("thinking_orbs", s) for s in STATES))


def test_gallery_detail_and_search(dash_duo):
    from dash.testing.application_runners import import_app
    from selenium.webdriver.common.keys import Keys

    dash_duo.start_server(import_app("gallery"))
    driver = dash_duo.driver
    driver.set_window_size(1440, 1200)
    driver.get(dash_duo.server_url + "/c/thinking_orbs/weaving")
    dash_duo.wait_for_element("#detail-preview canvas")
    dash_duo.wait_for_contains_text("#detail-snippet", "dlc.thinking_orbs.Orb")
    labels = driver.execute_script("return document.querySelector('#detail-controls').textContent")
    for title in ("Size", "Color", "Rate", "Playing", "Theme", "Dots", "Dot size"):
        assert title in labels, title
    assert "Hue" not in labels
    # The empty field shows upstream's own label, not a generic one.
    assert driver.execute_script(
        "return [...document.querySelectorAll('#detail-controls input')].some((i) => i.placeholder === 'Weaving…')")

    # Search: both libraries have a "weaving"; the orb's row shows the family icon.
    driver.get(dash_duo.server_url + "/")
    dash_duo.wait_for_element("#site-search")
    dash_duo.find_element("#site-search").send_keys("weaving")
    for _ in range(40):
        rows = driver.find_elements("css selector", ".dlc-search-option")
        if len(rows) == 2:
            break
        time.sleep(0.1)
    assert [r.find_element("css selector", ".dlc-search-group").text for r in rows] == ["dlc.loadersz", "dlc.thinking_orbs"]
    for _ in range(40):
        icon = driver.execute_script(
            "return !!document.querySelector('.dlc-search-option[href=\"/c/thinking_orbs/weaving\"] .dlc-search-preview .dlc-icon-thinking_orbs')")
        if icon:
            break
        time.sleep(0.1)
    assert icon
    # The icon file exists and the rule that paints it is in place.
    assert "icons/thinking_orbs.svg" in driver.execute_script(
        "return getComputedStyle(document.querySelector('.dlc-icon-thinking_orbs')).getPropertyValue('--dlc-icon')")
    dash_duo.find_element("#site-search").send_keys(Keys.ARROW_DOWN, Keys.ENTER)
    dash_duo.wait_for_text_to_equal("h1", "weaving")
    assert driver.current_url.endswith("/c/thinking_orbs/weaving")
    assert dash_duo.get_logs() == []
