"""Local gallery explorer for dash-loading-components.

Single-page component explorer: all upstream families on one scrollable
page, click a card to see the import + call snippet.

Run:
  source /workspace/dash-loading/.venv/bin/activate
  cd /workspace/dash-loading/dash-loading-components
  REACT_VERSION=19.2.4 python gallery.py
"""
import os

# React 19 opt-in for Dash 4.5 (must be set before dash imports renderer heavily)
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

FAMILY_LOOKUP = {key: (label, items, mode) for key, label, items, mode in FAMILIES}

DEFAULT_SELECTION = {"family": "loading_dev", "name": "Arc"}


def component_kwargs(mode, size, color):
    """Return kwargs matching the family's prop mode."""
    size = size or DEFAULT_SIZE
    color = color or DEFAULT_COLOR
    if mode == "size_color":
        return {"size": size, "color": color}
    if mode == "hw_color":
        return {"height": size, "width": size, "color": color}
    if mode == "premium":
        return {"size": size, "color": color}
    if mode == "indicators":
        # Upstream prefers size tokens; global slider does not map 1:1
        return {"size": "medium", "color": color}
    if mode == "m3":
        return {"size": size, "color": color}
    return {}


def format_snippet(family_key, name, mode, size, color):
    kwargs = component_kwargs(mode, size, color)
    parts = []
    for k, v in kwargs.items():
        if isinstance(v, str):
            parts.append(f'{k}="{v}"')
        else:
            parts.append(f"{k}={v}")
    call = f"dlc.{family_key}.{name}({', '.join(parts)})"
    return (
        "import dash_loading_components as dlc\n"
        "\n"
        f"{call}\n"
    )


