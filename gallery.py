"""Gallery for dash-loading-components.

  /                      overview: every family, one card per spinner
  /c/<family>/<Name>     component page: live demo, controls, snippets, props
  /credits               upstream packages and their licenses

Run locally with `pixi run gallery`. Deployed behind gunicorn as
`gallery:server` (see the Dockerfile).
"""
from __future__ import annotations

import json
import logging
import os
import re
from typing import Any, Callable, Optional
from urllib.parse import unquote

os.environ.setdefault("REACT_VERSION", "19.2.4")

import dash
import dash_mantine_components as dmc
from dash import ALL, MATCH, Dash, Input, Output, State, callback, clientside_callback, dcc, html, no_update

import dash_loading_components as dlc
from dash_loading_components.registry import COMPONENT_LOOKUP, FAMILIES, FAMILY_LOOKUP

try:
    import black
except ImportError:  # pragma: no cover - deployment installs Black in the venv
    black = None

logger = logging.getLogger(__name__)

try:
    dash._dash_renderer._set_react_version("19.2.4")
except Exception as exc:  # pragma: no cover
    print("warn: could not set React version via _set_react_version:", exc)

REPO_URL = "https://github.com/PhylaTech/dash-loading-components"
SITE_URL = "https://dash-loading-components.phylatech.com"

DEFAULT_COLOR = "#f97316"
DEFAULT_SIZE = 48

# Size presets for the workbench (px), loading.dev-style Small / Medium / Large
SIZE_PRESETS = [("Small", 24), ("Medium", 48), ("Large", 96)]
SIZE_PRESET_VALUES = {v for _, v in SIZE_PRESETS}
SIZE_PRESET_DEFAULT = 48

# Workbench control order (props not listed follow in family order)
WORKBENCH_PROP_PRIORITY = [
    "size", "height", "width", "color", "rate", "playing",
    "easing", "cap", "sweep", "direction", "origin",
    "thickness", "stroke", "stroke_width", "stroke_width_secondary",
    "stroke_length", "bg_opacity", "secondary_color", "margin",
    "play_state", "paused", "loading", "enabled", "visible", "still",
    "reverse", "dense", "variant", "contained",
    "container_color", "size_ratio", "radius", "bar_count", "dot_count",
    "dot_size", "ring_count", "ring_gap", "alternate", "orbit_radius", "stagger",
    "text", "text_color", "aria_label", "className",
]

PROP_SECTION_TITLES = {
    "size": "Size",
    "height": "Height",
    "width": "Width",
    "color": "Color",
    "rate": "Rate",
    "playing": "Playing",
    "easing": "Easing",
    "cap": "Cap",
    "play_state": "State",
    "thickness": "Thickness",
    "stroke": "Stroke",
    "stroke_width": "Stroke width",
    "secondary_color": "Secondary color",
    "margin": "Margin",
    "loading": "Loading",
    "enabled": "Enabled",
    "visible": "Visible",
    "paused": "Paused",
    "variant": "Variant",
    "contained": "Contained",
    "container_color": "Container color",
    "size_ratio": "Size ratio",
    "radius": "Radius",
    "text": "Text",
    "text_color": "Text color",
    "aria_label": "aria-label",
    "className": "Custom classes",
    "sweep": "Sweep",
    "direction": "Direction",
    "origin": "Origin",
    "animation_duration": "Animation duration",
    "still": "Still",
    "reverse": "Reverse",
    "ring_count": "Ring count",
    "ring_gap": "Ring gap",
    "alternate": "Alternate",
    "orbit_radius": "Orbit radius",
    "stagger": "Stagger",
    "dense": "Dense",
    "bg_opacity": "Track opacity",
    "stroke_length": "Stroke length",
    "stroke_width_secondary": "Secondary stroke",
    "bar_count": "Bar count",
    "dot_count": "Dot count",
    "dot_size": "Dot size",
}

PROP_SECTION_COPY = {
    "size": "The spinner’s dimensions in pixels. The presets are Small (24), Medium (48) and Large (96). Every dlc component takes it.",
    "height": "Height in pixels, for loaders that size their height separately from their width.",
    "width": "Width in pixels, for loaders that size their width separately from their height.",
    "color": "Any valid CSS color. Every dlc component takes it.",
    "rate": (
        "Relative tempo: 1.0 is this spinner’s own tempo, the one it runs at "
        "upstream with no tempo prop set; 2.0 is twice as fast. Every dlc "
        "component takes it, whatever unit its library uses underneath."
    ),
    "playing": "False freezes the animation where it is. Every dlc component takes it.",
    "easing": "How the motion accelerates through each cycle.",
    "cap": "How the ends of the stroke are drawn: round finishes them with a half circle, flat cuts them square.",
    "play_state": "Pauses or resumes the animation.",
    "thickness": "Stroke thickness.",
    "stroke": "Stroke width in pixels.",
    "stroke_width": "Stroke width in pixels.",
    "secondary_color": "Color of the track, or of the second tone on loaders that use two. Empty keeps the spinner’s own.",
    "margin": "Spacing between the spinner’s elements, in pixels.",
    "loading": "Whether the spinner renders.",
    "enabled": "Whether the spinner renders.",
    "visible": "Whether the spinner renders.",
    "variant": "Visual variant.",
    "contained": "Draws the Material container behind the indicator.",
    "container_color": "Color of the Material container. Empty keeps the spinner’s own.",
    "size_ratio": "Size of the indicator relative to its container.",
    "radius": "Corner or arc radius.",
    "text": "Optional label rendered with the indicator.",
    "text_color": "Color of the label. Empty keeps the spinner’s own.",
    "aria_label": "Accessible name announced to assistive technology.",
    "className": (
        "Extra classes for tweaking the spinner in ways the library does not "
        "provide. On loading_dev wrappers they land on the spinner root, as in "
        "loading.dev."
    ),
    "sweep": (
        "Which way the sweep runs: diagonal from the top left corner to the "
        "bottom right, rows from top to bottom, columns from left to right."
    ),
    "direction": "Which way the motion travels: out spreads from the center, in draws into it.",
    "origin": "Where the spinner grows from: center scales from the middle, bottom rises from the baseline.",
    "animation_duration": "Length of one loop in seconds.",
    "reverse": "Runs the animation backwards.",
    "dense": "A bolder, more compact OrbitProgress.",
    "bg_opacity": "Opacity of the track behind the stroke, from 0 to 1.",
    "stroke_length": "Fraction of the path that is stroked, from 0 to 1.",
    "stroke_width_secondary": "Stroke width of the background circle.",
    "bar_count": "Number of bars.",
    "dot_count": "Number of dots.",
    "dot_size": "Diameter of each dot in pixels.",
    "ring_count": "Number of concentric rings. Rings that would not fit inside the size are dropped.",
    "ring_gap": "Gap between rings in pixels.",
    "alternate": "Turns every other ring the opposite way.",
    "orbit_radius": "Radius of the orbit relative to the size.",
    "stagger": "Offsets each dot’s pulse from the last.",
}

# Upstream tempo and pause props, replaced on the page by the contract's
# `rate` and `playing` (src/lib/contract.js translates them back).
NATIVE_TEMPO_PROPS = frozenset({"duration", "speed", "speed_multiplier", "speed_plus", "animation_duration"})
NATIVE_PLAY_PROPS = frozenset({"play_state", "paused", "still"})
# react-loader-spinner has no tempo prop at all, so rate does nothing there.
RATELESS_FAMILIES = frozenset({"loader_spinner"})

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

