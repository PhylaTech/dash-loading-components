"""Local gallery explorer for dash-loading-components.

loading.dev-style UX:
  /                      overview — left sticky nav + component cards
  /c/<family>/<Name>     component detail — live preview, controls, snippet

Run:
  source /workspace/dash-loading/.venv/bin/activate
  cd /workspace/dash-loading/dash-loading-components
  REACT_VERSION=19.2.4 python gallery.py
"""
from __future__ import annotations

import os
import re
from typing import Any, Callable, Optional
from urllib.parse import unquote

os.environ.setdefault("REACT_VERSION", "19.2.4")

import dash
from dash import Dash, html, dcc, Input, Output, State, ALL, callback, ctx, no_update

import dash_loading_components as dlc

try:
    dash._dash_renderer._set_react_version("19.2.4")
except Exception as exc:  # pragma: no cover
    print("warn: could not set React version via _set_react_version:", exc)

DEFAULT_COLOR = "#f97316"
DEFAULT_SIZE = 48
ACCENT = "#f97316"

# ---------------------------------------------------------------------------
# Catalog (preserve prior FAMILIES component lists)
# ---------------------------------------------------------------------------

FAMILIES = [
    (
        "loading_dev",
        "loading-dev",
        [
            ("Arc", dlc.loading_dev.Arc),
            ("Atom", dlc.loading_dev.Atom),
            ("Orbit", dlc.loading_dev.Orbit),
            ("Wave", dlc.loading_dev.Wave),
            ("Ring", dlc.loading_dev.Ring),
            ("Pulse", dlc.loading_dev.Pulse),
            ("Cascade", dlc.loading_dev.Cascade),
            ("Comet", dlc.loading_dev.Comet),
            ("Morph", dlc.loading_dev.Morph),
            ("Loading", dlc.loading_dev.Loading),
            ("Blocks", dlc.loading_dev.Blocks),
            ("Clock", dlc.loading_dev.Clock),
            ("Dual", dlc.loading_dev.Dual),
            ("Eclipse", dlc.loading_dev.Eclipse),
            ("Radar", dlc.loading_dev.Radar),
            ("Ripple", dlc.loading_dev.Ripple),
            ("Snake", dlc.loading_dev.Snake),
            ("Swirl", dlc.loading_dev.Swirl),
            ("Trace", dlc.loading_dev.Trace),
            ("Flip", dlc.loading_dev.Flip),
            ("Gather", dlc.loading_dev.Gather),
            ("Leap", dlc.loading_dev.Leap),
            ("Slide", dlc.loading_dev.Slide),
            ("Classic", dlc.loading_dev.Classic),
            ("ClassicV2", dlc.loading_dev.ClassicV2),
            ("Compass", dlc.loading_dev.Compass),
            ("BouncingDots", dlc.loading_dev.BouncingDots),
            ("CircularDots", dlc.loading_dev.CircularDots),
            ("LinearDots", dlc.loading_dev.LinearDots),
        ],
    ),
    (
        "ldrs",
        "ldrs",
        [
            ("Ring", dlc.ldrs.Ring),
            ("Helix", dlc.ldrs.Helix),
            ("DotPulse", dlc.ldrs.DotPulse),
            ("LineSpinner", dlc.ldrs.LineSpinner),
            ("Orbit", dlc.ldrs.Orbit),
            ("Quantum", dlc.ldrs.Quantum),
            ("Jelly", dlc.ldrs.Jelly),
            ("Infinity", dlc.ldrs.Infinity),
            ("Hourglass", dlc.ldrs.Hourglass),
            ("DotWave", dlc.ldrs.DotWave),
            ("Mirage", dlc.ldrs.Mirage),
            ("Ping", dlc.ldrs.Ping),
        ],
    ),
    (
        "spinners",
        "react-spinners",
        [
            ("ClipLoader", dlc.spinners.ClipLoader),
            ("BeatLoader", dlc.spinners.BeatLoader),
            ("HashLoader", dlc.spinners.HashLoader),
            ("SyncLoader", dlc.spinners.SyncLoader),
            ("PropagateLoader", dlc.spinners.PropagateLoader),
            ("PulseLoader", dlc.spinners.PulseLoader),
            ("ScaleLoader", dlc.spinners.ScaleLoader),
            ("MoonLoader", dlc.spinners.MoonLoader),
            ("BarLoader", dlc.spinners.BarLoader),
            ("RingLoader", dlc.spinners.RingLoader),
            ("BounceLoader", dlc.spinners.BounceLoader),
            ("GridLoader", dlc.spinners.GridLoader),
        ],
    ),
    (
        "spinners_react",
        "spinners-react",
        [
            ("SpinnerCircular", dlc.spinners_react.SpinnerCircular),
            ("SpinnerCircularFixed", dlc.spinners_react.SpinnerCircularFixed),
            ("SpinnerCircularSplit", dlc.spinners_react.SpinnerCircularSplit),
            ("SpinnerInfinity", dlc.spinners_react.SpinnerInfinity),
            ("SpinnerDotted", dlc.spinners_react.SpinnerDotted),
            ("SpinnerRound", dlc.spinners_react.SpinnerRound),
            ("SpinnerRoundOutlined", dlc.spinners_react.SpinnerRoundOutlined),
            ("SpinnerRoundFilled", dlc.spinners_react.SpinnerRoundFilled),
            ("SpinnerDiamond", dlc.spinners_react.SpinnerDiamond),
        ],
    ),
    (
        "loader_spinner",
        "react-loader-spinner",
        [
            ("TailSpin", dlc.loader_spinner.TailSpin),
            ("Oval", dlc.loader_spinner.Oval),
            ("ThreeDots", dlc.loader_spinner.ThreeDots),
            ("Rings", dlc.loader_spinner.Rings),
            ("BallTriangle", dlc.loader_spinner.BallTriangle),
            ("Grid", dlc.loader_spinner.Grid),
            ("DNA", dlc.loader_spinner.DNA),
            ("InfinitySpin", dlc.loader_spinner.InfinitySpin),
            ("Circles", dlc.loader_spinner.Circles),
            ("Hourglass", dlc.loader_spinner.Hourglass),
        ],
    ),
    (
        "premium",
        "premium-react-loaders",
        [
            ("SpinnerCircle", dlc.premium.SpinnerCircle),
            ("SpinnerRing", dlc.premium.SpinnerRing),
            ("SpinnerDots", dlc.premium.SpinnerDots),
            ("SpinnerBars", dlc.premium.SpinnerBars),
            ("OrbitDots", dlc.premium.OrbitDots),
            ("OrbitRings", dlc.premium.OrbitRings),
            ("AtomLoader", dlc.premium.AtomLoader),
            ("PulseDots", dlc.premium.PulseDots),
            ("PulseWave", dlc.premium.PulseWave),
            ("BouncingDots", dlc.premium.BouncingDots),
            ("InfinityLoader", dlc.premium.InfinityLoader),
            ("MobiusLoader", dlc.premium.MobiusLoader),
            ("ShimmerBox", dlc.premium.ShimmerBox),
            ("ButtonSpinner", dlc.premium.ButtonSpinner),
            ("SuccessCheckmark", dlc.premium.SuccessCheckmark),
        ],
    ),
    (
        "indicators",
        "react-loading-indicators",
        [
            ("Atom", dlc.indicators.Atom),
            ("BlinkBlur", dlc.indicators.BlinkBlur),
            ("Commet", dlc.indicators.Commet),
            ("FourSquare", dlc.indicators.FourSquare),
            ("LifeLine", dlc.indicators.LifeLine),
            ("Mosaic", dlc.indicators.Mosaic),
            ("OrbitProgress", dlc.indicators.OrbitProgress),
            ("Riple", dlc.indicators.Riple),
            ("Slab", dlc.indicators.Slab),
            ("ThreeDot", dlc.indicators.ThreeDot),
            ("TrophySpin", dlc.indicators.TrophySpin),
        ],
    ),
    (
        "m3",
        "@alerix/m3-loading-indicator",
        [("LoadingIndicator", dlc.m3.LoadingIndicator)],
    ),
    (
        "epic",
        "react-epic-spinners",
        [
            ("AtomSpinner", dlc.epic.AtomSpinner),
            ("OrbitSpinner", dlc.epic.OrbitSpinner),
            ("FlowerSpinner", dlc.epic.FlowerSpinner),
            ("TrinityRingsSpinner", dlc.epic.TrinityRingsSpinner),
            ("HollowDotsSpinner", dlc.epic.HollowDotsSpinner),
            ("SpringSpinner", dlc.epic.SpringSpinner),
            ("SemipolarSpinner", dlc.epic.SemipolarSpinner),
            ("RadarSpinner", dlc.epic.RadarSpinner),
        ],
    ),
]

