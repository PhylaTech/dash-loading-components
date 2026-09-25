"""Local gallery explorer for dash-loading-components.

loading.dev-style UX:
  /                      overview — left sticky nav + component cards
  /c/<family>/<Name>     component detail — split workbench, dual snippets,
                         right TOC, per-prop docs

Run:
  source /workspace/dash-loading/.venv/bin/activate
  cd /workspace/dash-loading/dash-loading-components
  REACT_VERSION=19.2.4 python gallery.py
"""
from __future__ import annotations

import logging
import os
import re
from typing import Any, Callable, Optional
from urllib.parse import unquote

os.environ.setdefault("REACT_VERSION", "19.2.4")

import dash
from dash import Dash, html, dcc, Input, Output, State, ALL, callback, ctx, no_update

import dash_loading_components as dlc

try:
    import black
except ImportError:  # pragma: no cover - deployment installs Black in the venv
    black = None

logger = logging.getLogger(__name__)

try:
    dash._dash_renderer._set_react_version("19.2.4")
except Exception as exc:  # pragma: no cover
    print("warn: could not set React version via _set_react_version:", exc)

DEFAULT_COLOR = "#f97316"
DEFAULT_SIZE = 48
ACCENT = "#f97316"

# Size presets for workbench (px) — loading.dev-style Small / Medium / Large
SIZE_PRESETS = [("Small", 24), ("Medium", 48), ("Large", 96)]
SIZE_PRESET_VALUES = {v for _, v in SIZE_PRESETS}
SIZE_PRESET_DEFAULT = 48

# Props shown as compact workbench controls (order preference within available)
WORKBENCH_PROP_PRIORITY = [
    "size", "height", "width", "color", "speed",
    "easing", "cap", "sweep", "direction", "origin",
    "thickness", "stroke", "strokeWidth", "strokeWidthSecondary",
    "strokeLength", "bgOpacity", "secondaryColor", "margin",
    "playState", "paused", "loading", "enabled", "visible", "still",
    "reverse", "dense", "variant", "contained",
    "containerColor", "sizeRatio", "radius", "barCount", "dotCount",
    "dotSize", "ringCount", "ringGap", "alternate", "orbitRadius", "stagger",
    "text", "textColor", "ariaLabel", "className",
]

PROP_SECTION_TITLES = {
    "size": "Size",
    "height": "Height",
    "width": "Width",
    "color": "Color",
    "speed": "Speed",
    "duration": "Duration",
    "easing": "Easing",
    "cap": "Cap",
    "playState": "State",
    "thickness": "Thickness",
    "stroke": "Stroke",
    "strokeWidth": "Stroke width",
    "secondaryColor": "Secondary color",
    "margin": "Margin",
    "loading": "Loading",
    "enabled": "Enabled",
    "visible": "Visible",
    "paused": "Paused",
    "variant": "Variant",
    "contained": "Contained",
    "containerColor": "Container color",
    "sizeRatio": "Size ratio",
    "radius": "Radius",
    "text": "Text",
    "textColor": "Text color",
    "ariaLabel": "aria-label",
    "className": "Custom Classes",
    "sweep": "Sweep",
    "direction": "Direction",
    "origin": "Origin",
    "speedMultiplier": "Speed multiplier",
    "speedPlus": "Speed plus",
    "animationDuration": "Animation duration",
    "still": "Still",
    "reverse": "Reverse",
    "ringCount": "Ring count",
    "ringGap": "Ring gap",
    "alternate": "Alternate",
    "orbitRadius": "Orbit radius",
    "stagger": "Stagger",
    "dense": "Dense",
    "bgOpacity": "Background opacity",
    "strokeLength": "Stroke length",
    "strokeWidthSecondary": "Secondary stroke",
    "barCount": "Bar count",
    "dotCount": "Dot count",
    "dotSize": "Dot size",
}

PROP_SECTION_COPY = {
    "size": (
        "Sets the spinner’s dimensions in pixels. "
        "Workbench presets map to Small (24), Medium (48), and Large (96)."
    ),
    "height": "Height in pixels for loaders that expose height separately from width.",
    "width": "Width in pixels for loaders that expose width separately from height.",
    "color": "Any valid CSS color. The gallery default accent is #f97316.",
    "speed": (
        "Relative rate for the Common API: 1.0 = this spinner’s normal tempo, "
        "the tempo it runs at upstream with no tempo prop set. "
        "The Namespaced snippet shows the translated native unit "
        "(duration ms, speedMultiplier, percent, etc.)."
    ),
    "duration": "Animation cycle length in milliseconds. Higher values are slower.",
    "easing": "Rotation easing: linear, ease-in-out, or stacked (loading-dev).",
    "cap": "Stroke end style: round or flat (loading-dev).",
    "playState": "Whether the animation is running or paused.",
    "thickness": "Stroke thickness (spinners-react).",
    "stroke": "Stroke width for line-based loaders.",
    "strokeWidth": "Stroke width in pixels.",
    "secondaryColor": "Secondary / track color when the spinner uses two tones.",
    "margin": "Spacing between spinner elements.",
    "loading": "Whether the spinner is shown (react-spinners).",
    "enabled": "Whether the spinner is enabled (spinners-react).",
    "visible": "Visibility toggle.",
    "paused": "Pause the Material loading indicator.",
    "variant": "Visual variant when the upstream component supports it.",
    "contained": "Show the Material container track.",
    "containerColor": "Color of the Material container track.",
    "sizeRatio": "Inner size relative to the container.",
    "radius": "Corner or arc radius.",
    "text": "Optional label text beside the indicator.",
    "textColor": "Label text color.",
    "ariaLabel": "Accessible name announced to assistive tech.",
    "className": (
        "You can use a custom className in case you need to tweak the spinner "
        "in a specific way that the library doesn’t provide. "
        "On loading_dev wrappers it is merged onto the spinner root "
        "(same as loading.dev)."
    ),
    "sweep": (
        "Controls which way the sweep runs. diagonal goes from the top left "
        "corner to the bottom right, rows from top to bottom, columns from "
        "left to right. The default sweep is diagonal."
    ),
    "direction": (
        "Controls which way the motion travels. out spreads it from the "
        "center, in draws it into the center. The default direction is out."
    ),
    "origin": (
        "Controls where the spinner grows from. center scales it from the "
        "middle, bottom keeps its base fixed so it rises from the baseline. "
        "The default origin is center."
    ),
    "speedMultiplier": "Speed multiplier (react-spinners).",
    "speedPlus": "Speed adjustment in [-5, 5] (react-loading-indicators).",
    "animationDuration": "Animation duration in milliseconds (epic-spinners).",
    "still": "Disable animation while keeping the spinner visible (spinners-react).",
    "reverse": "Reverse animation direction (premium-react-loaders).",
    "dense": "Make OrbitProgress more bold/compact (react-loading-indicators).",
    "bgOpacity": "Background / track opacity for ldrs loaders that expose it (0–1).",
    "strokeLength": "Fraction of the path that is stroked for ldrs Infinity (0–1).",
    "strokeWidthSecondary": "Stroke width of the Oval background circle.",
    "barCount": "Number of bars (ScaleLoader / Premium SpinnerBars).",
    "dotCount": "Number of dots (Premium SpinnerDots).",
    "dotSize": "Size of each dot (Premium SpinnerDots).",
}