# From loading-dev d.ts: which wrappers expose easing / cap
LOADING_DEV_EASING = {
    "Arc", "Atom", "Clock", "Comet", "Dual", "Orbit", "Radar", "Ring", "Snake", "Trace"
}
LOADING_DEV_CAP = {"Arc", "Cascade", "Dual", "Ring", "Snake", "Trace"}

SKIP_UI_PROPS = {"id", "style", "setProps"}

# Control definitions. `default` is what the control starts at; per-spinner
# corrections live in UPSTREAM_DEFAULTS. A color default of "" means "leave
# it to the spinner": the field starts empty and nothing is sent.
PROP_SPECS: dict[str, dict[str, Any]] = {
    "size": {"kind": "slider", "min": 12, "max": 120, "step": 1, "default": DEFAULT_SIZE},
    "color": {"kind": "color", "default": DEFAULT_COLOR},
    "playing": {"kind": "bool", "default": True},
    "easing": {"kind": "enum", "options": ["linear", "ease-in-out", "stacked"],
               "labels": {"linear": "Linear", "ease-in-out": "Eased", "stacked": "Stacked"},
               "default": "linear"},
    "cap": {"kind": "enum", "options": ["round", "flat"],
            "labels": {"round": "Round", "flat": "Flat"}, "default": "round"},
    "stroke": {"kind": "slider", "min": 1, "max": 12, "step": 1, "default": 4},
    "className": {"kind": "text", "default": "", "placeholder": "e.g. opacity-40"},
    "sweep": {"kind": "enum", "options": ["diagonal", "rows", "columns"],
              "labels": {"diagonal": "Diagonal", "rows": "Rows", "columns": "Columns"},
              "default": "diagonal"},
    "direction": {"kind": "enum", "options": ["out", "in"],
                  "labels": {"out": "Out", "in": "In"}, "default": "out"},
    "origin": {"kind": "enum", "options": ["center", "bottom"],
               "labels": {"center": "Center", "bottom": "Bottom"}, "default": "center"},
    "margin": {"kind": "slider", "min": 0, "max": 16, "step": 1, "default": 2},
    "loading": {"kind": "bool", "default": True},
    "height": {"kind": "slider", "min": 2, "max": 120, "step": 1, "default": DEFAULT_SIZE},
    "width": {"kind": "slider", "min": 2, "max": 160, "step": 1, "default": DEFAULT_SIZE},
    "thickness": {"kind": "slider", "min": 20, "max": 200, "step": 5, "default": 100},
    "secondary_color": {"kind": "color", "default": ""},
    "enabled": {"kind": "bool", "default": True},
    "stroke_width": {"kind": "slider", "min": 1, "max": 12, "step": 1, "default": 4},
    "radius": {"kind": "slider", "min": 0, "max": 20, "step": 0.5, "default": 0},
    "visible": {"kind": "bool", "default": True},
    "aria_label": {"kind": "text", "default": "", "placeholder": "loading"},
    "text": {"kind": "text", "default": "", "placeholder": "Loading…"},
    "text_color": {"kind": "color", "default": ""},
    "variant": {"kind": "dropdown", "options": ["default", "dotted", "disc", "spoke", "bars"],
                "default": "default"},
    "paused": {"kind": "bool", "default": False},
    "contained": {"kind": "bool", "default": False},
    "container_color": {"kind": "color", "default": ""},
    "size_ratio": {"kind": "slider", "min": 0.2, "max": 1.0, "step": 0.05, "default": 1.0},
    "animation_duration": {"kind": "slider", "min": 0.2, "max": 3.0, "step": 0.1, "default": 1.0},
    "still": {"kind": "bool", "default": False},
    "reverse": {"kind": "bool", "default": False},
    "dense": {"kind": "bool", "default": False},
    "bg_opacity": {"kind": "slider", "min": 0.0, "max": 1.0, "step": 0.05, "default": 0.1},
    "stroke_length": {"kind": "slider", "min": 0.05, "max": 1.0, "step": 0.05, "default": 0.15},
    "stroke_width_secondary": {"kind": "slider", "min": 1, "max": 12, "step": 1, "default": 2},
    "bar_count": {"kind": "slider", "min": 2, "max": 12, "step": 1, "default": 5},
    "dot_count": {"kind": "slider", "min": 2, "max": 12, "step": 1, "default": 3},
    "dot_size": {"kind": "slider", "min": 2, "max": 24, "step": 1, "default": 8},
    "ring_count": {"kind": "slider", "min": 1, "max": 8, "step": 1, "default": 3},
    "ring_gap": {"kind": "slider", "min": 0, "max": 24, "step": 1, "default": 6},
    "alternate": {"kind": "bool", "default": True},
    "orbit_radius": {"kind": "slider", "min": 0.2, "max": 1.0, "step": 0.05, "default": 0.5},
    "stagger": {"kind": "bool", "default": True},
}

RATE_SPEC: dict[str, Any] = {"kind": "slider", "min": 0.5, "max": 3.0, "step": 0.1, "default": 1.0}

# react-loading-indicators gives each spinner its own curve, several of them
# cubic-beziers, so the control starts empty ("Default") rather than naming
# one that would be wrong for most of the family.
INDICATORS_EASING_SPEC: dict[str, Any] = {
    "kind": "dropdown",
    "options": ["linear", "ease-in", "ease-out", "ease-in-out"],
    "default": None,
}

INDICATORS_VARIANT = {
    "OrbitProgress": {
        "kind": "dropdown",
        "options": ["disc", "dotted", "spokes", "split-disc", "track-disc"],
        "default": "disc",
    },
    "ThreeDot": {
        "kind": "dropdown",
        "options": ["pulsate", "bob", "brick-stack", "bounce"],
        "default": "pulsate",
    },
}

PREMIUM_THICKNESS_SPEC = {"kind": "slider", "min": 1, "max": 12, "step": 1, "default": 2}


def prop_spec(family: str, prop: str, name: str | None = None) -> dict[str, Any] | None:
    """Resolve control metadata for one prop of one spinner."""
    if prop == "rate":
        return RATE_SPEC
    if prop == "easing" and family == "indicators":
        return INDICATORS_EASING_SPEC
    if prop == "variant" and family == "indicators" and name in INDICATORS_VARIANT:
        return INDICATORS_VARIANT[name]
    if prop == "thickness" and family == "premium":
        return PREMIUM_THICKNESS_SPEC
    return PROP_SPECS.get(prop)


def _for(family: str, names: str, value: Any) -> dict[tuple[str, str], Any]:
    return {(family, name): value for name in names.split()}