FAMILY_LOOKUP = {key: (label, items) for key, label, items in FAMILIES}
COMPONENT_LOOKUP = {
    (key, name): component
    for key, _label, items in FAMILIES
    for name, component in items
}

# loading.dev short blurbs (from loading.dev spinner pages)
LOADING_DEV_BLURBS = {
    "Arc": "A single open stroke rotating in a circle.",
    "Atom": "Three rings tumbling inside a circle.",
    "Orbit": "A fading half-arc rotating around a dot.",
    "Wave": "Five bars rising and falling in a wave.",
    "Ring": "An arc rotating in a faint circle.",
    "Pulse": "A ring rippling outward from a dot.",
    "Cascade": "Three nested arcs fanning into a spiral and snapping back in line.",
    "Comet": "A full ring fading into its tail.",
    "Morph": "A square rounding into a circle and back as it turns.",
    "Loading": "The loading.dev mark, its brightest block circling the ring.",
    "Blocks": "Nine blocks shrinking and growing in a sweep across a grid.",
    "Clock": "A clock hand sweeping around a faint face.",
    "Dual": "Two arcs turning in opposite directions.",
    "Eclipse": "Two dots trading places, one passing behind the other.",
    "Ripple": "Three rings spreading out from the center.",
    "Snake": "An arc stretching and shrinking as it circles.",
    "Swirl": "A bright cell chasing its trail around a square.",
    "Trace": "A dash tracing the outline of a rounded square.",
    "Flip": "A square flipping over on one axis, then the other.",
    "Gather": "Four blocks pulling together, turning, and pushing apart.",
    "Leap": "Three dots in a row, the last one leaping to the front.",
    "Slide": "Three dots sliding into the empty corner of a square.",
    "Classic": "Twelve fading bars arranged in a radial pattern.",
    "ClassicV2": "Two lit ticks stepping around a ring of eight.",
    "BouncingDots": "Three staggered dots bouncing up and down.",
    "CircularDots": "Eight dots in a ring, the brightest hopping around.",
    "LinearDots": "Three dots lighting up in turn from left to right.",
}