# ---------------------------------------------------------------------------
# Catalog — shared with dlc.Loading (dash_loading_components.registry)
# ---------------------------------------------------------------------------

from dash_loading_components.registry import (
    FAMILIES,
    FAMILY_LOOKUP,
    COMPONENT_LOOKUP,
    supports_relative_speed,
    translate_relative_speed,
)

# Native tempo props replaced by relative ``speed`` on detail controls
TEMPO_NATIVE_PROPS = frozenset(
    {"duration", "speed", "speedMultiplier", "speedPlus", "animationDuration"}
)

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
        "doc": "Extra class names merged onto the spinner root (loading.dev).",
    },
    "sweep": {
        "kind": "enum",
        "options": ["diagonal", "rows", "columns"],
        "labels": {"diagonal": "Diagonal", "rows": "Rows", "columns": "Columns"},
        "default": "diagonal",
        "doc": "Sweep path: diagonal (default), rows, or columns.",
    },
    "direction": {
        "kind": "enum",
        "options": ["out", "in"],
        "labels": {"out": "Out", "in": "In"},
        "default": "out",
        "doc": "Ripple direction: out (default) or in.",
    },
    "origin": {
        "kind": "enum",
        "options": ["center", "bottom"],
        "labels": {"center": "Center", "bottom": "Bottom"},
        "default": "center",
        "doc": "Wave growth origin: center (default) or bottom.",
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
    "still": {
        "kind": "bool",
        "default": False,
        "doc": "Freeze animation while keeping the spinner visible.",
    },
    "reverse": {
        "kind": "bool",
        "default": False,
        "doc": "Reverse animation direction.",
    },
    "dense": {
        "kind": "bool",
        "default": False,
        "doc": "Bolder/compact OrbitProgress animation.",
    },
    "bgOpacity": {
        "kind": "slider",
        "min": 0.0,
        "max": 1.0,
        "step": 0.05,
        "default": 0.1,
        "doc": "Background opacity (0–1).",
    },
    "strokeLength": {
        "kind": "slider",
        "min": 0.05,
        "max": 1.0,
        "step": 0.05,
        "default": 0.15,
        "doc": "Fraction of path that is stroked (0–1).",
    },
    "strokeWidthSecondary": {
        "kind": "slider",
        "min": 1,
        "max": 12,
        "step": 1,
        "default": 2,
        "doc": "Secondary stroke width (Oval background).",
    },
    "barCount": {
        "kind": "slider",
        "min": 2,
        "max": 12,
        "step": 1,
        "default": 5,
        "doc": "Number of bars.",
    },
    "dotCount": {
        "kind": "slider",
        "min": 2,
        "max": 8,
        "step": 1,
        "default": 3,
        "doc": "Number of dots.",
    },
    "dotSize": {
        "kind": "slider",
        "min": 2,
        "max": 24,
        "step": 1,
        "default": 8,
        "doc": "Dot diameter in pixels.",
    },
    "ringCount": {
        "kind": "slider",
        "min": 1,
        "max": 8,
        "step": 1,
        "default": 3,
        "doc": "Number of concentric rings (OrbitRings).",
    },
    "ringGap": {
        "kind": "slider",
        "min": 0,
        "max": 24,
        "step": 1,
        "default": 6,
        "doc": "Gap between rings in px (OrbitRings).",
    },
    "alternate": {
        "kind": "bool",
        "default": True,
        "doc": "Alternate ring rotation directions (OrbitRings).",
    },
    "orbitRadius": {
        "kind": "slider",
        "min": 0.2,
        "max": 1.0,
        "step": 0.05,
        "default": 0.5,
        "doc": "Orbit radius relative to size (OrbitDots).",
    },
    "stagger": {
        "kind": "bool",
        "default": True,
        "doc": "Stagger animation between dots (OrbitDots).",
    },
}

# Relative speed for the common Loading path (1.0 = this spinner's normal).
# Native units appear only in the Namespaced snippet after translation.
RELATIVE_SPEED_SPEC: dict[str, Any] = {
    "kind": "slider",
    "min": 0.5,
    "max": 3.0,
    "step": 0.1,
    "default": 1.0,
    "doc": (
        "Relative rate: 1.0 = this spinner's normal tempo. "
        "Translated to native units in the Namespaced snippet "
        "(fixes the old shared-unit footgun)."
    ),
}


INDICATORS_EASING_SPEC: dict[str, Any] = {
    "kind": "dropdown",
    "options": ["linear", "ease-in", "ease-out", "ease-in-out"],
    "default": "ease-in-out",
    "doc": "CSS animation easing (react-loading-indicators).",
}