# The wrappers share one prop list per family, but a spinner does not always
# use all of it: react-spinners' ClipLoader has no margin, most ldrs loaders
# draw no stroke. A control for a prop the spinner ignores would do nothing,
# so the gallery leaves it out. tests/test_gallery_controls.py checks that
# every control left in changes what renders.
IGNORED_PROPS: dict[tuple[str, str], frozenset[str]] = {
    **_for("ldrs", "Helix DotPulse Orbit Quantum Jelly Hourglass DotWave Mirage Ping",
           frozenset({"stroke"})),
    **_for("spinners", "ClipLoader HashLoader PropagateLoader MoonLoader RingLoader BounceLoader",
           frozenset({"margin", "height", "width"})),
    **_for("spinners", "BeatLoader SyncLoader PulseLoader GridLoader",
           frozenset({"height", "width"})),
    **_for("spinners", "ScaleLoader", frozenset({"size"})),
    **_for("spinners", "BarLoader", frozenset({"size", "margin"})),
    **_for("spinners_react", "SpinnerDotted SpinnerRound SpinnerRoundOutlined SpinnerRoundFilled",
           frozenset({"secondary_color"})),
    **_for("loader_spinner", "TailSpin", frozenset({"secondary_color"})),
    **_for("loader_spinner", "Oval", frozenset({"radius"})),
    **_for("loader_spinner", "Rings BallTriangle Grid",
           frozenset({"secondary_color", "stroke_width"})),
    **_for("loader_spinner", "ThreeDots Circles",
           frozenset({"secondary_color", "stroke_width", "radius"})),
    # Fixed palettes of their own, so color does nothing either.
    **_for("loader_spinner", "DNA Hourglass",
           frozenset({"color", "secondary_color", "stroke_width", "radius"})),
    **_for("loader_spinner", "InfinitySpin",
           frozenset({"height", "secondary_color", "stroke_width", "radius", "visible"})),
    **_for("premium", "SpinnerCircle SpinnerDots SpinnerBars PulseDots PulseWave InfinityLoader",
           frozenset({"secondary_color"})),
    **_for("premium", "OrbitDots", frozenset({"thickness"})),
    **_for("premium", "BouncingDots", frozenset({"size", "reverse"})),
    # Size already sets the box (2:1); explicit height/width would override it.
    **_for("premium", "ShimmerBox", frozenset({"height", "width"})),
    **_for("premium", "ButtonSpinner", frozenset({"secondary_color", "reverse"})),
    **_for("premium", "SuccessCheckmark", frozenset({"secondary_color"})),
    **_for("indicators", "Atom BlinkBlur Commet FourSquare LifeLine Mosaic Riple Slab TrophySpin",
           frozenset({"variant"})),
}

# Where a spinner's own default differs from the family-wide PROP_SPECS one.
# Controls start here, so the page shows what `dlc.<family>.<Name>()` renders;
# tests/test_gallery_controls.py renders both and compares.
UPSTREAM_DEFAULTS: dict[tuple[str, str], dict[str, Any]] = {
    ("ldrs", "Ring"): {"stroke": 5, "bg_opacity": 0},
    ("ldrs", "LineSpinner"): {"stroke": 3},
    ("spinners", "ScaleLoader"): {"height": 35, "width": 4, "radius": 2},
    ("spinners", "BarLoader"): {"height": 4, "width": 100},
    **_for("spinners_react", "SpinnerCircular SpinnerCircularFixed SpinnerCircularSplit "
           "SpinnerInfinity SpinnerDiamond", {"secondary_color": "rgba(0,0,0,0.44)"}),
    ("loader_spinner", "TailSpin"): {"stroke_width": 2, "radius": 1},
    ("loader_spinner", "Oval"): {"stroke_width": 2, "secondary_color": "#4fa94d"},
    ("loader_spinner", "Rings"): {"radius": 6},
    ("loader_spinner", "BallTriangle"): {"radius": 5},
    ("loader_spinner", "Grid"): {"radius": 12.5},
    ("premium", "SpinnerCircle"): {"thickness": 4},
    ("premium", "SpinnerRing"): {"thickness": 4, "secondary_color": "rgba(0, 0, 0, 0.1)"},
    ("premium", "SpinnerDots"): {"dot_count": 8, "dot_size": 4},
    ("premium", "OrbitDots"): {"dot_count": 4, "dot_size": 8, "orbit_radius": 0.4},
    # A skeleton shimmer, so it keeps upstream's greys rather than the accent.
    ("premium", "ShimmerBox"): {"color": "#e5e7eb", "secondary_color": "#f3f4f6"},
}

# Props the gallery always passes, even at their default: the spinner's size
# and the accent color. Everything else is sent only once it is changed.
ALWAYS_SENT = frozenset({"size", "color"})


# Preferred control order per family (props not listed still appear after)
FAMILY_PROP_ORDER = {
    "loading_dev": ["size", "color", "rate", "playing", "easing", "cap", "sweep", "direction", "origin", "className"],
    "ldrs": ["size", "color", "rate", "playing", "stroke", "stroke_length", "bg_opacity", "className"],
    "spinners": ["size", "color", "rate", "playing", "margin", "height", "width", "radius", "bar_count", "loading", "className"],
    "spinners_react": ["size", "color", "rate", "playing", "thickness", "secondary_color", "enabled", "className"],
    "loader_spinner": [
        "size", "height", "width", "color", "playing", "secondary_color", "stroke_width",
        "stroke_width_secondary", "animation_duration", "radius", "visible", "aria_label", "className",
    ],
    "premium": [
        "size", "color", "rate", "playing", "secondary_color", "thickness", "reverse",
        "dot_count", "dot_size", "bar_count", "ring_count", "ring_gap", "alternate",
        "orbit_radius", "stagger", "visible", "className",
    ],
    "indicators": ["size", "color", "rate", "playing", "easing", "text", "text_color", "variant", "dense", "className"],
    "m3": ["size", "color", "rate", "playing", "contained", "container_color", "size_ratio", "className"],
    "epic": ["size", "color", "rate", "playing", "className"],
}


# ---------------------------------------------------------------------------
# Upstream families (credits page, overview sections, nav)
# ---------------------------------------------------------------------------