# From loading-dev d.ts — which wrappers expose easing / cap
LOADING_DEV_EASING = {
    "Arc", "Atom", "Clock", "Comet", "Dual", "Orbit", "Radar", "Ring", "Snake", "Trace"
}
LOADING_DEV_CAP = {"Arc", "Cascade", "Dual", "Ring", "Snake", "Trace"}

SKIP_UI_PROPS = {"id", "style", "setProps"}

# Prop control definitions (kind, default, docs, optional constraints)
PROP_SPECS: dict[str, dict[str, Any]] = {
    "size": {
        "kind": "slider",
        "min": 12,
        "max": 120,
        "step": 1,
        "default": DEFAULT_SIZE,
        "doc": "Width/height in pixels (or size token for some families).",
    },
    "color": {
        "kind": "color",
        "default": DEFAULT_COLOR,
        "doc": "Any CSS color.",
    },
    "duration": {
        "kind": "slider",
        "min": 200,
        "max": 4000,
        "step": 50,
        "default": 1000,
        "doc": "Animation cycle length in milliseconds.",
    },
    "playState": {
        "kind": "dropdown",
        "options": ["running", "paused"],
        "default": "running",
        "doc": "Whether the animation runs.",
    },
    "easing": {
        "kind": "dropdown",
        "options": ["linear", "ease-in-out", "stacked"],
        "default": "linear",
        "doc": "Rotation easing: linear, ease-in-out, or stacked.",
    },
    "cap": {
        "kind": "dropdown",
        "options": ["round", "flat"],
        "default": "round",
        "doc": "Stroke end style: round or flat.",
    },
    "speed": {
        "kind": "slider",
        "min": 0.5,
        "max": 3.0,
        "step": 0.1,
        "default": 1.0,
        "doc": "Animation speed multiplier.",
    },
    "stroke": {
        "kind": "slider",
        "min": 1,
        "max": 12,
        "step": 1,
        "default": 4,
        "doc": "Stroke width.",
    },
    "className": {
        "kind": "text",
        "default": "",
        "doc": "Optional CSS class on the outer wrapper.",
    },
    "speedMultiplier": {
        "kind": "slider",
        "min": 0.2,
        "max": 3.0,
        "step": 0.1,
        "default": 1.0,
        "doc": "Speed multiplier (react-spinners).",
    },
    "margin": {
        "kind": "slider",
        "min": 0,
        "max": 16,
        "step": 1,
        "default": 2,
        "doc": "Margin between spinner elements.",
    },
    "loading": {
        "kind": "bool",
        "default": True,
        "doc": "Whether the spinner is shown.",
    },
    "height": {
        "kind": "slider",
        "min": 12,
        "max": 120,
        "step": 1,
        "default": DEFAULT_SIZE,
        "doc": "Height in pixels.",
    },
    "width": {
        "kind": "slider",
        "min": 12,
        "max": 120,
        "step": 1,
        "default": DEFAULT_SIZE,
        "doc": "Width in pixels.",
    },
    "thickness": {
        "kind": "slider",
        "min": 20,
        "max": 200,
        "step": 5,
        "default": 100,
        "doc": "Stroke thickness (spinners-react).",
    },
    "secondaryColor": {
        "kind": "color",
        "default": "#e2e8f0",
        "doc": "Secondary / track color.",
    },
    "enabled": {
        "kind": "bool",
        "default": True,
        "doc": "Whether the spinner is enabled.",
    },
    "strokeWidth": {
        "kind": "slider",
        "min": 1,
        "max": 12,
        "step": 1,
        "default": 4,
        "doc": "Stroke width.",
    },
    "radius": {
        "kind": "slider",
        "min": 0,
        "max": 20,
        "step": 1,
        "default": 0,
        "doc": "Corner / arc radius.",
    },
    "visible": {
        "kind": "bool",
        "default": True,
        "doc": "Visibility toggle.",
    },
    "ariaLabel": {
        "kind": "text",
        "default": "loading",
        "doc": "Accessible label.",
    },
    "speedPlus": {
        "kind": "slider",
        "min": -5,
        "max": 5,
        "step": 1,
        "default": 0,
        "doc": "Speed adjustment (indicators).",
    },
    "text": {
        "kind": "text",
        "default": "",
        "doc": "Optional label text.",
    },
    "textColor": {
        "kind": "color",
        "default": "#334155",
        "doc": "Label text color.",
    },
    "variant": {
        "kind": "dropdown",
        "options": ["default", "dotted", "disc", "spoke", "bars"],
        "default": "default",
        "doc": "Visual variant (when supported).",
    },
    "paused": {
        "kind": "bool",
        "default": False,
        "doc": "Pause the animation.",
    },
    "contained": {
        "kind": "bool",
        "default": False,
        "doc": "Show Material container track.",
    },
    "containerColor": {
        "kind": "color",
        "default": "#e2e8f0",
        "doc": "Container track color.",
    },
    "sizeRatio": {
        "kind": "slider",
        "min": 0.2,
        "max": 1.0,
        "step": 0.05,
        "default": 1.0,
        "doc": "Inner size relative to container.",
    },
    "animationDuration": {
        "kind": "slider",
        "min": 400,
        "max": 4000,
        "step": 50,
        "default": 1000,
        "doc": "Animation duration in milliseconds.",
    },
}