INDICATORS_VARIANT = {
    "OrbitProgress": {
        "kind": "dropdown",
        "options": ["disc", "dotted", "spokes", "split-disc", "track-disc"],
        "default": "disc",
        "doc": "OrbitProgress variant.",
    },
    "ThreeDot": {
        "kind": "dropdown",
        "options": ["pulsate", "bob", "brick-stack", "bounce"],
        "default": "pulsate",
        "doc": "ThreeDot variant.",
    },
}

LOADER_SPINNER_ANIM_DURATION_SPEC: dict[str, Any] = {
    "kind": "slider",
    "min": 0.2,
    "max": 3.0,
    "step": 0.1,
    "default": 1.0,
    "doc": "Oval rotation duration in seconds (react-loader-spinner).",
}


PREMIUM_THICKNESS_SPEC = {
    "kind": "slider",
    "min": 1,
    "max": 12,
    "step": 1,
    "default": 2,
    "doc": "Stroke / ring thickness in px (premium-react-loaders).",
}


def prop_spec(family: str, prop: str, name: str | None = None) -> dict[str, Any] | None:
    """Resolve control/default metadata; relative speed for Loading path."""
    if prop == "speed" and supports_relative_speed(family):
        return RELATIVE_SPEED_SPEC
    if prop == "easing" and family == "indicators":
        return INDICATORS_EASING_SPEC
    if prop == "variant" and family == "indicators" and name in INDICATORS_VARIANT:
        return INDICATORS_VARIANT[name]
    if prop == "animationDuration" and family == "loader_spinner":
        return LOADER_SPINNER_ANIM_DURATION_SPEC
    if prop == "thickness" and family == "premium":
        return PREMIUM_THICKNESS_SPEC
    return PROP_SPECS.get(prop)