UPSTREAM_CREDITS = [
    {
        "family": "loading_dev", "npm": "loading-dev", "version": "0.3.4", "spdx": "MIT",
        "homepage": "https://loading.dev/", "repo": "https://github.com/jakubkrehel/loading",
        "blurb": "Refined, lightweight loaders from loading.dev. The family that sets the React 19 floor.",
        "status": "mvp",
    },
    {
        "family": "ldrs", "npm": "ldrs", "version": "1.1.9", "spdx": "MIT",
        "homepage": "https://uiball.com/ldrs/", "repo": "https://github.com/GriffinJohnston/ldrs",
        "blurb": "CSS-animated web-component loaders by UI Ball.",
        "status": "mvp",
    },
    {
        "family": "spinners", "npm": "react-spinners", "version": "0.17.1", "spdx": "MIT",
        "homepage": "https://www.npmjs.com/package/react-spinners",
        "repo": "https://github.com/davidhu2000/react-spinners",
        "blurb": "The classic react-spinners set, the one dash-loading-spinners also wraps.",
        "status": "mvp",
    },
    {
        "family": "spinners_react", "npm": "spinners-react", "version": "1.0.11", "spdx": "MIT",
        "homepage": "https://www.npmjs.com/package/spinners-react",
        "repo": "https://github.com/adexin/spinners-react",
        "blurb": "Lightweight SVG spinners with speed and thickness controls.",
        "status": "mvp",
    },
    {
        "family": "loader_spinner", "npm": "react-loader-spinner", "version": "8.0.2",
        "spdx": "MIT", "homepage": "https://www.npmjs.com/package/react-loader-spinner",
        "repo": "https://github.com/mhnpd/react-loader-spinner",
        "blurb": "SVG loaders sized by height and width, with stroke and radius controls.",
        "status": "mvp",
    },
    {
        "family": "premium", "npm": "premium-react-loaders", "version": "4.2.0", "spdx": "MIT",
        "homepage": "https://www.npmjs.com/package/premium-react-loaders", "repo": None,
        "blurb": "Orbit, dot and bar loaders, plus a shimmer skeleton and a success checkmark.",
        "status": "mvp",
    },
    {
        "family": "indicators", "npm": "react-loading-indicators", "version": "1.0.1",
        "spdx": "MIT", "homepage": "https://www.npmjs.com/package/react-loading-indicators",
        "repo": None,
        "blurb": "Indicators sized by token (small, medium, large), with variants and an optional label.",
        "status": "mvp",
    },
    {
        "family": "m3", "npm": "@alerix/m3-loading-indicator", "version": "1.0.5",
        "spdx": "Apache-2.0", "homepage": "https://www.npmjs.com/package/@alerix/m3-loading-indicator",
        "repo": None,
        "blurb": "The Material 3 Expressive loading indicator, a shape that morphs as it turns.",
        "status": "mvp",
    },
    {
        "family": "epic", "npm": "react-epic-spinners", "version": "0.6.0", "spdx": "MIT",
        "homepage": "https://www.npmjs.com/package/react-epic-spinners",
        "repo": "https://github.com/bondz/react-epic-spinners",
        "blurb": "Ported from epic-spinners for Vue.",
        "status": "mvp",
    },
    {
        "family": "svg_spinners", "npm": "react-svg-spinners", "version": "0.3.1", "spdx": "MIT",
        "homepage": "https://www.npmjs.com/package/react-svg-spinners",
        "repo": "https://github.com/theme-park/react-svg-spinners",
        "blurb": "Not wrapped yet: its React ^18.2 peer range does not admit React 19.",
        "status": "gated",
    },
]
CREDITS_BY_FAMILY = {entry["family"]: entry for entry in UPSTREAM_CREDITS}

# Every component in nav order, for the pager and the search index
CATALOG: list[tuple[str, str]] = [
    (family, name) for family, _label, items in FAMILIES for name, _comp in items
]


# ---------------------------------------------------------------------------
# Values: controls → what the spinner is given
# ---------------------------------------------------------------------------

def description_for(family: str, name: str, upstream: str) -> str:
    if family == "loading_dev" and name in LOADING_DEV_BLURBS:
        return LOADING_DEV_BLURBS[name]
    return f"The {name} loader from {upstream}, as a Dash component."


def detail_path(family: str, name: str) -> str:
    return f"/c/{family}/{name}"


def parse_pathname(pathname: Optional[str]) -> tuple[str, Optional[str], Optional[str]]:
    """Return (mode, family, name). mode is 'overview' | 'detail' | 'credits' | 'unknown'."""
    if not pathname or pathname == "/":
        return "overview", None, None
    pathname = unquote(pathname.rstrip("/") or "/")
    if pathname in ("/credits", "/licenses"):
        return "credits", None, None
    m = re.match(r"^/c/([a-z0-9_]+)/([A-Za-z0-9_]+)$", pathname)
    if m:
        family, name = m.group(1), m.group(2)
        if (family, name) in COMPONENT_LOOKUP:
            return "detail", family, name
    return "unknown", None, None


def configurable_props(family: str, name: str, component: Callable) -> list[str]:
    """Dash-exposed props that make sense as controls for this spinner.

    Upstream tempo and pause props give way to the contract's `rate` and
    `playing`; a family with no tempo prop shows no rate control.
    """
    try:
        available = list(component().available_properties)
    except Exception:
        available = []
    props = [p for p in available if p not in SKIP_UI_PROPS]

    # loading_dev: only show easing/cap when the wrapper actually exposes them
    if family == "loading_dev":
        if name not in LOADING_DEV_EASING:
            props = [p for p in props if p != "easing"]
        if name not in LOADING_DEV_CAP:
            props = [p for p in props if p != "cap"]

    replaced = NATIVE_PLAY_PROPS | (frozenset() if family in RATELESS_FAMILIES else NATIVE_TEMPO_PROPS)
    props = [p for p in props if p not in replaced]
    if family in RATELESS_FAMILIES:
        props.remove("rate")

    ignored = IGNORED_PROPS.get((family, name), frozenset())
    props = [p for p in props if p not in ignored]

    order = [p for p in FAMILY_PROP_ORDER.get(family, []) if p in props]
    return order + [p for p in props if p not in order]


def default_values(family: str, name: str, props: list[str]) -> dict[str, Any]:
    """What each control starts at: the spinner's own default where known."""
    overrides = UPSTREAM_DEFAULTS.get((family, name), {})
    values: dict[str, Any] = {}
    for p in props:
        if p in overrides:
            values[p] = overrides[p]
        elif family == "indicators" and p == "size":
            values[p] = "medium"
        elif p == "size" and uses_size_presets(family, props):
            values[p] = SIZE_PRESET_DEFAULT
        else:
            spec = prop_spec(family, p, name)
            values[p] = spec["default"] if spec else None
    return values


def sent_values(family: str, name: str, values: dict[str, Any]) -> dict[str, Any]:
    """The props the spinner is given: size and color, plus every control
    that has moved off the spinner's own default.

    Leaving the rest out is what makes the preview, the snippets and the
    overview card render exactly what `dlc.<family>.<Name>()` does.
    """
    defaults = default_values(family, name, list(values))
    keep = ALWAYS_SENT
    return {
        k: v
        for k, v in values.items()
        if k in keep or (v != defaults.get(k) and v not in ("", None))
    }


def instantiate(family: str, name: str, values: dict[str, Any]):
    """Live preview: exactly the call the snippet shows."""
    try:
        return COMPONENT_LOOKUP[(family, name)](**values)
    except Exception as exc:
        return html.Div(f"error: {exc}", className="dlc-error")


def format_py_value(v: Any) -> str:
    if isinstance(v, bool):
        return "True" if v else "False"
    if isinstance(v, str):
        return f'"{v}"'
    if isinstance(v, float) and v == int(v):
        return f"{v:.1f}"  # keep relative speed readable as 1.0, not 1
    return repr(v)


# Every snippet the gallery renders goes through Black, at a width that fits
# the demo card's code panel without soft wrapping.
SNIPPET_LINE_LENGTH = 64


def format_python_snippet(source: str, line_length: int = SNIPPET_LINE_LENGTH) -> str:
    """Format displayed Python with Black without making the gallery fragile."""
    if black is None:
        logger.warning("Black is unavailable; displaying an unformatted snippet")
        return source
    try:
        return black.format_str(source, mode=black.Mode(line_length=line_length))
    except Exception:
        logger.warning("Black failed to format gallery snippet; using raw source", exc_info=True)
        return source


def build_snippet(family: str, name: str, values: dict[str, Any]) -> str:
    parts = [f"{k}={format_py_value(v)}" for k, v in values.items()]
    return format_python_snippet(
        f"import dash_loading_components as dlc\n\ndlc.{family}.{name}({', '.join(parts)})\n"
    )


