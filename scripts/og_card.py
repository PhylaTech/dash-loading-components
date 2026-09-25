"""Render assets/og-card.png (1200x630) and assets/favicon.ico from the gallery's own style.

    pixi run og-card

The card is a Dash page with real loaders on it, screenshotted through the
same Chrome the tests use, so it stays in step with the site's colors and
components instead of being redrawn by hand.
"""
from __future__ import annotations

import os
import sys
import time
from pathlib import Path

os.environ.setdefault("REACT_VERSION", "19.2.4")
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import dash
from dash import Dash, html
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import dash_loading_components as dlc

dash._dash_renderer._set_react_version("19.2.4")

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "og-card.png"
ICO = ROOT / "assets" / "favicon.ico"
ACCENT = "#f97316"
W, H = 1200, 630

# Nine loaders, one per library, at the sizes that read best at 96px tiles.
TILES = [
    dlc.loading_dev.Dual(size=44, color=ACCENT),
    dlc.ldrs.Helix(size=44, color=ACCENT),
    dlc.premium.OrbitRings(size=44, color=ACCENT),
    dlc.spinners.HashLoader(size=40, color=ACCENT),
    dlc.spinners_react.SpinnerDiamond(size=44, color=ACCENT, thickness=140),
    dlc.loader_spinner.TailSpin(size=44, color=ACCENT),
    dlc.indicators.Mosaic(size="small", color=ACCENT),
    dlc.m3.LoadingIndicator(size=44, color=ACCENT),
    dlc.epic.TrinityRingsSpinner(size=44, color=ACCENT),
]

CSS = """
html { -webkit-font-smoothing: antialiased; }
body { margin: 0; background: #1a1b1e; color: #f8f9fa;
  font-family: ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }
.card { width: 1200px; height: 630px; box-sizing: border-box; padding: 64px 72px;
  display: grid; grid-template-columns: 1fr 336px; gap: 56px; align-items: center; position: relative;
  background: radial-gradient(circle, rgb(255 255 255 / 0.06) 1px, transparent 1px) 0 0 / 16px 16px; }
.card::after { content: ""; position: absolute; inset: 0; pointer-events: none;
  background: radial-gradient(60% 80% at 82% 50%, rgb(249 115 22 / 0.10), transparent 70%); }
h1 { margin: 0; font-size: 64px; line-height: 1.04; letter-spacing: -0.035em; font-weight: 650; }
h1 span { display: block; color: #909296; }
.lede { margin: 26px 0 0; font-size: 24px; line-height: 1.4; color: #c1c2c5; max-width: 640px; }
.lede b { color: #f8f9fa; font-weight: 600; }
.pip { display: inline-flex; align-items: center; gap: 10px; margin-top: 30px; padding: 12px 18px;
  border: 1px solid #373a40; border-radius: 10px; background: #25262b;
  font: 500 19px ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; color: #e9ecef; }
.pip i { color: #909296; font-style: normal; }
.grid { display: grid; grid-template-columns: repeat(3, 96px); gap: 12px; position: relative; }
.tile { width: 96px; height: 96px; display: flex; align-items: center; justify-content: center;
  border: 1px solid #373a40; border-radius: 16px; background: #25262b; overflow: hidden; }
.tile.indicators > * { transform: scale(0.6); }
.foot { position: absolute; left: 72px; bottom: 44px; display: flex; align-items: center; gap: 10px;
  font-size: 18px; color: #909296; }
.foot b { color: #e9ecef; font-weight: 600; }
.foot img { width: 22px; height: 22px; }
"""

app = Dash(__name__, assets_folder=str(ROOT / "assets"), assets_ignore=r".*\.css|.*\.js")
app.index_string = app.index_string.replace("</head>", f"<style>{CSS}</style></head>", 1)
app.layout = html.Div(
    [
        html.Div(
            [
                html.H1(["Loading,", html.Span("made beautiful for Dash.")]),
                html.P([html.B("107 loading indicators"), " from 9 React libraries, as Dash components "
                        "that all speak the same ", html.B("size"), ", ", html.B("color"), ", ",
                        html.B("rate"), " and ", html.B("playing"), "."], className="lede"),
                html.Div([html.I("$"), "pip install dash-loading-components"], className="pip"),
            ]
        ),
        html.Div(
            [html.Div(t, className="tile indicators" if type(t).__name__.startswith("Indicators") else "tile")
             for t in TILES],
            className="grid",
        ),
        html.Div([html.Img(src="/assets/favicon.svg"), html.B("dash-loading-components"),
                  html.Span("·"), html.Span("dash-loading-components.phylatech.com")], className="foot"),
    ],
    className="card",
    id="card",
)


def write_ico(driver) -> None:
    """favicon.ico for clients that ignore SVG icons: one 64px PNG frame,
    which the ICO container has allowed since Vista. Dash serves it at
    /_favicon.ico; the SVG is linked from the page for everyone else."""
    import base64
    import struct

    driver.set_script_timeout(10)
    png = base64.b64decode(driver.execute_async_script("""
        const done = arguments[arguments.length - 1];
        const img = new Image();
        img.onload = () => {
          const c = document.createElement('canvas');
          c.width = c.height = 64;
          c.getContext('2d').drawImage(img, 0, 0, 64, 64);
          done(c.toDataURL('image/png').split(',')[1]);
        };
        img.src = '/assets/favicon.svg';
    """))
    header = struct.pack("<HHH", 0, 1, 1)
    entry = struct.pack("<BBBBHHII", 64, 64, 0, 0, 1, 32, len(png), 6 + 16)
    ICO.write_bytes(header + entry + png)
    print(f"wrote {ICO} ({ICO.stat().st_size} bytes)")


def main() -> None:
    import threading

    threading.Thread(target=lambda: app.run(port=8099, debug=False), daemon=True).start()
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument(f"--window-size={W},{H}")
    options.add_argument("--force-device-scale-factor=1")
    options.add_argument("--hide-scrollbars")
    driver = webdriver.Chrome(options=options)
    try:
        driver.get("http://127.0.0.1:8099/")
        for _ in range(50):
            if driver.execute_script("return document.querySelectorAll('.tile > *').length") >= len(TILES):
                break
            time.sleep(0.2)
        # Let every loader settle into a representative frame.
        time.sleep(1.2)
        # The window size includes browser chrome; grow it until the viewport is exactly W x H.
        inner_w, inner_h = driver.execute_script("return [innerWidth, innerHeight]")
        driver.set_window_size(2 * W - inner_w, 2 * H - inner_h)
        time.sleep(0.3)
        driver.get_screenshot_as_file(str(OUT))
        write_ico(driver)
    finally:
        driver.quit()
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