# Preferred control order per family (props not listed still appear after)
FAMILY_PROP_ORDER = {
    "loading_dev": [
        "size", "color", "duration", "playState", "easing", "cap", "className"
    ],
    "ldrs": ["size", "color", "speed", "stroke", "className"],
    "spinners": [
        "size", "color", "speedMultiplier", "margin", "loading", "height", "width", "className"
    ],
    "spinners_react": [
        "size", "color", "speed", "thickness", "secondaryColor", "enabled", "className"
    ],
    "loader_spinner": [
        "height", "width", "color", "secondaryColor", "strokeWidth", "radius",
        "visible", "ariaLabel", "className",
    ],
    "premium": ["size", "color", "speed", "className"],
    "indicators": [
        "size", "color", "speedPlus", "text", "textColor", "variant", "className"
    ],
    "m3": [
        "size", "color", "speed", "paused", "contained", "containerColor", "sizeRatio", "className"
    ],
    "epic": ["size", "color", "animationDuration", "className"],
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def description_for(family: str, name: str, upstream: str) -> str:
    if family == "loading_dev" and name in LOADING_DEV_BLURBS:
        return LOADING_DEV_BLURBS[name]
    return f"Dash wrapper for upstream `{upstream}` `{name}`."


def card_anchor(family: str, name: str) -> str:
    return f"card-{family}-{name}"


def detail_path(family: str, name: str) -> str:
    return f"/c/{family}/{name}"


def parse_pathname(pathname: Optional[str]) -> tuple[str, Optional[str], Optional[str]]:
    """Return (mode, family, name). mode is 'overview' | 'detail' | 'unknown'."""
    if not pathname or pathname == "/":
        return "overview", None, None
    pathname = unquote(pathname.rstrip("/") or "/")
    m = re.match(r"^/c/([a-z0-9_]+)/([A-Za-z0-9_]+)$", pathname)
    if m:
        family, name = m.group(1), m.group(2)
        if (family, name) in COMPONENT_LOOKUP:
            return "detail", family, name
    return "unknown", None, None


def configurable_props(family: str, name: str, component: Callable) -> list[str]:
    """Return Dash-exposed props that make sense as controls."""
    try:
        available = list(component().available_properties)
    except Exception:
        available = []
    skip = set(SKIP_UI_PROPS)
    props = [p for p in available if p not in skip]

    # loading_dev: only show easing/cap when the wrapper actually exposes them
    if family == "loading_dev":
        if "easing" in props and name not in LOADING_DEV_EASING:
            props = [p for p in props if p != "easing"]
        if "cap" in props and name not in LOADING_DEV_CAP:
            props = [p for p in props if p != "cap"]

    order = FAMILY_PROP_ORDER.get(family, [])
    ordered = [p for p in order if p in props]
    rest = [p for p in props if p not in ordered]
    return ordered + rest


def default_values(family: str, name: str, props: list[str]) -> dict[str, Any]:
    values: dict[str, Any] = {}
    for p in props:
        if family == "indicators" and p == "size":
            values[p] = "medium"
            continue
        if p == "className":
            # omit empty by default — not "set"
            continue
        if p == "text":
            continue
        if p == "ariaLabel":
            continue
        spec = PROP_SPECS.get(p)
        if spec is not None:
            values[p] = spec["default"]
        elif p == "size":
            values[p] = DEFAULT_SIZE
        elif p == "color":
            values[p] = DEFAULT_COLOR
    return values


def format_py_value(v: Any) -> str:
    if isinstance(v, bool):
        return "True" if v else "False"
    if isinstance(v, str):
        return f'"{v}"'
    if isinstance(v, float) and v == int(v):
        return str(int(v))
    return repr(v)


def build_snippet(family: str, name: str, values: dict[str, Any]) -> str:
    parts = []
    for k, v in values.items():
        if v is None:
            continue
        if isinstance(v, str) and v == "" and k in ("className", "text", "ariaLabel"):
            continue
        parts.append(f"{k}={format_py_value(v)}")
    call = f"dlc.{family}.{name}({', '.join(parts)})"
    return f"import dash_loading_components as dlc\n\n{call}\n"


def instantiate(family: str, name: str, values: dict[str, Any]):
    component = COMPONENT_LOOKUP[(family, name)]
    kwargs = {k: v for k, v in values.items() if v is not None}
    # Drop empty optional strings
    for k in list(kwargs):
        if isinstance(kwargs[k], str) and kwargs[k] == "" and k in (
            "className", "text", "ariaLabel"
        ):
            del kwargs[k]
    try:
        return component(**kwargs)
    except Exception as exc:
        return html.Div(f"error: {exc}", style={"color": "crimson", "fontSize": 13})


def overview_preview_kwargs(family: str) -> dict[str, Any]:
    if family == "loader_spinner":
        return {"height": DEFAULT_SIZE, "width": DEFAULT_SIZE, "color": DEFAULT_COLOR}
    if family == "indicators":
        return {"size": "medium", "color": DEFAULT_COLOR}
    if family == "epic":
        return {"size": DEFAULT_SIZE, "color": DEFAULT_COLOR}
    return {"size": DEFAULT_SIZE, "color": DEFAULT_COLOR}


# ---------------------------------------------------------------------------
# Styles
# ---------------------------------------------------------------------------

# Styles live in assets/gallery.css (auto-served by Dash)


# ---------------------------------------------------------------------------
# Layout builders
# ---------------------------------------------------------------------------

def build_site_footer() -> html.Footer:
    """dash-upset-style branding footer (overview + detail)."""
    return html.Footer(
        [
            html.Div(
                [
                    html.Span("Made with ❤️ by "),
                    html.A(
                        "PhylaTech",
                        href="https://github.com/PhylaTech",
                        target="_blank",
                        rel="noopener noreferrer",
                    ),
                    html.Span(" · Powered by "),
                    html.A(
                        "Plotly",
                        href="https://plotly.com",
                        target="_blank",
                        rel="noopener noreferrer",
                    ),
                    html.Span(" · "),
                    html.A(
                        "Source on GitHub",
                        href="https://github.com/PhylaTech/dash-loading-components",
                        target="_blank",
                        rel="noopener noreferrer",
                    ),
                ],
                className="dlc-site-footer-brand",
            ),
            html.P(
                "svg_spinners gated (React ^18.2 peer). Local MVP — not published.",
                className="dlc-footer-note",
            ),
        ],
        className="dlc-site-footer",
    )


def build_sidenav(active_family: Optional[str] = None, active_name: Optional[str] = None) -> html.Aside:
    nav_items: list = [
        html.A(
            [
                html.Span("dlc", className="dlc-brand-mark"),
                html.Span("dash-loading-components", className="sub"),
            ],
            href="/",
            className="dlc-brand",
        ),
        dcc.Link("Overview", href="/", className="dlc-nav-item dlc-nav-home"),
        dcc.Input(
            id="nav-search",
            type="search",
            placeholder="Search…",
            debounce=False,
            className="dlc-nav-search",
            n_submit=0,
        ),
    ]
    for key, label, items in FAMILIES:
        nav_items.append(
            html.Div(
                f"{key} · {label}",
                className="dlc-nav-family",
                id={"type": "nav-family", "family": key},
            )
        )
        for name, _comp in items:
            # Always link to detail pages (same as overview cards), never hash anchors.
            href = detail_path(key, name)
            cls = "dlc-nav-item dlc-nav-comp"
            if key == active_family and name == active_name:
                cls += " dlc-nav-active"
            link_id = {"type": "nav-comp", "family": key, "name": name}
            nav_items.append(
                dcc.Link(name, href=href, className=cls, id=link_id)
            )

    footer = html.Div(
        html.A(
            "GitHub",
            href="https://github.com/PhylaTech/dash-loading-components",
            target="_blank",
            rel="noopener noreferrer",
            className="dlc-nav-github",
        ),
        className="dlc-nav-footer",
    )
    return html.Aside(
        [
            html.Div(nav_items, className="dlc-nav-body"),
            footer,
        ],
        className="dlc-sidenav",
    )


def make_overview_card(family: str, name: str, component: Callable) -> html.Div:
    kwargs = overview_preview_kwargs(family)
    try:
        node = component(**kwargs)
    except Exception as exc:
        node = html.Div("err", title=str(exc), style={"color": "crimson", "fontSize": 11})
    card = html.A(
        [
            html.Div(name, className="name"),
            html.Div(node, className="preview"),
        ],
        href=detail_path(family, name),
        id=card_anchor(family, name),
        className="dlc-card",
        **{"data-family": family, "data-name": name},
    )
    return html.Div(
        card,
        id={"type": "card-wrap", "family": family, "name": name},
        className="dlc-card-wrap",
        **{"data-family": family, "data-name": name},
    )


def build_overview() -> html.Div:
    sections = []
    for key, label, items in FAMILIES:
        sections.append(
            html.Section(
                [
                    html.H2([html.Code(f"dlc.{key}"), html.Span(f"  ·  {label}",
                              style={"fontWeight": 500, "opacity": 0.7, "fontSize": "0.85em"})]),
                    html.P(f"{len(items)} components", className="meta"),
                    html.Div(
                        [make_overview_card(key, n, c) for n, c in items],
                        className="dlc-grid",
                    ),
                ],
                id=f"family-{key}",
                className="dlc-family",
            )
        )
    return html.Div(
        [
            html.Div(
                [
                    html.H1("Loading, made beautiful for Dash."),
                    html.P(
                        "Dash wrappers for modern React loading libraries — loading-dev, ldrs, "
                        "react-spinners, and more. Requires Dash ≥4.5 / React 19."
                    ),
                    html.Pre(
                        "import dash_loading_components as dlc",
                        className="dlc-hero-teaser",
                    ),
                ],
                className="dlc-hero",
            ),
            *sections,
            build_site_footer(),
        ],
        className="dlc-main",
    )


def control_for_prop(prop: str, value: Any, family: str) -> html.Div:
    """Build a single control widget for a prop."""
    # indicators size is special (string tokens)
    if family == "indicators" and prop == "size":
        return html.Div(
            [
                html.H3(prop),
                html.P("Size token (small / medium / large) or number.", className="doc"),
                dcc.Dropdown(
                    id={"type": "prop-ctrl", "prop": prop},
                    options=[
                        {"label": "small", "value": "small"},
                        {"label": "medium", "value": "medium"},
                        {"label": "large", "value": "large"},
                    ],
                    value=value if value in ("small", "medium", "large") else "medium",
                    clearable=False,
                ),
            ],
            className="dlc-prop",
        )

    spec = PROP_SPECS.get(prop)
    if spec is None:
        # fallback text
        return html.Div(
            [
                html.H3(prop),
                html.P("Custom value.", className="doc"),
                dcc.Input(
                    id={"type": "prop-ctrl", "prop": prop},
                    type="text",
                    value="" if value is None else str(value),
                    style={"width": "100%"},
                ),
            ],
            className="dlc-prop",
        )

    kind = spec["kind"]
    doc = spec.get("doc", "")
    kids = [html.H3(prop), html.P(doc, className="doc")]

    if kind == "slider":
        kids.append(
            dcc.Slider(
                id={"type": "prop-ctrl", "prop": prop},
                min=spec["min"],
                max=spec["max"],
                step=spec["step"],
                value=value if value is not None else spec["default"],
                marks=None,
                tooltip={"placement": "bottom", "always_visible": True},
            )
        )
    elif kind == "color":
        kids.append(
            dcc.Input(
                id={"type": "prop-ctrl", "prop": prop},
                type="color",
                value=value or spec["default"],
                style={"width": 56, "height": 36, "padding": 2, "border": "1px solid #e2e8f0",
                       "borderRadius": 8, "background": "#fff"},
            )
        )
    elif kind == "dropdown":
        kids.append(
            dcc.Dropdown(
                id={"type": "prop-ctrl", "prop": prop},
                options=[{"label": o, "value": o} for o in spec["options"]],
                value=value if value in spec["options"] else spec["default"],
                clearable=False,
            )
        )
    elif kind == "bool":
        kids.append(
            dcc.Checklist(
                id={"type": "prop-ctrl", "prop": prop},
                options=[{"label": " enabled", "value": "on"}],
                value=["on"] if (True if value is None else bool(value)) else [],
                style={"fontSize": 13},
            )
        )
    elif kind == "text":
        kids.append(
            dcc.Input(
                id={"type": "prop-ctrl", "prop": prop},
                type="text",
                value="" if value is None else str(value),
                placeholder=prop,
                style={"width": "100%", "padding": "8px 10px", "borderRadius": 8,
                       "border": "1px solid #e2e8f0"},
            )
        )
    else:
        kids.append(html.Div(f"unsupported kind {kind}"))

    return html.Div(kids, className="dlc-prop")


def build_detail(family: str, name: str) -> html.Div:
    upstream = FAMILY_LOOKUP[family][0]
    component = COMPONENT_LOOKUP[(family, name)]
    props = configurable_props(family, name, component)
    values = default_values(family, name, props)
    desc = description_for(family, name, upstream)

    controls = [control_for_prop(p, values.get(p), family) for p in props]
    # Hidden sentinel so ALL pattern always has at least one Input when props empty
    if not controls:
        controls = [
            html.Div(
                dcc.Input(id={"type": "prop-ctrl", "prop": "_none"}, type="hidden", value=""),
                style={"display": "none"},
            )
        ]

    return html.Div(
        [
            dcc.Store(id="detail-meta", data={"family": family, "name": name, "props": props}),
            dcc.Store(id="detail-values", data=values),
            dcc.Link("← Overview", href="/", className="dlc-back"),
            html.H1(name, className="dlc-detail-title"),
            html.P(desc, className="dlc-detail-desc"),
            html.Div(
                [
                    html.Div(
                        [
                            html.Div(
                                instantiate(family, name, values),
                                id="detail-preview",
                                className="dlc-preview-panel",
                            ),
                        ]
                    ),
                    html.Div(
                        [
                            html.Pre(
                                build_snippet(family, name, values),
                                id="detail-snippet",
                                className="dlc-snippet",
                            ),
                            html.Div(controls, id="detail-controls"),
                        ]
                    ),
                ],
                className="dlc-detail-layout",
            ),
            build_site_footer(),
        ],
        className="dlc-main",
    )


def build_404() -> html.Div:
    return html.Div(
        [
            html.H1("Not found"),
            html.P("Unknown route. Try the overview."),
            dcc.Link("Overview", href="/", className="dlc-back"),
            build_site_footer(),
        ],
        className="dlc-main dlc-404",
    )


def page_shell(sidenav, main) -> html.Div:
    return html.Div([sidenav, main], className="dlc-shell")


# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------

app = Dash(__name__, suppress_callback_exceptions=True)
app.title = "dlc gallery"

app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        html.Div(id="page"),
    ]
)