# Loaders whose animation sweeps well past their own box. Shrinking `size`
# either does not help (react-loading-indicators takes size tokens, not
# pixels) or leaves the loader too small to read, so scale the whole preview
# down instead: same proportions, just fitted to the card. The clipping test
# in tests/test_gallery_overview.py keeps these honest.
OVERVIEW_SCALE: dict[tuple[str, str], float] = {
    ("spinners", "PropagateLoader"): 0.7,
    ("spinners", "GridLoader"): 0.7,
    ("indicators", "LifeLine"): 0.8,
    ("epic", "HollowDotsSpinner"): 0.5,
}

# Card size overrides: the card shows the page's defaults at a size that fits.
OVERVIEW_SIZE: dict[tuple[str, str], dict[str, Any]] = {
    **_for("indicators", " ".join(n for n, _ in FAMILY_LOOKUP["indicators"][1]),
           {"size": "small"}),
}


def overview_values(family: str, name: str) -> dict[str, Any]:
    """Exactly what the component page starts with, sized for the card."""
    props = configurable_props(family, name, COMPONENT_LOOKUP[(family, name)])
    values = sent_values(family, name, default_values(family, name, props))
    values.update(OVERVIEW_SIZE.get((family, name), {}))
    return values



# ---------------------------------------------------------------------------
# Layout builders (dash-mantine-components)
# ---------------------------------------------------------------------------

THEME = {
    "primaryColor": "orange",
    "defaultRadius": "md",
    "fontFamily": "ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif",
    "fontFamilyMonospace": "ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace",
    "headings": {"fontWeight": "650"},
}

HEADER_HEIGHT = 60
NAVBAR_WIDTH = 280
COLOR_SWATCHES = [
    "#f97316", "#ef4444", "#ec4899", "#a855f7", "#6366f1", "#3b82f6",
    "#06b6d4", "#10b981", "#84cc16", "#eab308", "#71717a", "#18181b",
]


def icon(name: str, className: str = "") -> html.Span:
    """One mask-image SVG from assets/icons, painted in currentColor."""
    return html.Span(className=f"dlc-icon dlc-icon-{name} {className}".strip(), **{"aria-hidden": "true"})


def external_link(children, href: str, **kwargs) -> dmc.Anchor:
    return dmc.Anchor(children, href=href, target="_blank", **kwargs)


def uses_size_presets(family: str, props: list[str]) -> bool:
    """Prefer Small/Medium/Large presets when size is a numeric px prop."""
    return "size" in props and family not in ("indicators", "loader_spinner")


def search_data() -> list[dict]:
    """Select groups for the header search: every component, then pages."""
    groups = [
        {
            "group": f"{label} · dlc.{key}",
            "items": [{"value": detail_path(key, name), "label": name} for name, _c in items],
        }
        for key, label, items in FAMILIES
    ]
    groups.append({"group": "Pages", "items": [
        {"value": "/", "label": "Overview"},
        {"value": "/credits", "label": "Credits & Licenses"},
    ]})
    return groups


def build_header() -> dmc.AppShellHeader:
    version = dlc.__version__
    return dmc.AppShellHeader(
        dmc.Group(
            [
                dmc.Group(
                    [
                        dmc.Burger(id="nav-burger", size="sm", hiddenFrom="sm",
                                   **{"aria-label": "Toggle navigation"}),
                        dmc.Anchor(
                            [
                                html.Span(
                                    dlc.loading_dev.Loading(size=20, color=DEFAULT_COLOR),
                                    className="dlc-brand-mark",
                                ),
                                html.Span("dash-loading-components", className="dlc-brand-name"),
                            ],
                            href="/",
                            underline="never",
                            className="dlc-brand",
                        ),
                        # Unreleased builds carry 0.0.0, which reads as broken.
                        *([dmc.Badge(f"v{version}", variant="light", visibleFrom="xs")]
                          if version != "0.0.0" else []),
                    ],
                    gap="sm",
                    wrap="nowrap",
                ),
                dmc.Group(
                    [
                        dmc.Select(
                            id="site-search",
                            data=search_data(),
                            searchable=True,
                            clearable=False,
                            value=None,
                            placeholder="Search",
                            nothingFoundMessage="No components match",
                            leftSection=icon("search"),
                            rightSection=dmc.Kbd(
                                [html.Span("⌘", className="dlc-mod-mac"),
                                 html.Span("Ctrl", className="dlc-mod-other"), " K"],
                                size="xs", className="dlc-kbd",
                            ),
                            rightSectionWidth=52,
                            rightSectionPointerEvents="none",
                            maxDropdownHeight=380,
                            limit=40,
                            w={"base": 170, "sm": 260},
                            className="dlc-search",
                            comboboxProps={"shadow": "md"},
                            **{"aria-label": "Search components"},
                        ),
                        external_link(
                            dmc.ActionIcon(icon("github"), variant="default", size="lg",
                                           **{"aria-label": "Source on GitHub"}),
                            REPO_URL,
                        ),
                        dmc.ColorSchemeToggle(
                            lightIcon=icon("moon"),
                            darkIcon=icon("sun"),
                            variant="default",
                            size="lg",
                            **{"aria-label": "Toggle color scheme"},
                        ),
                    ],
                    gap="xs",
                    wrap="nowrap",
                ),
            ],
            justify="space-between",
            h="100%",
            px="md",
            wrap="nowrap",
        )
    )


def build_navbar() -> dmc.AppShellNavbar:
    """Static navbar; NavLink `active="exact"` follows the URL on its own."""
    sections = [
        dmc.NavLink(label="Overview", href="/", leftSection=icon("overview"), active="exact"),
        dmc.NavLink(label="Credits & Licenses", href="/credits", leftSection=icon("credits"),
                    active="exact"),
    ]
    for key, label, items in FAMILIES:
        sections.append(
            dmc.Group(
                [icon(key), dmc.Text(label, size="xs", fw=600, tt="uppercase", c="dimmed"),
                 dmc.Divider(style={"flex": 1}),
                 dmc.Text(str(len(items)), size="xs", c="dimmed", className="dlc-tabular")],
                gap=8,
                wrap="nowrap",
                className="dlc-nav-section",
            )
        )
        sections += [
            dmc.NavLink(label=name, href=detail_path(key, name), active="exact",
                        className="dlc-nav-link")
            for name, _comp in items
        ]
    return dmc.AppShellNavbar(
        dmc.ScrollArea(sections, type="scroll", className="dlc-nav-scroll"),
        id="dlc-navbar",
    )


def build_footer() -> html.Footer:
    return html.Footer(
        dmc.Group(
            [
                dmc.Text(["Made with care by ", external_link("PhylaTech", "https://github.com/PhylaTech")],
                         size="sm", c="dimmed"),
                dmc.Text(["Built on ", external_link("Plotly Dash", "https://dash.plotly.com"), " and ",
                          external_link("Dash Mantine Components", "https://www.dash-mantine-components.com")],
                         size="sm", c="dimmed"),
                dmc.Anchor("Credits & Licenses", href="/credits", size="sm"),
            ],
            gap="lg",
        ),
        className="dlc-footer",
    )


