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

# Relative speed for the common Loading path (1.0 = family normal).
# Native units appear only in the Namespaced snippet after translation.
RELATIVE_SPEED_SPEC: dict[str, Any] = {
    "kind": "slider",
    "min": 0.5,
    "max": 3.0,
    "step": 0.1,
    "default": 1.0,
    "doc": (
        "Relative rate: 1.0 = this family's normal tempo. "
        "Translated to native units in the Namespaced snippet "
        "(fixes the old shared-unit footgun)."
    ),
}


def prop_spec(family: str, prop: str) -> dict[str, Any] | None:
    """Resolve control/default metadata; relative speed for Loading path."""
    if prop == "speed" and supports_relative_speed(family):
        return RELATIVE_SPEED_SPEC
    return PROP_SPECS.get(prop)


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
        spec = prop_spec(family, p)
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


def build_namespaced_values(family: str, values: dict[str, Any]) -> dict[str, Any]:
    """Control values → native prop dict (relative speed translated)."""
    native = dict(values)
    if supports_relative_speed(family) and "speed" in native:
        rel = native.pop("speed")
        native.update(translate_relative_speed(family, rel))
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
    }
)


def build_common_snippet(family: str, name: str, values: dict[str, Any]) -> str:
    """Common API snippet: dlc.Loading(..., speed=relative, ...)."""
    parts = [f'library="{family}"', f'spinner="{name}"']
    cleaned = _omit_empty_strings(values)
    # Ordered common surface first
    for key in ("size", "color", "speed", "className"):
        if key == "speed" and not supports_relative_speed(family):
            continue
        if key in cleaned:
            parts.append(f"{key}={format_py_value(cleaned[key])}")
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
        kwargs["className"] = cleaned["className"]
    if supports_relative_speed(family):
        kwargs["speed"] = cleaned.get("speed", 1.0)
    kwargs["playing"] = _derive_playing(family, cleaned)
    kwargs.update(extras)
    try:
        return dlc.Loading(library=family, spinner=name, **kwargs)
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

    spec = prop_spec(family, prop)
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
                                            build_namespaced_values(family, values),
                                        ),
                                        id="detail-snippet-namespaced",
                                        className="dlc-snippet",
                                    ),
                                ],
                                className="dlc-snippet-block",
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
    spec = prop_spec(family, prop)
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
        collected[prop] = _coerce_control_value(prop, raw, family)
    # Preserve order from props_order for snippet stability
    ordered = {p: collected[p] for p in props_order if p in collected}
    for p, v in collected.items():
        if p not in ordered:
            ordered[p] = v
    preview = instantiate(family, name, ordered)
    common = build_common_snippet(family, name, ordered)
    namespaced = build_snippet(
        family, name, build_namespaced_values(family, ordered)
    )
    return preview, common, namespaced, ordered


if __name__ == "__main__":
    print("dlc gallery — http://127.0.0.1:8050/  (REACT_VERSION=%s)" % os.environ.get("REACT_VERSION"))
    app.run(host="0.0.0.0", port=8050, debug=False)