@callback(Output("page", "children"), Input("url", "pathname"))
def render_page(pathname):
    mode, family, name = parse_pathname(pathname)
    if mode == "overview":
        return page_shell(build_sidenav(), build_overview())
    if mode == "detail":
        return page_shell(
            build_sidenav(active_family=family, active_name=name),
            build_detail(family, name),
        )
    return page_shell(build_sidenav(), build_404())


def _coerce_control_value(prop: str, raw: Any, family: str) -> Any:
    if prop == "_none":
        return None
    spec = PROP_SPECS.get(prop)
    if family == "indicators" and prop == "size":
        return raw
    if spec and spec["kind"] == "bool":
        # Checklist returns list
        if isinstance(raw, list):
            return "on" in raw
        return bool(raw)
    if spec and spec["kind"] == "slider":
        if raw is None:
            return spec["default"]
        # keep int when step is int-like
        step = spec.get("step", 1)
        if isinstance(step, int) or (isinstance(step, float) and step == int(step) and step >= 1):
            try:
                return int(raw)
            except (TypeError, ValueError):
                return spec["default"]
        try:
            return float(raw)
        except (TypeError, ValueError):
            return spec["default"]
    if spec and spec["kind"] == "text":
        return "" if raw is None else str(raw)
    return raw


@callback(
    Output({"type": "nav-comp", "family": ALL, "name": ALL}, "style"),
    Output({"type": "nav-family", "family": ALL}, "style"),
    Output({"type": "card-wrap", "family": ALL, "name": ALL}, "style"),
    Input("nav-search", "value"),
    State({"type": "nav-comp", "family": ALL, "name": ALL}, "id"),
    State({"type": "nav-family", "family": ALL}, "id"),
    State({"type": "card-wrap", "family": ALL, "name": ALL}, "id"),
)
def filter_nav_search(query, nav_ids, family_ids, card_ids):
    q = (query or "").strip().lower()
    nav_styles = []
    visible_by_family: dict[str, bool] = {}
    for id_dict in nav_ids or []:
        family = id_dict.get("family", "")
        name = id_dict.get("name", "")
        hay = f"{family} {name}".lower()
        match = (not q) or (q in hay) or (q in name.lower()) or (q in family.lower())
        visible_by_family[family] = visible_by_family.get(family, False) or match
        nav_styles.append({} if match else {"display": "none"})

    family_styles = []
    for id_dict in family_ids or []:
        family = id_dict.get("family", "")
        show = (not q) or visible_by_family.get(family, False)
        family_styles.append({} if show else {"display": "none"})

    card_styles = []
    for id_dict in card_ids or []:
        family = id_dict.get("family", "")
        name = id_dict.get("name", "")
        hay = f"{family} {name}".lower()
        match = (not q) or (q in hay) or (q in name.lower()) or (q in family.lower())
        if match:
            card_styles.append({})
        else:
            card_styles.append({"opacity": "0.22", "pointerEvents": "none", "filter": "grayscale(0.35)"})

    return nav_styles, family_styles, card_styles