def make_overview_card(family: str, name: str) -> dmc.Anchor:
    node = instantiate(family, name, overview_values(family, name))
    scale = OVERVIEW_SCALE.get((family, name))
    if scale is not None:
        node = html.Div(node, style={"transform": f"scale({scale})"})
    return dmc.Anchor(
        [html.Div(node, className="preview"), html.Div(name, className="name")],
        href=detail_path(family, name),
        underline="never",
        className="dlc-card",
        **{"data-family": family, "data-name": name},
    )


def build_overview() -> html.Div:
    sections = []
    for key, label, items in FAMILIES:
        credit = CREDITS_BY_FAMILY[key]
        sections.append(
            html.Section(
                [
                    dmc.Group(
                        [
                            dmc.Title([icon(key), label], order=2, className="dlc-family-title"),
                            dmc.Code(f"dlc.{key}"),
                            dmc.Badge(str(len(items)), variant="light", color="gray", radius="sm",
                                      className="dlc-tabular"),
                            external_link([credit["npm"], icon("external")], credit["homepage"],
                                          size="sm", c="dimmed", className="dlc-family-link"),
                        ],
                        gap="sm",
                        align="center",
                    ),
                    dmc.Text(credit["blurb"], c="dimmed", size="sm", mt=6, mb="md"),
                    html.Div([make_overview_card(key, n) for n, _c in items], className="dlc-grid"),
                ],
                id=f"family-{key}",
                className="dlc-family",
            )
        )
    return html.Div(
        [
            html.Section(
                [
                    dmc.Title(["Loading,", html.Br(), html.Span("made beautiful for Dash.")],
                              order=1, className="dlc-hero-title"),
                    dmc.Text(
                        f"{len(CATALOG)} loading indicators from {len(FAMILIES)} React libraries, "
                        "as Dash components that all speak the same size, color, rate and playing.",
                        c="dimmed", size="lg", maw=560, className="dlc-hero-lede",
                    ),
                    dmc.CodeHighlight(code="pip install dash-loading-components", language="bash",
                                      className="dlc-install", maw=560, mb="sm"),
                    dmc.CodeHighlight(
                        code=format_python_snippet(
                            "import dash_loading_components as dlc\n\n"
                            "# size, color, rate and playing work the same on every component\n"
                            'dlc.loading_dev.Dual(size=48, color="#f97316", rate=1.5)\n\n'
                            "# each library's own props are there too, in snake_case\n"
                            'dlc.premium.OrbitRings(size=48, color="#f97316", ring_count=4)\n'
                        ).rstrip(),
                        language="python",
                        maw=560,
                        className="dlc-hero-code",
                    ),
                ],
                className="dlc-hero",
            ),
            *sections,
            build_footer(),
        ],
        className="dlc-page",
    )


def section_title(prop: str) -> str:
    return PROP_SECTION_TITLES.get(prop, prop)


def section_copy(family: str, prop: str) -> str:
    if family == "indicators" and prop == "size":
        return "A size token: small, medium or large."
    if family == "indicators" and prop == "easing":
        return "The CSS easing of each cycle. Empty keeps the curve each indicator is designed with."
    return PROP_SECTION_COPY.get(prop, f"Configurable `{prop}` for this wrapper.")


def workbench_control(prop: str, value: Any, family: str, props: list[str], name: str):
    """One control in the demo card. Switches report `checked`, the rest `value`."""
    label = section_title(prop)
    spec = prop_spec(family, prop, name) or {"kind": "text", "default": ""}
    presets = prop == "size" and (family == "indicators" or uses_size_presets(family, props))
    kind = "segmented" if presets else spec["kind"]
    ctrl_id = {"type": "prop-ctrl", "prop": prop, "kind": kind}

    def segmented(options: list[tuple[str, str]], current: str):
        return dmc.Stack(
            [dmc.Text(label, size="sm", fw=500),
             dmc.SegmentedControl(id=ctrl_id, data=[{"label": l, "value": v} for l, v in options],
                                  value=current, fullWidth=True, size="xs")],
            gap=4,
        )

    if family == "indicators" and prop == "size":
        return segmented([("Small", "small"), ("Medium", "medium"), ("Large", "large")], value)
    if prop == "size" and uses_size_presets(family, props):
        # SegmentedControl values are strings; _coerce_control_value turns them back.
        preset = value if value in SIZE_PRESET_VALUES else SIZE_PRESET_DEFAULT
        return segmented([(l, str(v)) for l, v in SIZE_PRESETS], str(preset))

    if kind == "slider":
        current = value if value is not None else spec["default"]
        return dmc.Stack(
            [dmc.Group([dmc.Text(label, size="sm", fw=500),
                        dmc.Text(f"{current:g}", id={"type": "prop-readout", "prop": prop},
                                 size="xs", c="dimmed", className="dlc-tabular")],
                       justify="space-between"),
             dmc.Slider(id=ctrl_id, min=spec["min"], max=spec["max"], step=spec["step"],
                        value=current, updatemode="drag", size="sm", label=None,
                        className="dlc-ctrl-slider")],
            gap=6,
        )
    if kind == "color":
        return dmc.ColorInput(
            id=ctrl_id, label=label, value=value or "", placeholder="Default",
            format="rgba" if "rgba" in (value or "") else "hex",
            swatches=COLOR_SWATCHES, swatchesPerRow=6, size="sm",
        )
    if kind == "enum":
        opts = spec["options"]
        labels = spec.get("labels") or {o: o for o in opts}
        return segmented([(labels[o], o) for o in opts], value if value in opts else spec["default"])
    if kind == "dropdown":
        return dmc.Select(
            id=ctrl_id, label=label, data=spec["options"], value=value,
            clearable=spec["default"] is None, placeholder="Default", size="sm",
            allowDeselect=spec["default"] is None,
        )
    if kind == "bool":
        return dmc.Switch(id={"type": "prop-switch", "prop": prop}, label=label,
                          checked=bool(value), size="sm")
    return dmc.TextInput(id=ctrl_id, label=label, value=value or "",
                         placeholder=spec.get("placeholder", ""), debounce=400, size="sm")


def build_prop_doc_section(family: str, prop: str, default: Any) -> html.Section:
    meta = [dmc.Code(prop)]
    if prop not in ALWAYS_SENT and default not in ("", None):
        meta += [dmc.Text("default", size="xs", c="dimmed"), dmc.Code(format_py_value(default))]
    return html.Section(
        [
            dmc.Title(section_title(prop), order=3, className="dlc-toc-target"),
            dmc.Group(meta, gap=6, mt=4, mb=6),
            dmc.Text(section_copy(family, prop), c="dimmed", size="sm", maw=640),
        ],
        id=f"section-{prop}",
        className="dlc-prop-doc",
    )


def build_pager(family: str, name: str) -> dmc.SimpleGrid:
    i = CATALOG.index((family, name))
    cells = []
    for label, j, align in (("Previous", i - 1, "left"), ("Next", i + 1, "right")):
        if 0 <= j < len(CATALOG):
            f, n = CATALOG[j]
            cells.append(dmc.Anchor(
                dmc.Paper([dmc.Text(label, size="xs", c="dimmed"), dmc.Text(n, fw=600)],
                          withBorder=True, p="md", ta=align, className="dlc-pager-card"),
                href=detail_path(f, n), underline="never",
            ))
        else:
            cells.append(html.Div())
    return dmc.SimpleGrid(cells, cols=2, mt="xl")