# Preferred control order per family (props not listed still appear after)
FAMILY_PROP_ORDER = {
    "loading_dev": [
        "size", "color", "duration", "playState", "easing", "cap",
        "sweep", "direction", "origin", "className",
    ],
    "ldrs": ["size", "color", "speed", "stroke", "strokeLength", "bgOpacity", "className"],
    "spinners": [
        "size", "color", "speedMultiplier", "margin", "loading", "height", "width", "radius", "barCount", "className"
    ],
    "spinners_react": [
        "size", "color", "speed", "thickness", "secondaryColor", "enabled", "still", "className"
    ],
    "loader_spinner": [
        "height", "width", "color", "secondaryColor", "strokeWidth", "strokeWidthSecondary",
        "animationDuration", "radius", "visible", "ariaLabel", "className",
    ],
    "premium": ["size", "color", "speed", "secondaryColor", "thickness", "reverse", "visible", "dotCount", "dotSize", "barCount", "ringCount", "ringGap", "alternate", "orbitRadius", "stagger", "className"],
    "indicators": [
        "size", "color", "speedPlus", "easing", "text", "textColor", "variant", "dense", "className"
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
    """Return Dash-exposed props that make sense as controls.

    For families with speed translation, native tempo props are replaced by
    a single relative ``speed`` control (common Loading path).
    """
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

    if supports_relative_speed(family):
        props = [p for p in props if p not in TEMPO_NATIVE_PROPS]
        if "speed" not in props:
            props.append("speed")

    order = FAMILY_PROP_ORDER.get(family, [])
    # Prefer relative speed where FAMILY_PROP_ORDER listed a native tempo name
    order_norm = []
    seen_speed = False
    for p in order:
        if p in TEMPO_NATIVE_PROPS and supports_relative_speed(family):
            if not seen_speed:
                order_norm.append("speed")
                seen_speed = True
            continue
        order_norm.append(p)
    ordered = [p for p in order_norm if p in props]
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
        if family == "premium" and p == "secondaryColor":
            # omit — light default washes out alternating OrbitRings on white
            continue
        spec = prop_spec(family, p, name)
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
    if isinstance(v, float):
        # Keep relative speed readable as 1.0 (not 1)
        if v == int(v):
            return f"{v:.1f}"
        return repr(v)
    return repr(v)


def _omit_empty_strings(values: dict[str, Any]) -> dict[str, Any]:
    out = {}
    for k, v in values.items():
        if v is None:
            continue
        if isinstance(v, str) and v == "" and k in ("className", "text", "ariaLabel"):
            continue
        out[k] = v
    return out


def build_namespaced_values(
    family: str, name: str, values: dict[str, Any]
) -> dict[str, Any]:
    """Control values → native prop dict (relative speed translated)."""
    native = dict(values)
    if supports_relative_speed(family) and "speed" in native:
        rel = native.pop("speed")
        native.update(translate_relative_speed(family, rel, name))
    return _omit_empty_strings(native)


def format_python_snippet(source: str) -> str:
    """Format displayed Python with Black without making the gallery fragile."""
    if black is None:
        logger.warning("Black is unavailable; displaying an unformatted snippet")
        return source
    try:
        return black.format_str(source, mode=black.Mode(line_length=88))
    except Exception:
        logger.warning("Black failed to format gallery snippet; using raw source", exc_info=True)
        return source


def build_snippet(family: str, name: str, values: dict[str, Any]) -> str:
    """Namespaced snippet with native prop names/units."""
    parts = []
    for k, v in values.items():
        parts.append(f"{k}={format_py_value(v)}")
    call = f"dlc.{family}.{name}({', '.join(parts)})"
    return format_python_snippet(f"import dash_loading_components as dlc\n\n{call}\n")


def _derive_playing(family: str, values: dict[str, Any]) -> bool:
    if "playState" in values:
        return values["playState"] != "paused"
    if "paused" in values:
        return not bool(values["paused"])
    if "loading" in values:
        return bool(values["loading"])
    if "enabled" in values:
        return bool(values["enabled"])
    if "visible" in values:
        return bool(values["visible"])
    return True


# Props Loading maps itself — strip from common extras
_LOADING_MANAGED = frozenset(
    {
        "speed",
        "duration",
        "speedMultiplier",
        "speedPlus",
        "animationDuration",
        "playState",
        "paused",
        "loading",
        "enabled",
        "visible",
        "size",
        "color",
        "className",
        "class_name",
    }
)


def build_common_snippet(family: str, name: str, values: dict[str, Any]) -> str:
    """Common API snippet: dlc.Loading(..., speed=relative, ...)."""
    parts = [f'library="{family}"', f'spinner="{name}"']
    cleaned = _omit_empty_strings(values)
    # Ordered common surface first
    for key in ("size", "color", "speed", "class_name"):
        if key == "speed" and not supports_relative_speed(family):
            continue
        # Control store still uses React className; Common snippet is snake_case
        src_key = "className" if key == "class_name" else key
        if src_key in cleaned:
            parts.append(f"{key}={format_py_value(cleaned[src_key])}")
        elif key == "speed" and supports_relative_speed(family):
            parts.append("speed=1.0")
    playing = _derive_playing(family, cleaned)
    if not playing:
        parts.append("playing=False")
    # Exotic passthrough (easing, cap, thickness, …)
    for k, v in cleaned.items():
        if k in _LOADING_MANAGED:
            continue
        parts.append(f"{k}={format_py_value(v)}")
    call = f"dlc.Loading({', '.join(parts)})"
    return format_python_snippet(f"import dash_loading_components as dlc\n\n{call}\n")


def instantiate(family: str, name: str, values: dict[str, Any]):
    """Live preview via dlc.Loading (relative speed translated inside)."""
    cleaned = _omit_empty_strings(values)
    extras = {k: v for k, v in cleaned.items() if k not in _LOADING_MANAGED}
    kwargs: dict[str, Any] = {}
    if "size" in cleaned:
        kwargs["size"] = cleaned["size"]
    if "color" in cleaned:
        kwargs["color"] = cleaned["color"]
    if "className" in cleaned:
        kwargs["class_name"] = cleaned["className"]
    if supports_relative_speed(family):
        kwargs["speed"] = cleaned.get("speed", 1.0)
    kwargs["playing"] = _derive_playing(family, cleaned)
    kwargs.update(extras)
    try:
        return dlc.Loading(library=family, spinner=name, **kwargs)
    except Exception as exc:
        return html.Div(f"error: {exc}", style={"color": "crimson", "fontSize": 13})


# Loaders whose animation sweeps well past its own box. Shrinking `size`
# either does not help (react-loading-indicators takes size tokens, not
# pixels) or leaves the loader too small to read, so scale the whole preview
# down instead: same proportions, just fitted to the card slot. Values are
# the measured ink extent over a full cycle divided by the slot width; the
# clipping test in tests/test_gallery_overview.py keeps them honest.
OVERVIEW_SCALE: dict[tuple[str, str], float] = {
    ("spinners", "PropagateLoader"): 0.56,
    ("indicators", "LifeLine"): 0.68,
    ("indicators", "BlinkBlur"): 0.8,
}


def overview_preview_kwargs(family: str, name: str | None = None) -> dict[str, Any]:
    """Preview props for overview cards.

    Prefer sizes that fit the ~124px-wide card slot. Wide intrinsic loaders
    (epic hollow-dots, large grids) use a smaller overview size; expanding
    animations are additionally clipped by `.preview { overflow: hidden }`.
    """
    if family == "loader_spinner":
        return {"height": DEFAULT_SIZE, "width": DEFAULT_SIZE, "color": DEFAULT_COLOR}
    if family == "indicators":
        # "small" keeps LifeLine / BlinkBlur closer to the card width
        return {"size": "small", "color": DEFAULT_COLOR}
    if family == "epic":
        # HollowDotsSpinner is ~6× size wide; size 20 ≈ 120px fits the card
        return {"size": 20, "color": DEFAULT_COLOR}
    if family == "spinners" and name in ("GridLoader", "MoonLoader", "PropagateLoader"):
        return {"size": 36, "color": DEFAULT_COLOR}
    if family == "spinners" and name == "BarLoader":
        return {"height": 4, "width": 100, "color": DEFAULT_COLOR}
    if family == "premium" and name == "ShimmerBox":
        # Mapped by wrapper to width=2*size, height=size → 80×40
        return {"size": 40, "color": "#e2e8f0"}
    if family == "premium" and name == "OrbitRings":
        return {"size": 40, "color": DEFAULT_COLOR}
    return {"size": DEFAULT_SIZE, "color": DEFAULT_COLOR}


# ---------------------------------------------------------------------------
# Styles
# ---------------------------------------------------------------------------

# Styles live in assets/gallery.css (auto-served by Dash)


# ---------------------------------------------------------------------------
# Layout builders
# ---------------------------------------------------------------------------

def build_site_footer() -> html.Footer:
    """dash-upset-style branding footer (overview + detail + credits)."""
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
                        "Plotly Dash",
                        href="https://dash.plotly.com",
                        target="_blank",
                        rel="noopener noreferrer",
                    ),
                    html.Span(" / "),
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
                    html.Span(" · "),
                    dcc.Link("Credits", href="/credits"),
                ],
                className="dlc-site-footer-brand",
            ),
            html.P(
                "svg_spinners gated (React ^18.2 peer). Gallery preview — package in development.",
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
        [
            html.A(
                "GitHub",
                href="https://github.com/PhylaTech/dash-loading-components",
                target="_blank",
                rel="noopener noreferrer",
                className="dlc-nav-github",
            ),
            dcc.Link("Credits & Licenses", href="/credits", className="dlc-nav-credits"),
        ],
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
    kwargs = overview_preview_kwargs(family, name)
    try:
        node = component(**kwargs)
    except Exception as exc:
        node = html.Div("err", title=str(exc), style={"color": "crimson", "fontSize": 11})
    scale = OVERVIEW_SCALE.get((family, name))
    if scale is not None:
        node = html.Div(node, style={"transform": f"scale({scale})"})
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
                    html.P(
                        f"{len(items)} component" + ("" if len(items) == 1 else "s"),
                        className="meta",
                    ),
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
                        format_python_snippet(
                            "import dash_loading_components as dlc\n\n"
                            'dlc.Loading(library="loading_dev", spinner="Dual", '
                            'size=48, color="#f97316", speed=1.0)\n'
                            "# or namespaced: dlc.loading_dev.Dual(...)"
                        ),
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


def uses_size_presets(family: str, props: list[str]) -> bool:
    """Prefer Small/Medium/Large presets when size is a numeric px prop."""
    if "size" not in props:
        return False
    if family in ("indicators", "loader_spinner"):
        return False
    return True


def section_title(prop: str) -> str:
    return PROP_SECTION_TITLES.get(prop, prop)


def section_copy(family: str, prop: str, name: str | None = None) -> str:
    if family == "indicators" and prop == "size":
        return "Size token: small, medium, or large (upstream string tokens)."
    if family == "indicators" and prop == "easing":
        return "CSS animation easing function (react-loading-indicators)."
    if prop in PROP_SECTION_COPY and not (family == "indicators" and prop == "easing"):
        return PROP_SECTION_COPY[prop]
    spec = prop_spec(family, prop, name)
    if spec and spec.get("doc"):
        return spec["doc"]
    return f"Configurable `{prop}` for this wrapper."


def build_prop_example_snippet(family: str, name: str, prop: str) -> str:
    """Short namespaced examples for the prop docs section (not live-synced)."""
    lines = ["import dash_loading_components as dlc", ""]
    if prop == "size" and family != "indicators":
        for label, px in SIZE_PRESETS:
            lines.append(f"dlc.{family}.{name}(size={px})  # {label}")
    elif family == "indicators" and prop == "size":
        for tok in ("small", "medium", "large"):
            lines.append(f'dlc.{family}.{name}(size="{tok}")')
    elif prop == "color":
        lines.append(f'dlc.{family}.{name}(color="#f97316", size={DEFAULT_SIZE})')
    elif prop == "speed" and supports_relative_speed(family):
        lines.append(
            f'dlc.Loading(library="{family}", spinner="{name}", '
            f"size={DEFAULT_SIZE}, speed=1.5)"
        )
        native = translate_relative_speed(family, 1.5, name)
        kw = ", ".join(f"{k}={format_py_value(v)}" for k, v in native.items())
        lines.append(f"# namespaced ≈ dlc.{family}.{name}({kw})")
    elif prop == "easing":
        lines.append(f'dlc.{family}.{name}(easing="ease-in-out", size={DEFAULT_SIZE})')
    elif prop == "cap":
        lines.append(f'dlc.{family}.{name}(cap="flat", size={DEFAULT_SIZE})')
    elif prop == "playState":
        lines.append(f'dlc.{family}.{name}(playState="paused", size={DEFAULT_SIZE})')
    elif prop == "sweep":
        for opt in ("diagonal", "rows", "columns"):
            lines.append(
                f'dlc.{family}.{name}(sweep="{opt}", size={DEFAULT_SIZE})'
            )
    elif prop == "direction":
        for opt in ("out", "in"):
            lines.append(
                f'dlc.{family}.{name}(direction="{opt}", size={DEFAULT_SIZE})'
            )
    elif prop == "origin":
        for opt in ("center", "bottom"):
            lines.append(
                f'dlc.{family}.{name}(origin="{opt}", size={DEFAULT_SIZE})'
            )
    elif prop == "className":
        lines.append(f'dlc.{family}.{name}(className="opacity-40", size={DEFAULT_SIZE})')
    else:
        spec = prop_spec(family, prop, name)
        demo = spec["default"] if spec else None
        if demo is None:
            lines.append(f"dlc.{family}.{name}(...)  # set {prop}=...")
        else:
            lines.append(
                f"dlc.{family}.{name}({prop}={format_py_value(demo)}, size={DEFAULT_SIZE})"
            )
    return format_python_snippet("\n".join(lines) + "\n")


def workbench_control(prop: str, value: Any, family: str, props: list[str], name: str | None = None) -> html.Div:
    """Compact control row for the workbench panel (beside preview)."""
    label = section_title(prop)
    ctrl_id = {"type": "prop-ctrl", "prop": prop}

    # indicators size tokens
    if family == "indicators" and prop == "size":
        return html.Div(
            [
                html.Label(label, className="dlc-ctrl-label"),
                dcc.RadioItems(
                    id=ctrl_id,
                    options=[
                        {"label": "Small", "value": "small"},
                        {"label": "Medium", "value": "medium"},
                        {"label": "Large", "value": "large"},
                    ],
                    value=value if value in ("small", "medium", "large") else "medium",
                    inline=True,
                    className="dlc-size-presets",
                ),
            ],
            className="dlc-ctrl-row",
        )

    # numeric size → presets
    if prop == "size" and uses_size_presets(family, props):
        preset_val = value if value in SIZE_PRESET_VALUES else SIZE_PRESET_DEFAULT
        return html.Div(
            [
                html.Label(label, className="dlc-ctrl-label"),
                dcc.RadioItems(
                    id=ctrl_id,
                    options=[{"label": lab, "value": px} for lab, px in SIZE_PRESETS],
                    value=preset_val,
                    inline=True,
                    className="dlc-size-presets",
                ),
            ],
            className="dlc-ctrl-row",
        )

    spec = prop_spec(family, prop, name)
    kids: list = [html.Label(label, className="dlc-ctrl-label")]

    if spec is None:
        kids.append(
            dcc.Input(
                id=ctrl_id,
                type="text",
                value="" if value is None else str(value),
                className="dlc-ctrl-input",
            )
        )
        return html.Div(kids, className="dlc-ctrl-row")

    kind = spec["kind"]
    if kind == "slider":
        kids.append(
            dcc.Slider(
                id=ctrl_id,
                min=spec["min"],
                max=spec["max"],
                step=spec["step"],
                value=value if value is not None else spec["default"],
                marks=None,
                tooltip={"placement": "bottom", "always_visible": True},
                className="dlc-ctrl-slider",
            )
        )
    elif kind == "color":
        kids.append(
            dcc.Input(
                id=ctrl_id,
                type="color",
                value=value or spec["default"],
                className="dlc-ctrl-color",
            )
        )
    elif kind == "enum":
        opts = spec["options"]
        labels = spec.get("labels") or {o: o for o in opts}
        kids.append(
            dcc.RadioItems(
                id=ctrl_id,
                options=[{"label": labels.get(o, o), "value": o} for o in opts],
                value=value if value in opts else spec["default"],
                inline=True,
                className="dlc-size-presets",
            )
        )
    elif kind == "dropdown":
        kids.append(
            dcc.Dropdown(
                id=ctrl_id,
                options=[{"label": o, "value": o} for o in spec["options"]],
                value=value if value in spec["options"] else spec["default"],
                clearable=False,
                className="dlc-ctrl-dropdown",
            )
        )
    elif kind == "bool":
        kids.append(
            dcc.Checklist(
                id=ctrl_id,
                options=[{"label": f" {label}", "value": "on"}],
                value=["on"] if (True if value is None else bool(value)) else [],
                className="dlc-ctrl-check",
            )
        )
    elif kind == "text":
        kids.append(
            dcc.Input(
                id=ctrl_id,
                type="text",
                value="" if value is None else str(value),
                placeholder=prop,
                className="dlc-ctrl-input",
            )
        )
    else:
        kids.append(html.Div(f"unsupported kind {kind}"))

    return html.Div(kids, className="dlc-ctrl-row")


def build_prop_doc_section(family: str, name: str, prop: str) -> html.Section:
    title = section_title(prop)
    return html.Section(
        [
            html.H2(title),
            html.P(section_copy(family, prop, name), className="dlc-prop-doc-copy"),
            html.Pre(
                build_prop_example_snippet(family, name, prop),
                className="dlc-snippet dlc-snippet-doc",
            ),
        ],
        id=f"section-{prop}",
        className="dlc-prop-doc",
    )


def build_detail_toc(props: list[str]) -> html.Aside:
    links = [html.A("Preview", href="#section-preview", className="dlc-toc-link")]
    for p in props:
        if p == "className":
            # still document, keep in TOC
            pass
        links.append(
            html.A(section_title(p), href=f"#section-{p}", className="dlc-toc-link")
        )
    return html.Aside(
        [html.Div("On this page", className="dlc-toc-heading"), *links],
        className="dlc-toc",
    )


def build_detail(family: str, name: str) -> html.Div:
    upstream = FAMILY_LOOKUP[family][0]
    component = COMPONENT_LOOKUP[(family, name)]
    props = configurable_props(family, name, component)
    values = default_values(family, name, props)
    # Snap default size to Medium preset when using presets
    if uses_size_presets(family, props) and "size" in values:
        values["size"] = SIZE_PRESET_DEFAULT
    desc = description_for(family, name, upstream)

    # Workbench control order
    wb_order = [p for p in WORKBENCH_PROP_PRIORITY if p in props]
    wb_rest = [p for p in props if p not in wb_order]
    wb_props = wb_order + wb_rest

    controls = [workbench_control(p, values.get(p), family, props, name) for p in wb_props]
    if not controls:
        controls = [
            html.Div(
                dcc.Input(id={"type": "prop-ctrl", "prop": "_none"}, type="hidden", value=""),
                style={"display": "none"},
            )
        ]

    control_panel = html.Div(
        [
            html.Div("Controls", className="dlc-workbench-controls-title"),
            html.Div(controls, id="detail-controls", className="dlc-workbench-controls-body"),
            html.Button(
                "Reset to defaults",
                id="detail-reset",
                n_clicks=0,
                type="button",
                className="dlc-reset-btn",
            ),
        ],
        className="dlc-workbench-controls",
    )

    workbench = html.Section(
        [
            html.Div(
                instantiate(family, name, values),
                id="detail-preview",
                className="dlc-preview-panel",
            ),
            control_panel,
        ],
        id="section-preview",
        className="dlc-workbench",
    )

    snippets = html.Div(
        [
            html.Div(
                [
                    html.Div("Common API", className="dlc-snippet-label"),
                    html.Pre(
                        build_common_snippet(family, name, values),
                        id="detail-snippet-common",
                        className="dlc-snippet",
                    ),
                ],
                className="dlc-snippet-block",
            ),
            html.Div(
                [
                    html.Div("Namespaced", className="dlc-snippet-label"),
                    html.Pre(
                        build_snippet(
                            family,
                            name,
                            build_namespaced_values(family, name, values),
                        ),
                        id="detail-snippet-namespaced",
                        className="dlc-snippet",
                    ),
                ],
                className="dlc-snippet-block",
            ),
        ],
        className="dlc-snippets-row",
    )

    prop_docs = [build_prop_doc_section(family, name, p) for p in props]

    content = html.Div(
        [
            dcc.Store(id="detail-meta", data={"family": family, "name": name, "props": props}),
            dcc.Store(id="detail-values", data=values),
            html.Div(
                [
                    html.Span("Component", className="dlc-detail-kicker"),
                    html.Span(" / ", className="dlc-detail-sep"),
                    html.Span(name, className="dlc-detail-name"),
                ],
                className="dlc-detail-breadcrumb",
            ),
            html.H1(name, className="dlc-detail-title"),
            html.P(desc, className="dlc-detail-desc"),
            workbench,
            snippets,
            *prop_docs,
            build_site_footer(),
        ],
        className="dlc-detail-content",
    )

    return html.Div(
        [
            content,
            build_detail_toc(props),
        ],
        className="dlc-main dlc-detail-page",
    )


UPSTREAM_CREDITS = [
    {
        "family": "loading_dev",
        "npm": "loading-dev",
        "version": "0.3.4",
        "spdx": "MIT",
        "homepage": "https://loading.dev/",
        "repo": "https://github.com/jakubkrehel/loading",
        "note": "Product tent-pole; drives React 19 / Dash ≥4.5 floor.",
        "status": "mvp",
    },
    {
        "family": "ldrs",
        "npm": "ldrs",
        "version": "1.1.9",
        "spdx": "MIT",
        "homepage": "https://uiball.com/ldrs/",
        "repo": "https://github.com/GriffinJohnston/ldrs",
        "note": "Beautiful CSS-animated loaders by UI Ball.",
        "status": "mvp",
    },
    {
        "family": "spinners",
        "npm": "react-spinners",
        "version": "0.17.1",
        "spdx": "MIT",
        "homepage": "https://www.npmjs.com/package/react-spinners",
        "repo": "https://github.com/davidhu2000/react-spinners",
        "note": "Classic spinner zoo; also used by dash-loading-spinners.",
        "status": "mvp",
    },
    {
        "family": "spinners_react",
        "npm": "spinners-react",
        "version": "1.0.11",
        "spdx": "MIT",
        "homepage": "https://www.npmjs.com/package/spinners-react",
        "repo": "https://github.com/adexin/spinners-react",
        "note": "Lightweight SVG spinners with speed/thickness controls.",
        "status": "mvp",
    },
    {
        "family": "loader_spinner",
        "npm": "react-loader-spinner",
        "version": "8.0.2",
        "spdx": "MIT",
        "homepage": "https://www.npmjs.com/package/react-loader-spinner",
        "repo": "https://github.com/mhnpd/react-loader-spinner",
        "note": "Diverse loader set with height/width/radius controls.",
        "status": "mvp",
    },
    {
        "family": "premium",
        "npm": "premium-react-loaders",
        "version": "4.2.0",
        "spdx": "MIT",
        "homepage": "https://www.npmjs.com/package/premium-react-loaders",
        "repo": None,
        "note": "Premium-quality orbit, dot, and bar loaders.",
        "status": "mvp",
    },
    {
        "family": "indicators",
        "npm": "react-loading-indicators",
        "version": "1.0.1",
        "spdx": "MIT",
        "homepage": "https://www.npmjs.com/package/react-loading-indicators",
        "repo": None,
        "note": "Size-token indicators with variant/easing support.",
        "status": "mvp",
    },
    {
        "family": "m3",
        "npm": "@alerix/m3-loading-indicator",
        "version": "1.0.5",
        "spdx": "Apache-2.0",
        "homepage": "https://www.npmjs.com/package/@alerix/m3-loading-indicator",
        "repo": None,
        "note": "Material Design 3 circular indicator. Apache-2.0 license.",
        "status": "mvp",
    },
    {
        "family": "epic",
        "npm": "react-epic-spinners",
        "version": "0.6.0",
        "spdx": "MIT",
        "homepage": "https://www.npmjs.com/package/react-epic-spinners",
        "repo": "https://github.com/bondz/react-epic-spinners",
        "note": "Ported from epic-spinners (Vue) to React.",
        "status": "mvp",
    },
    {
        "family": "svg_spinners",
        "npm": "react-svg-spinners",
        "version": "0.3.1",
        "spdx": "MIT",
        "homepage": "https://www.npmjs.com/package/react-svg-spinners",
        "repo": "https://github.com/theme-park/react-svg-spinners",
        "note": "Gated — React ^18.2 peer dependency not yet resolved for React 19.",
        "status": "gated",
    },
]


def _credits_badge(spdx: str) -> html.Span:
    cls = "dlc-credits-badge "
    if spdx == "MIT":
        cls += "dlc-credits-badge-mit"
    elif spdx.startswith("Apache"):
        cls += "dlc-credits-badge-apache"
    else:
        cls += "dlc-credits-badge-gated"
    return html.Span(spdx, className=cls)


def _credits_links(entry: dict) -> list:
    links = [
        html.A("npm", href=f"https://www.npmjs.com/package/{entry['npm']}", target="_blank", rel="noopener noreferrer"),
    ]
    if entry.get("homepage") and "npmjs.com" not in entry["homepage"]:
        links.append(html.Span(" · "))
        links.append(html.A("homepage", href=entry["homepage"], target="_blank", rel="noopener noreferrer"))
    if entry.get("repo"):
        links.append(html.Span(" · "))
        links.append(html.A("repo", href=entry["repo"], target="_blank", rel="noopener noreferrer"))
    return links


def build_credits() -> html.Div:
    rows = []
    for entry in UPSTREAM_CREDITS:
        status_suffix = ""
        if entry["status"] == "gated":
            status_suffix = " (gated)"
        rows.append(
            html.Tr([
                html.Td([html.Code(f"dlc.{entry['family']}"), html.Span(status_suffix, style={"color": "var(--muted)", "fontSize": "11px"})]),
                html.Td([html.Code(entry["npm"]), html.Span(f" {entry['version']}", style={"color": "var(--muted)"})]),
                html.Td(_credits_badge(entry["spdx"])),
                html.Td(_credits_links(entry)),
                html.Td(entry["note"]),
            ])
        )

    table = html.Table(
        [
            html.Thead(html.Tr([
                html.Th("dlc namespace"),
                html.Th("Upstream package"),
                html.Th("License"),
                html.Th("Links"),
                html.Th("Notes"),
            ])),
            html.Tbody(rows),
        ],
        className="dlc-credits-table",
    )

    return html.Div(
        [
            html.H1("Credits & Licenses", style={"fontSize": "28px", "margin": "0 0 8px", "letterSpacing": "-0.03em"}),
            html.P(
                [
                    html.Strong("dash-loading-components"),
                    html.Span(" is licensed under the "),
                    html.A("MIT License", href="https://github.com/PhylaTech/dash-loading-components/blob/main/LICENSE", target="_blank", rel="noopener noreferrer"),
                    html.Span(
                        " and wraps third-party React loading-indicator libraries, "
                        "redistributed under their own licenses. "
                        "Full inventory is maintained in "
                    ),
                    html.A("docs/UPSTREAM-INVENTORY.md", href="https://github.com/PhylaTech/dash-loading-components/blob/main/docs/UPSTREAM-INVENTORY.md", target="_blank", rel="noopener noreferrer"),
                    html.Span(" and the root "),
                    html.A("NOTICE", href="https://github.com/PhylaTech/dash-loading-components/blob/main/NOTICE", target="_blank", rel="noopener noreferrer"),
                    html.Span(" file."),
                ],
                className="dlc-credits-intro",
            ),
            html.H2("Day-one upstream families", style={"fontSize": "20px", "margin": "0 0 14px"}),
            table,
            html.Div(
                [
                    html.H2("Hard skips"),
                    html.P(
                        "css-spinners (GPL-3.0) and react18-loaders (MPL-2.0) are not wrapped "
                        "due to license incompatibility with MIT distribution."
                    ),
                ],
                className="dlc-credits-skip",
            ),
            html.P(
                [
                    html.Span("Copyright © 2026 Evan Roy Rees / "),
                    html.A("Phyla Technologies", href="https://github.com/PhylaTech", target="_blank", rel="noopener noreferrer"),
                ],
                className="dlc-credits-note",
                style={"marginTop": "24px"},
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

_OG_IMAGE = "https://dash-loading-components.phylatech.com/assets/og-card.png"
_OG_DESCRIPTION = (
    "Interactive gallery of Dash loading spinners \u2014 wrappers for "
    "loading.dev, ldrs, react-spinners, and more. Built by PhylaTech."
)

app = Dash(
    __name__,
    suppress_callback_exceptions=True,
    meta_tags=[
        {"name": "description", "content": _OG_DESCRIPTION},
        {"property": "og:title", "content": "dash-loading-components"},
        {"property": "og:description", "content": _OG_DESCRIPTION},
        {"property": "og:type", "content": "website"},
        {"property": "og:url", "content": "https://dash-loading-components.phylatech.com/"},
        {"property": "og:site_name", "content": "PhylaTech"},
        {"property": "og:image", "content": _OG_IMAGE},
        {"property": "og:image:alt", "content": "dash-loading-components — Interactive Dash loading spinner gallery"},
        {"name": "twitter:card", "content": "summary_large_image"},
        {"name": "twitter:title", "content": "dash-loading-components"},
        {"name": "twitter:description", "content": _OG_DESCRIPTION},
        {"name": "twitter:image", "content": _OG_IMAGE},
    ],
)
app.title = "dash-loading-components \u00b7 gallery"

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
    if mode == "credits":
        return page_shell(build_sidenav(), build_credits())
    return page_shell(build_sidenav(), build_404())


def _coerce_control_value(prop: str, raw: Any, family: str, name: str | None = None) -> Any:
    if prop == "_none":
        return None
    spec = prop_spec(family, prop, name)
    if family == "indicators" and prop == "size":
        return raw
    # Size presets (RadioItems) — keep concrete px ints
    if prop == "size" and family != "indicators" and isinstance(raw, (int, float)):
        return int(raw)
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
    Output({"type": "prop-ctrl", "prop": ALL}, "value"),
    Input("detail-reset", "n_clicks"),
    State({"type": "prop-ctrl", "prop": ALL}, "id"),
    State("detail-meta", "data"),
    prevent_initial_call=True,
)
def reset_detail_controls(n_clicks, ids, meta):
    """Restore workbench controls to gallery defaults."""
    if not n_clicks or not meta:
        return no_update
    family = meta["family"]
    name = meta["name"]
    props = meta.get("props") or []
    defaults = default_values(family, name, props)
    if uses_size_presets(family, props):
        defaults["size"] = SIZE_PRESET_DEFAULT
    out = []
    for id_dict in ids or []:
        prop = id_dict.get("prop")
        if not prop or prop == "_none":
            out.append("")
            continue
        if prop in defaults:
            v = defaults[prop]
        elif prop in ("className", "text", "ariaLabel"):
            v = ""
        else:
            spec = prop_spec(family, prop, name)
            v = spec["default"] if spec else None
        spec = prop_spec(family, prop, name)
        if family == "indicators" and prop == "size":
            out.append(v if v in ("small", "medium", "large") else "medium")
        elif spec and spec["kind"] == "bool":
            out.append(["on"] if v else [])
        else:
            out.append(v)
    return out


@callback(
    Output("detail-preview", "children"),
    Output("detail-snippet-common", "children"),
    Output("detail-snippet-namespaced", "children"),
    Output("detail-values", "data"),
    Input({"type": "prop-ctrl", "prop": ALL}, "value"),
    State({"type": "prop-ctrl", "prop": ALL}, "id"),
    State("detail-meta", "data"),
    prevent_initial_call=True,
)
def update_detail(values, ids, meta):
    if not meta:
        return no_update, no_update, no_update, no_update
    family = meta["family"]
    name = meta["name"]
    props_order = meta.get("props") or []
    collected: dict[str, Any] = {}
    for raw, id_dict in zip(values or [], ids or []):
        prop = id_dict.get("prop")
        if not prop or prop == "_none":
            continue
        collected[prop] = _coerce_control_value(prop, raw, family, name)
    # Preserve order from props_order for snippet stability
    ordered = {p: collected[p] for p in props_order if p in collected}
    for p, v in collected.items():
        if p not in ordered:
            ordered[p] = v
    preview = instantiate(family, name, ordered)
    common = build_common_snippet(family, name, ordered)
    namespaced = build_snippet(
        family, name, build_namespaced_values(family, name, ordered)
    )
    return preview, common, namespaced, ordered


if __name__ == "__main__":
    _port = int(os.environ.get("PORT", "8050"))
    print("dlc gallery — http://127.0.0.1:%d/  (REACT_VERSION=%s)" % (_port, os.environ.get("REACT_VERSION")))
    app.run(host="0.0.0.0", port=_port, debug=False)