@callback(
    Output("detail-preview", "children"),
    Output("detail-snippet", "children"),
    Output("detail-values", "data"),
    Input({"type": "prop-ctrl", "prop": ALL}, "value"),
    State({"type": "prop-ctrl", "prop": ALL}, "id"),
    State("detail-meta", "data"),
    prevent_initial_call=True,
)
def update_detail(values, ids, meta):
    if not meta:
        return no_update, no_update, no_update
    family = meta["family"]
    name = meta["name"]
    props_order = meta.get("props") or []
    collected: dict[str, Any] = {}
    for raw, id_dict in zip(values or [], ids or []):
        prop = id_dict.get("prop")
        if not prop or prop == "_none":
            continue
        collected[prop] = _coerce_control_value(prop, raw, family)
    # Preserve order from props_order for snippet stability
    ordered = {p: collected[p] for p in props_order if p in collected}
    for p, v in collected.items():
        if p not in ordered:
            ordered[p] = v
    preview = instantiate(family, name, ordered)
    snippet = build_snippet(family, name, ordered)
    return preview, snippet, ordered


if __name__ == "__main__":
    print("dlc gallery — http://127.0.0.1:8050/  (REACT_VERSION=%s)" % os.environ.get("REACT_VERSION"))
    app.run(host="0.0.0.0", port=8050, debug=False)