def build_detail(family: str, name: str) -> html.Div:
    upstream = FAMILY_LOOKUP[family][0]
    credit = CREDITS_BY_FAMILY[family]
    props = configurable_props(family, name, COMPONENT_LOOKUP[(family, name)])
    values = default_values(family, name, props)
    sent = sent_values(family, name, values)

    wb_props = [p for p in WORKBENCH_PROP_PRIORITY if p in props]
    wb_props += [p for p in props if p not in wb_props]
    controls = [workbench_control(p, values.get(p), family, props, name) for p in wb_props]

    demo = dmc.Paper(
        [
            html.Div(
                [
                    html.Div(instantiate(family, name, sent), id="detail-preview",
                             className="dlc-preview-panel"),
                    html.Div(
                        [
                            dmc.Group(
                                [dmc.Text("Controls", size="xs", fw=700, tt="uppercase", c="dimmed"),
                                 dmc.Button("Reset", id="detail-reset", n_clicks=0, variant="subtle",
                                            size="compact-xs", color="gray",
                                            leftSection=icon("reset"))],
                                justify="space-between",
                            ),
                            dmc.Stack(controls, gap="sm", id="detail-controls"),
                        ],
                        className="dlc-controls",
                    ),
                ],
                className="dlc-demo-top",
            ),
            dmc.CodeHighlight(id="detail-snippet", code=build_snippet(family, name, sent).rstrip(),
                              language="python", className="dlc-demo-code"),
        ],
        withBorder=True,
        radius="lg",
        className="dlc-demo",
    )

    content = html.Div(
        [
            dcc.Store(id="detail-meta", data={"family": family, "name": name, "props": props}),
            dmc.Breadcrumbs(
                [dmc.Anchor([icon(family), upstream], href=f"/#family-{family}", size="sm"),
                 dmc.Text(name, size="sm", **{"aria-current": "page"})],
                separator=icon("chevron"),
            ),
            dmc.Title(name, order=1, mt="xs"),
            dmc.Text(description_for(family, name, upstream), c="dimmed", mt=6, maw=640),
            dmc.Group(
                [
                    dmc.Code(f"dlc.{family}.{name}"),
                    external_link(dmc.Badge([credit["npm"], icon("external")], variant="light",
                                            color="gray", radius="sm", tt="none",
                                            className="dlc-badge-link"),
                                  credit["homepage"]),
                    dmc.Badge(credit["spdx"], variant="outline", color="gray", radius="sm"),
                ],
                gap="xs",
                mt="sm",
            ),
            dmc.Title("Demo", order=2, className="dlc-toc-target dlc-section-title", id="section-preview"),
            demo,
            dmc.Title("Props", order=2, className="dlc-toc-target dlc-section-title"),
            *[build_prop_doc_section(family, p, values.get(p)) for p in props],
            build_pager(family, name),
            build_footer(),
        ],
        className="dlc-detail-content",
    )
    toc = html.Aside(
        [
            dmc.Text("On this page", size="xs", fw=700, tt="uppercase", c="dimmed", mb="xs"),
            dmc.TableOfContents(
                id="detail-toc",
                selector=".dlc-toc-target",
                size="sm",
                variant="light",
                radius="sm",
                minDepthToOffset=2,
                depthOffset=16,
                offset=HEADER_HEIGHT + 16,
                scrollIntoViewOptions={"behavior": "smooth", "block": "start"},
            ),
        ],
        className="dlc-toc",
        **{"aria-label": "On this page"},
    )
    return html.Div([content, toc], className="dlc-page dlc-detail-page")


def _credits_badge(spdx: str) -> dmc.Badge:
    color = "teal" if spdx == "MIT" else "orange" if spdx.startswith("Apache") else "yellow"
    return dmc.Badge(spdx, variant="light", color=color, radius="sm")


def _credits_links(entry: dict) -> list:
    links = [external_link("npm", f"https://www.npmjs.com/package/{entry['npm']}", size="sm")]
    if entry.get("homepage") and "npmjs.com" not in entry["homepage"]:
        links += [" · ", external_link("homepage", entry["homepage"], size="sm")]
    if entry.get("repo"):
        links += [" · ", external_link("repo", entry["repo"], size="sm")]
    return links


def build_credits() -> html.Div:
    rows = [
        dmc.TableTr([
            dmc.TableTd([dmc.Code(f"dlc.{e['family']}"),
                         *([dmc.Badge("gated", variant="light", color="yellow", radius="sm", ml=6)]
                           if e["status"] == "gated" else [])]),
            dmc.TableTd([dmc.Code(e["npm"]), dmc.Text(f" {e['version']}", span=True, size="sm", c="dimmed")]),
            dmc.TableTd(_credits_badge(e["spdx"])),
            dmc.TableTd(_credits_links(e)),
            dmc.TableTd(dmc.Text(e["blurb"], size="sm")),
        ])
        for e in UPSTREAM_CREDITS
    ]
    table = dmc.TableScrollContainer(
        dmc.Table(
            [dmc.TableThead(dmc.TableTr([dmc.TableTh(h) for h in
                                         ("Namespace", "Upstream package", "License", "Links", "Notes")])),
             dmc.TableTbody(rows)],
            verticalSpacing="sm",
            highlightOnHover=True,
            className="dlc-credits-table",
        ),
        minWidth=720,
    )
    return html.Div(
        [
            dmc.Title("Credits & Licenses", order=1),
            dmc.Text(
                [
                    dmc.Text("dash-loading-components", span=True, fw=600, c="var(--mantine-color-text)"),
                    " is licensed under the ",
                    external_link("MIT License", f"{REPO_URL}/blob/main/LICENSE"),
                    " and wraps third-party React loading-indicator libraries, redistributed "
                    "under their own licenses. The full inventory lives in ",
                    external_link("docs/UPSTREAM-INVENTORY.md", f"{REPO_URL}/blob/main/docs/UPSTREAM-INVENTORY.md"),
                    " and the root ",
                    external_link("NOTICE", f"{REPO_URL}/blob/main/NOTICE"),
                    " file.",
                ],
                c="dimmed", maw=720, mt="sm", mb="xl",
            ),
            table,
            dmc.Title("Not wrapped", order=2, mt="xl", size="h3"),
            dmc.Text(
                "css-spinners (GPL-3.0) and react18-loaders (MPL-2.0) are left out: their "
                "licenses are not compatible with MIT distribution.",
                c="dimmed", maw=720, mt="xs",
            ),
            dmc.Text(["Copyright © 2026 ", external_link("Phyla Technologies", "https://github.com/PhylaTech")],
                     size="sm", c="dimmed", mt="xl"),
            build_footer(),
        ],
        className="dlc-page dlc-credits",
    )


def build_404() -> html.Div:
    return html.Div(
        [
            dmc.Title("Not found", order=1),
            dmc.Text("There is no page at this address.", c="dimmed", mt="sm", mb="lg"),
            dmc.Anchor(dmc.Button("Back to the overview", variant="light"), href="/"),
            build_footer(),
        ],
        className="dlc-page",
    )


# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------

_OG_IMAGE = f"{SITE_URL}/assets/og-card.png"
_OG_DESCRIPTION = (
    "Interactive gallery of Dash loading spinners: wrappers for "
    "loading.dev, ldrs, react-spinners, and more. Built by PhylaTech."
)