def make_card(family_key, name, component, mode, size, color, selected):
    kwargs = component_kwargs(mode, size, color)
    try:
        node = component(**kwargs)
    except Exception as exc:
        node = html.Div(f"error: {exc}", style={"color": "crimson", "fontSize": 12})

    is_selected = selected and selected.get("family") == family_key and selected.get("name") == name
    border = "2px solid #f97316" if is_selected else "1px solid #e5e7eb"
    shadow = "0 0 0 3px rgba(249, 115, 22, 0.18)" if is_selected else "none"

    return html.Div(
        [
            html.Div(
                name,
                style={
                    "fontSize": 12,
                    "fontWeight": 600,
                    "marginBottom": 8,
                    "color": "#334155",
                    "letterSpacing": "0.01em",
                },
            ),
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
        id={"type": "dlc-card", "family": family_key, "name": name},
        n_clicks=0,
        role="button",
        tabIndex=0,
        title=f"Show snippet for dlc.{family_key}.{name}",
        style={
            "border": border,
            "boxShadow": shadow,
            "borderRadius": 10,
            "padding": 12,
            "background": "#fff",
            "minWidth": 140,
            "cursor": "pointer",
            "transition": "border-color 0.12s ease, box-shadow 0.12s ease",
            "userSelect": "none",
        },
        className="dlc-gallery-card" + (" is-selected" if is_selected else ""),
    )


def family_section(key, label, items, mode, size, color, selected):
    return html.Section(
        [
            html.Div(
                [
                    html.H2(
                        [
                            html.Code(f"dlc.{key}", style={"fontSize": "1.05em"}),
                            html.Span(
                                f"  ·  {label}",
                                style={"fontWeight": 500, "opacity": 0.7, "fontSize": "0.85em"},
                            ),
                        ],
                        style={"margin": "0 0 2px", "fontSize": 20, "color": "#0f172a"},
                    ),
                    html.P(
                        f"{len(items)} component{'s' if len(items) != 1 else ''}",
                        style={"margin": "0 0 14px", "fontSize": 13, "color": "#64748b"},
                    ),
                ]
            ),
            html.Div(
                [make_card(key, n, c, mode, size, color, selected) for n, c in items],
                style={
                    "display": "grid",
                    "gridTemplateColumns": "repeat(auto-fill, minmax(148px, 1fr))",
                    "gap": 12,
                },
            ),
        ],
        id=f"family-{key}",
        style={
            "padding": "20px 0 28px",
            "borderBottom": "1px solid #e2e8f0",
            "scrollMarginTop": "88px",
        },
        className=f"dlc-family dlc-family-{key}",
    )


def build_gallery(size, color, selected):
    size = size or DEFAULT_SIZE
    color = color or DEFAULT_COLOR
    return [
        family_section(key, label, items, mode, size, color, selected)
        for key, label, items, mode in FAMILIES
    ]


def build_code_panel(selected, size, color):
    size = size or DEFAULT_SIZE
    color = color or DEFAULT_COLOR
    if not selected:
        selected = DEFAULT_SELECTION
    family = selected.get("family")
    name = selected.get("name")
    meta = FAMILY_LOOKUP.get(family)
    if not meta:
        return html.Div("Select a component card.", className="dlc-code-empty")
    label, _items, mode = meta
    snippet = format_snippet(family, name, mode, size, color)
    mode_note = {
        "size_color": "props: size, color",
        "hw_color": "props: height, width, color",
        "premium": "props: size, color",
        "indicators": 'props: size="medium", color (token size)',
        "m3": "props: size, color",
    }.get(mode, mode)

    return html.Div(
        [
            html.Div(
                [
                    html.Span("Snippet", className="dlc-code-label"),
                    html.Span(f"dlc.{family}.{name}", className="dlc-code-target"),
                ],
                className="dlc-code-header",
            ),
            html.Pre(snippet, className="dlc-code-pre", id="code-snippet-text"),
            html.Div(
                [
                    html.Span(f"Upstream: {label}", className="dlc-code-meta"),
                    html.Span(mode_note, className="dlc-code-meta"),
                ],
                className="dlc-code-footer",
            ),
            html.P(
                "Click any card to update. Size & Color controls refresh the snippet when those props apply.",
                className="dlc-code-hint",
            ),
        ],
        className="dlc-code-panel-inner",
    )


def toc_links():
    links = []
    for key, label, items, _mode in FAMILIES:
        links.append(
            html.A(
                [
                    html.Span(key, className="dlc-toc-key"),
                    html.Span(str(len(items)), className="dlc-toc-count"),
                ],
                href=f"#family-{key}",
                className="dlc-toc-link",
                title=f"{label} ({len(items)})",
            )
        )
    return html.Nav(links, className="dlc-toc", **{"aria-label": "Family jump links"})


app = Dash(__name__, title="dlc gallery explorer")
server = app.server

app.index_string = """<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            :root {
                --dlc-bg: #f1f5f9;
                --dlc-surface: #ffffff;
                --dlc-ink: #0f172a;
                --dlc-muted: #64748b;
                --dlc-border: #e2e8f0;
                --dlc-accent: #f97316;
                --dlc-accent-soft: rgba(249, 115, 22, 0.14);
                --dlc-mono: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
            }
            html { scroll-behavior: smooth; }
            body {
                margin: 0;
                background: var(--dlc-bg);
                color: var(--dlc-ink);
                font-family: system-ui, -apple-system, Segoe UI, Roboto, sans-serif;
            }
            .dlc-page {
                max-width: 1280px;
                margin: 0 auto;
                padding: 20px 20px 48px;
            }
            .dlc-hero {
                margin-bottom: 16px;
            }
            .dlc-hero h1 {
                margin: 0 0 6px;
                font-size: 1.55rem;
                letter-spacing: -0.02em;
            }
            .dlc-hero p {
                margin: 0;
                color: var(--dlc-muted);
                font-size: 0.95rem;
                line-height: 1.45;
                max-width: 62ch;
            }
            .dlc-hero code {
                font-family: var(--dlc-mono);
                font-size: 0.88em;
                background: #e2e8f0;
                padding: 1px 5px;
                border-radius: 4px;
            }
            .dlc-controls-bar {
                position: sticky;
                top: 0;
                z-index: 40;
                background: rgba(241, 245, 249, 0.92);
                backdrop-filter: blur(8px);
                border: 1px solid var(--dlc-border);
                border-radius: 12px;
                padding: 12px 14px 10px;
                margin-bottom: 18px;
                box-shadow: 0 1px 0 rgba(15, 23, 42, 0.04);
            }
            .dlc-controls-row {
                display: grid;
                grid-template-columns: 1fr 180px;
                gap: 16px;
                align-items: end;
                max-width: 560px;
            }
            .dlc-field label {
                display: block;
                font-size: 0.72rem;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 0.05em;
                color: var(--dlc-muted);
                margin-bottom: 4px;
            }
            .dlc-field input[type="text"] {
                width: 100%;
                box-sizing: border-box;
                padding: 8px 10px;
                border: 1px solid var(--dlc-border);
                border-radius: 8px;
                font-family: var(--dlc-mono);
                font-size: 0.9rem;
                background: var(--dlc-surface);
            }
            .dlc-toc {
                display: flex;
                flex-wrap: wrap;
                gap: 6px;
                margin-top: 12px;
                padding-top: 10px;
                border-top: 1px solid var(--dlc-border);
            }
            .dlc-toc-link {
                display: inline-flex;
                align-items: center;
                gap: 6px;
                text-decoration: none;
                color: var(--dlc-ink);
                background: var(--dlc-surface);
                border: 1px solid var(--dlc-border);
                border-radius: 999px;
                padding: 4px 10px 4px 10px;
                font-size: 0.78rem;
                transition: border-color 0.12s, background 0.12s;
            }
            .dlc-toc-link:hover {
                border-color: var(--dlc-accent);
                background: var(--dlc-accent-soft);
            }
            .dlc-toc-key {
                font-family: var(--dlc-mono);
                font-weight: 600;
            }
            .dlc-toc-count {
                color: var(--dlc-muted);
                font-variant-numeric: tabular-nums;
                font-size: 0.72rem;
            }
            .dlc-layout {
                display: grid;
                grid-template-columns: minmax(0, 1fr) 340px;
                gap: 20px;
                align-items: start;
            }
            .dlc-main {
                min-width: 0;
            }
            .dlc-code-rail {
                position: sticky;
                top: 108px;
                align-self: start;
            }
            .dlc-code-panel {
                background: #0f172a;
                color: #e2e8f0;
                border-radius: 12px;
                padding: 14px;
                box-shadow: 0 10px 30px rgba(15, 23, 42, 0.18);
                border: 1px solid #1e293b;
            }
            .dlc-code-header {
                display: flex;
                flex-direction: column;
                gap: 2px;
                margin-bottom: 10px;
            }
            .dlc-code-label {
                font-size: 0.68rem;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 0.06em;
                color: #94a3b8;
            }
            .dlc-code-target {
                font-family: var(--dlc-mono);
                font-size: 0.85rem;
                color: #fdba74;
                word-break: break-all;
            }
            .dlc-code-pre {
                margin: 0;
                padding: 12px;
                background: #020617;
                border-radius: 8px;
                overflow-x: auto;
                font-family: var(--dlc-mono);
                font-size: 0.8rem;
                line-height: 1.55;
                color: #f8fafc;
                white-space: pre;
            }
            .dlc-code-footer {
                display: flex;
                flex-direction: column;
                gap: 2px;
                margin-top: 10px;
            }
            .dlc-code-meta {
                font-size: 0.72rem;
                color: #94a3b8;
            }
            .dlc-code-hint {
                margin: 10px 0 0;
                font-size: 0.72rem;
                color: #64748b;
                line-height: 1.4;
            }
            .dlc-code-empty {
                color: #94a3b8;
                font-size: 0.9rem;
            }
            .dlc-page-footer {
                margin-top: 28px;
                padding-top: 16px;
                border-top: 1px solid var(--dlc-border);
                font-size: 12px;
                color: var(--dlc-muted);
            }
            .dlc-gallery-card:hover {
                border-color: #fdba74 !important;
            }
            .dlc-gallery-card.is-selected:hover {
                border-color: #f97316 !important;
            }
            @media (max-width: 960px) {
                .dlc-layout {
                    grid-template-columns: 1fr;
                }
                .dlc-code-rail {
                    position: sticky;
                    top: 0;
                    z-index: 30;
                    order: -1;
                }
                .dlc-code-panel {
                    border-radius: 10px;
                }
                .dlc-controls-row {
                    grid-template-columns: 1fr;
                }
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>"""

app.layout = html.Div(
    [
        html.Div(
            [
                html.H1("dash-loading-components"),
                html.P(
                    [
                        "Local explorer — compare how loaders render across each upstream library. ",
                        "Click a card for the Python snippet. Import style: ",
                        html.Code("import dash_loading_components as dlc"),
                        " → ",
                        html.Code("dlc.loading_dev.Arc(...)"),
                        ".",
                    ]
                ),
            ],
            className="dlc-hero",
        ),
        html.Div(
            [
                html.Div(
                    [
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
                                    tooltip={"placement": "bottom", "always_visible": False},
                                ),
                            ],
                            className="dlc-field",
                        ),
                        html.Div(
                            [
                                html.Label("Color"),
                                dcc.Input(
                                    id="color",
                                    type="text",
                                    value=DEFAULT_COLOR,
                                    debounce=True,
                                    spellCheck=False,
                                ),
                            ],
                            className="dlc-field",
                        ),
                    ],
                    className="dlc-controls-row",
                ),
                toc_links(),
            ],
            className="dlc-controls-bar",
        ),
        html.Div(
            [
                html.Div(id="gallery-body", className="dlc-main"),
                html.Aside(
                    html.Div(id="code-panel", className="dlc-code-panel"),
                    className="dlc-code-rail",
                ),
            ],
            className="dlc-layout",
        ),
        html.P(
            "svg_spinners gated (React 19 peer). Local MVP — no push/PR from this gallery.",
            className="dlc-page-footer",
        ),
        dcc.Store(id="selection", data=DEFAULT_SELECTION),
    ],
    className="dlc-page",
)


@callback(
    Output("selection", "data"),
    Input({"type": "dlc-card", "family": ALL, "name": ALL}, "n_clicks"),
    State("selection", "data"),
    prevent_initial_call=True,
)
def on_card_click(n_clicks, selection):
    if not ctx.triggered_id:
        return no_update
    # Ignore spurious zeros from rebuilds
    if not n_clicks or not any(n_clicks):
        return no_update
    tid = ctx.triggered_id
    if not isinstance(tid, dict) or tid.get("type") != "dlc-card":
        return no_update
    return {"family": tid["family"], "name": tid["name"]}


@callback(
    Output("gallery-body", "children"),
    Output("code-panel", "children"),
    Input("size", "value"),
    Input("color", "value"),
    Input("selection", "data"),
)
def render_explorer(size, color, selection):
    selection = selection or DEFAULT_SELECTION
    return build_gallery(size, color, selection), build_code_panel(selection, size, color)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8050"))
    print(f"Starting gallery on 0.0.0.0:{port} (REACT_VERSION={os.environ.get('REACT_VERSION')})")
    app.run(host="0.0.0.0", port=port, debug=False)
