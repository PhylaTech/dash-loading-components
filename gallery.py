"""Local gallery MVP for dash-loading-components.

Run:
  source /workspace/dash-loading/.venv/bin/activate
  cd /workspace/dash-loading/dash-loading-components
  REACT_VERSION=19.2.4 python gallery.py
"""
import os

# React 19 opt-in for Dash 4.5 (must be set before dash imports renderer heavily)
os.environ.setdefault("REACT_VERSION", "19.2.4")

import dash
from dash import Dash, html, dcc, Input, Output, callback

import dash_loading_components as dlc

try:
    dash._dash_renderer._set_react_version("19.2.4")
except Exception as exc:  # pragma: no cover
    print("warn: could not set React version via _set_react_version:", exc)

DEFAULT_COLOR = "#f97316"
DEFAULT_SIZE = 48

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
        "size_color",
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
        "size_color",
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
        "size_color",
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
        "size_color",
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
        "hw_color",
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
        "premium",
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
        "indicators",
    ),
    (
        "m3",
        "@alerix/m3-loading-indicator",
        [("LoadingIndicator", dlc.m3.LoadingIndicator)],
        "m3",
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
        "size_color",
    ),
]


def make_card(name, component, mode, size, color):
    kwargs = {}
    try:
        if mode == "size_color":
            kwargs = {"size": size, "color": color}
        elif mode == "hw_color":
            kwargs = {"height": size, "width": size, "color": color}
        elif mode == "premium":
            kwargs = {"size": size, "color": color}
        elif mode == "indicators":
            # indicators use small/medium/large strings often; pass numeric when possible
            kwargs = {"size": "medium", "color": color}
        elif mode == "m3":
            kwargs = {"size": size, "color": color}
        node = component(**kwargs)
    except Exception as exc:
        node = html.Div(f"error: {exc}", style={"color": "crimson", "fontSize": 12})
    return html.Div(
        [
            html.Div(name, style={"fontSize": 12, "marginBottom": 8, "opacity": 0.75}),
            html.Div(
                node,
                style={
                    "display": "flex",
                    "alignItems": "center",
                    "justifyContent": "center",
                    "minHeight": 72,
                },
            ),
        ],
        style={
            "border": "1px solid #e5e7eb",
            "borderRadius": 8,
            "padding": 12,
            "background": "#fff",
            "minWidth": 140,
        },
        className="dlc-gallery-card",
    )


def family_section(key, label, items, mode, size, color):
    return html.Div(
        [
            html.H2(f"dlc.{key}", style={"margin": "0 0 4px"}),
            html.P(
                f"Upstream: {label} · {len(items)} components",
                style={"marginTop": 0, "opacity": 0.7},
            ),
            html.Div(
                [make_card(n, c, mode, size, color) for n, c in items],
                style={
                    "display": "grid",
                    "gridTemplateColumns": "repeat(auto-fill, minmax(150px, 1fr))",
                    "gap": 12,
                },
            ),
        ],
        style={"padding": "8px 0 24px"},
        id=f"family-{key}",
        className=f"dlc-family dlc-family-{key}",
    )


app = Dash(__name__, title="dlc gallery MVP")
server = app.server

app.layout = html.Div(
    [
        html.H1("dash-loading-components gallery"),
        html.P(
            [
                "Dash 4.5 + React 19 local MVP. Import style: ",
                html.Code("import dash_loading_components as dlc"),
                " → ",
                html.Code("dlc.loading_dev.Arc(...)"),
                " (also prefixed: ",
                html.Code("dlc.LoadingDevArc"),
                ").",
            ]
        ),
        html.Div(
            [
                html.Label("Size"),
                dcc.Slider(
                    id="size",
                    min=16,
                    max=96,
                    step=4,
                    value=DEFAULT_SIZE,
                    marks={16: "16", 48: "48", 96: "96"},
                ),
                html.Label("Color"),
                dcc.Input(id="color", type="text", value=DEFAULT_COLOR, debounce=True),
            ],
            style={"maxWidth": 480, "marginBottom": 16},
        ),
        dcc.Tabs(
            id="tabs",
            value=FAMILIES[0][0],
            children=[
                dcc.Tab(label=f"{key} ({len(items)})", value=key)
                for key, _label, items, _mode in FAMILIES
            ],
        ),
        html.Div(id="tab-body"),
        html.Hr(),
        html.P(
            "svg_spinners gated (React 19 peer). No push/PR from this MVP.",
            style={"opacity": 0.6, "fontSize": 12},
        ),
    ],
    style={
        "fontFamily": "system-ui, sans-serif",
        "padding": 24,
        "maxWidth": 1100,
        "margin": "0 auto",
        "background": "#f8fafc",
        "minHeight": "100vh",
    },
)


@callback(Output("tab-body", "children"), Input("tabs", "value"), Input("size", "value"), Input("color", "value"))
def render_tab(tab, size, color):
    size = size or DEFAULT_SIZE
    color = color or DEFAULT_COLOR
    for key, label, items, mode in FAMILIES:
        if key == tab:
            return family_section(key, label, items, mode, size, color)
    return html.Div("Unknown family")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8050"))
    print(f"Starting gallery on 0.0.0.0:{port} (REACT_VERSION={os.environ.get('REACT_VERSION')})")
    app.run(host="0.0.0.0", port=port, debug=False)