app = Dash(
    __name__,
    suppress_callback_exceptions=True,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"},
        {"name": "description", "content": _OG_DESCRIPTION},
        {"property": "og:title", "content": "dash-loading-components"},
        {"property": "og:description", "content": _OG_DESCRIPTION},
        {"property": "og:type", "content": "website"},
        {"property": "og:url", "content": f"{SITE_URL}/"},
        {"property": "og:site_name", "content": "PhylaTech"},
        {"property": "og:image", "content": _OG_IMAGE},
        {"property": "og:image:alt", "content": "dash-loading-components: Interactive Dash loading spinner gallery"},
        {"name": "twitter:card", "content": "summary_large_image"},
        {"name": "twitter:title", "content": "dash-loading-components"},
        {"name": "twitter:description", "content": _OG_DESCRIPTION},
        {"name": "twitter:image", "content": _OG_IMAGE},
    ],
)
app.title = "dash-loading-components · gallery"
# WSGI entry point: `gunicorn gallery:server`
server = app.server

# Apply the saved color scheme before first paint, so a dark-mode visitor
# never sees a white flash while the bundle loads. Mantine takes over after,
# reading and writing the same localStorage key.
_COLOR_SCHEME_BOOTSTRAP = (
    "<script>try{var s=localStorage.getItem('mantine-color-scheme-value');"
    "if(!s||s==='auto')s=matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light';"
    "document.documentElement.setAttribute('data-mantine-color-scheme',s)}catch(e){}"
    # The search hint names the modifier this platform uses (⌘ or Ctrl).
    "if(/Mac|iPhone|iPad/.test(navigator.platform))document.documentElement.dataset.mac=''</script>"
)
app.index_string = app.index_string.replace("<head>", "<head>" + _COLOR_SCHEME_BOOTSTRAP, 1)

app.layout = dmc.MantineProvider(
    [
        dcc.Location(id="url", refresh=False),
        dmc.AppShell(
            [
                build_header(),
                build_navbar(),
                dmc.AppShellMain(html.Div(id="page")),
            ],
            id="appshell",
            header={"height": HEADER_HEIGHT},
            navbar={"width": NAVBAR_WIDTH, "breakpoint": "sm", "collapsed": {"mobile": True}},
            padding=0,
        ),
    ],
    theme=THEME,
    defaultColorScheme="auto",
)


@callback(Output("page", "children"), Input("url", "pathname"))
def render_page(pathname):
    mode, family, name = parse_pathname(pathname)
    if mode == "overview":
        return build_overview()
    if mode == "detail":
        return build_detail(family, name)
    if mode == "credits":
        return build_credits()
    return build_404()


@callback(
    Output("url", "pathname"),
    Output("site-search", "value"),
    Input("site-search", "value"),
    prevent_initial_call=True,
)
def go_to_search_result(href):
    """Picking a search result navigates, then clears the box for the next search."""
    if not href:
        return no_update, no_update
    return href, None


# The mobile navbar opens from the burger and closes on navigation. Both run
# in the browser: a server round trip here reads as a sticky drawer.
clientside_callback(
    """(opened, navbar) => ({...navbar, collapsed: {mobile: !opened}})""",
    Output("appshell", "navbar"),
    Input("nav-burger", "opened"),
    State("appshell", "navbar"),
)
clientside_callback(
    """() => false""",
    Output("nav-burger", "opened"),
    Input("url", "pathname"),
    prevent_initial_call=True,
)


def _coerce_control_value(prop: str, raw: Any, family: str, name: str) -> Any:
    spec = prop_spec(family, prop, name)
    if family == "indicators" and prop == "size":
        return raw
    if prop == "size":
        return int(float(raw)) if raw not in (None, "") else SIZE_PRESET_DEFAULT
    if spec and spec["kind"] == "bool":
        return bool(raw)
    if spec and spec["kind"] == "slider":
        if raw is None:
            return spec["default"]
        return int(raw) if float(spec["step"]).is_integer() else float(raw)
    if spec and spec["kind"] in ("text", "color"):
        return (raw or "").strip()
    return raw


def _control_values(family: str, name: str, props: list[str]) -> tuple[dict, dict]:
    """Page defaults split into (value controls, switches), in control form."""
    defaults = default_values(family, name, props)
    values, switches = {}, {}
    for prop, v in defaults.items():
        spec = prop_spec(family, prop, name)
        if spec and spec["kind"] == "bool" and not (family == "indicators" and prop == "size"):
            switches[prop] = bool(v)
        elif prop == "size" and uses_size_presets(family, props):
            values[prop] = str(v)
        elif spec and spec["kind"] in ("text", "color"):
            values[prop] = v or ""
        else:
            values[prop] = v
    return values, switches


@callback(
    Output({"type": "prop-ctrl", "prop": ALL, "kind": ALL}, "value"),
    Output({"type": "prop-switch", "prop": ALL}, "checked"),
    Input("detail-reset", "n_clicks"),
    State({"type": "prop-ctrl", "prop": ALL, "kind": ALL}, "id"),
    State({"type": "prop-switch", "prop": ALL}, "id"),
    State("detail-meta", "data"),
    prevent_initial_call=True,
)
def reset_detail_controls(n_clicks, value_ids, switch_ids, meta):
    """Put every control back where the page started."""
    if not n_clicks or not meta:
        return no_update, no_update
    values, switches = _control_values(meta["family"], meta["name"], meta["props"])
    return ([values.get(i["prop"]) for i in value_ids],
            [switches.get(i["prop"], False) for i in switch_ids])


@callback(
    Output("detail-preview", "children"),
    Output("detail-snippet", "code"),
    Input({"type": "prop-ctrl", "prop": ALL, "kind": ALL}, "value"),
    Input({"type": "prop-switch", "prop": ALL}, "checked"),
    State({"type": "prop-ctrl", "prop": ALL, "kind": ALL}, "id"),
    State({"type": "prop-switch", "prop": ALL}, "id"),
    State("detail-meta", "data"),
    prevent_initial_call=True,
)
def update_detail(raw_values, raw_checked, value_ids, switch_ids, meta):
    if not meta:
        return no_update, no_update
    family, name = meta["family"], meta["name"]
    collected = {
        i["prop"]: _coerce_control_value(i["prop"], raw, family, name)
        for raw, i in [*zip(raw_values, value_ids), *zip(raw_checked, switch_ids)]
    }
    # Snippet order follows the page's prop order, not the control order.
    values = {p: collected[p] for p in meta["props"] if p in collected}
    sent = sent_values(family, name, values)
    return instantiate(family, name, sent), build_snippet(family, name, sent).rstrip()


# Slider readouts follow the thumb without a server round trip, formatted as
# the server's f"{v:g}" first renders them (0.1 steps arrive as 1.2000000002).
clientside_callback(
    """(v) => String(+Number(v).toFixed(4))""",
    Output({"type": "prop-readout", "prop": MATCH}, "children"),
    Input({"type": "prop-ctrl", "prop": MATCH, "kind": "slider"}, "value"),
    prevent_initial_call=True,
)


if __name__ == "__main__":
    _port = int(os.environ.get("PORT", "8050"))
    print("dlc gallery: http://127.0.0.1:%d/  (REACT_VERSION=%s)" % (_port, os.environ.get("REACT_VERSION")))
    app.run(host="0.0.0.0", port=_port, debug=False)
