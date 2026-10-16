# dash-loading-components (`dlc`)

Loading indicators for [Plotly Dash](https://dash.plotly.com), wrapping thirteen
React spinner libraries as one install. 472 components under stable namespaces,
with a common factory over the top so you can switch families without
relearning each one's props.

Browse them all in the live gallery: **<https://dash-loading-components.phylatech.com>**

```bash
pip install dash-loading-components
```

## One contract, every component

```python
import dash_loading_components as dlc

dlc.loading_dev.Dual(size=48, color="#f97316", rate=1.5)
dlc.premium.OrbitRings(size=48, color="#f97316", ring_count=4, playing=False)
dlc.ldrs.Ring(size=48, color="#f97316", stroke=5)
```

Every component takes the same four props with the same meaning:

| prop | meaning |
|---|---|
| `size` | pixels (`react-loading-indicators` takes its own `"small"` / `"medium"` / `"large"` tokens) |
| `color` | any CSS color |
| `rate` | relative tempo: `1.0` is this spinner's own tempo, `2.0` twice as fast. Unset keeps the upstream tempo |
| `playing` | `False` pauses the animation |

Each library's own props are there too, in snake_case, in the library's own
units: `dlc.loading_dev.Arc(duration=1600, easing="stacked")`,
`dlc.spinners.ClipLoader(speed_multiplier=2)`. A native tempo or pause prop
passed alongside `rate` or `playing` wins.

Need a loading overlay? Use Dash's own:

```python
dcc.Loading(children, custom_spinner=dlc.ldrs.Ring(size=48))
```

Discover what is available at runtime:

```python
dlc.list_libraries()          # ['loading_dev', 'ldrs', 'spinners', ..., 'gridora', 'loadersz', 'thinking_orbs']
dlc.list_spinners("ldrs")     # ['Ring', 'Helix', 'DotPulse', ...]
dlc.list_spinners("loadersz") # ['working', 'searching', 'connecting', ...]
```

## Requirements

**React ≥19 and Dash ≥4.5**, both hard requirements. The `loading_dev` family
needs React 19, and this package will not claim Dash 4.4 / React 18
compatibility.

Dash 4.5 is not on PyPI as a stable release yet, so the dependency is pinned as
`dash>=4.5.0rc0`. That specifier names the pre-release, which is what lets pip
resolve it; it will accept the final 4.5 release once published.

## Families

| Namespace | Upstream | Components |
|-----------|----------|-----------:|
| `loading_dev` | [loading-dev](https://www.npmjs.com/package/loading-dev) | 29 |
| `premium` | [premium-react-loaders](https://www.npmjs.com/package/premium-react-loaders) | 15 |
| `ldrs` | [ldrs](https://www.npmjs.com/package/ldrs) | 12 |
| `spinners` | [react-spinners](https://www.npmjs.com/package/react-spinners) | 12 |
| `indicators` | [react-loading-indicators](https://www.npmjs.com/package/react-loading-indicators) | 11 |
| `loader_spinner` | [react-loader-spinner](https://www.npmjs.com/package/react-loader-spinner) | 10 |
| `spinners_react` | [spinners-react](https://www.npmjs.com/package/spinners-react) | 9 |
| `epic` | [react-epic-spinners](https://www.npmjs.com/package/react-epic-spinners) | 8 |
| `m3` | [@alerix/m3-loading-indicator](https://www.npmjs.com/package/@alerix/m3-loading-indicator) | 1 |
| `flicker` | [flicker-dot](https://www.npmjs.com/package/flicker-dot) | 63 |
| `gridora` | [gridora](https://www.npmjs.com/package/gridora) | 133 |
| `loadersz` | [loadersz](https://www.npmjs.com/package/loadersz) | 160 |
| `thinking_orbs` | [thinking-orbs](https://www.npmjs.com/package/thinking-orbs) | 9 |

## Flip-dot presets

flicker-dot is a player: it animates whatever 7x7 frames it is given. `dlc.flicker`
ships 62 original presets for it, drawn by PhylaTech and MIT licensed with this
package, in six sets: Field (the naturalist set: `Mycelium`, `Diatom`,
`Cladogram`, `Chromatogram`, `HplcTrace`, `MassSpec`, `TestTube`, `Jellyfish`, ...), Data
(`Scatter`, `Histogram`, `LineChart`, `PieChart`, `Heatmap`, `Database`),
Everyday (`Cart`, `Upload`, `Download`, `Mail`, `Wifi`, `Heart`, `Lock`, ...),
Board (flip-dot panel classics), Geometry, and Solids (the five Platonic
solids). Each of those is the player with its frames filled in. The 63rd
spinner, `dlc.flicker.WellPlate`, is a full 96-well microplate (8 by 12, A1 corner cut off)
that a pipette fills well by well: it is drawn as SVG, because the 7x7 grid has
no room for it, and takes `size`, `color`, `on_opacity`, `off_color`, `off_opacity`,
`rate` and `playing`.

```python
dlc.flicker.Mycelium(size=48, color="#f97316")
dlc.flicker.Helix(size=48, variant="5x5", off_color="#e5e5e5", off_opacity=1)
```

To play frames of your own, give `dlc.flicker.Spinner` a list of frames. A frame
is 7 strings of 7 characters, `#` lit and `.` dark (or upstream's 49 booleans,
or 7 lists of 7):

```python
blink = ["...#...", "..###..", ".#####.", "#######", ".#####.", "..###..", "...#..."]
dlc.flicker.Spinner(grids=[blink, [row.replace("#", ".") for row in blink]])
```

`dlc.flicker.PRESETS` holds every preset's frames, a starting point for your own.
`rotate` (0, 90, 180 or 270, clockwise) and `mirror` orient any preset, so
`dlc.flicker.Cladogram(rotate=90)` grows left to right. `variant` picks the grid: `"7x7"`, its inner `"5x5"` (bigger dots) or `"9x9"`,
the 7x7 padded with a ring of unlit dots (smaller dots at the same size).
Lit dots are `color` at `on_opacity` (default `1`). Unlit dots are `off_color`
(default: `color`) at `off_opacity` (default `0.16`)
rather than upstream's fixed light grey, so one `color` reads on light and dark
pages; `off_opacity=0` shows only the lit dots.

## Grid-dot loaders

gridora ships 133 motion variants of grid-dot animations plus a bitmap-font text
component. `dlc.gridora.GridLoader` renders any motion variant; `dlc.gridora.Text`
renders text using gridora's built-in glyph font.

```python
dlc.gridora.GridLoader(variant="orbit", color="#f97316", rate=1.5)
dlc.gridora.Text(text="LOAD", color="#f97316", effect="bounce")
```

**`size` is overall px, not cell size.** Upstream `size` is an alias for `cellSize`
(the individual cell), which would make a 3×3 grid 12 px wide. When you set the
common `size`, `dlc.gridora` derives the cell size from the grid geometry. Pass
`cell_size` explicitly if you need direct control. The upstream `speed` prop is
cycle duration in seconds (higher = slower), not a multiplier; `rate` translates:
`speed = 1 / rate`.

## Canvas loaders

loadersz ships 160 canvas loaders as a Web Component, from product states
(`working`, `searching`) to chart-shaped ones (`heatmapping`, `sankeying`,
`treemapping`). `dlc.loadersz.Loader` renders any of them; the state is a prop,
so there is no `dlc.loadersz.working`.

```python
dlc.loadersz.Loader(state="heatmapping", size=96, color="#f97316")
dlc.loadersz.Loader(state="working", hue=200, density=1.5)
```

`color` paints every particle itself and wins over `hue` and `theme`. Leave it
off to get loadersz's own palette (grey, or a loader's own tones), tinted by
`hue` (0 to 360) and drawn for a light or dark page by `theme` (`"auto"`
follows the operating system, not the page).

## Agent status orbs

thinking-orbs draws nine states an AI or agent can be in as dotted spheres on a
plain 2D canvas: `working`, `searching`, `solving`, `listening`, `connecting`,
`weaving`, `composing`, `breathing` and `shaping`. `dlc.thinking_orbs.Orb`
renders any of them; the state is a prop, so there is no
`dlc.thinking_orbs.working`.

```python
dlc.thinking_orbs.Orb(state="searching")
dlc.thinking_orbs.Orb(state="solving", size=20, color="#f97316", rate=1.5)
```

- **`size` is any pixel size, drawn from one of three designs.** Upstream hand-tunes
  the orb at 64 (chat avatar), 32 and 20 (inline text) with separate dot counts,
  dot sizes and speeds, and fails on any other size. `dlc` draws the nearest design
  (by ratio) and scales the canvas to `size`: 48 is the 64 design a little smaller,
  24 the 20 design a little larger. Sizes above 64 upscale the 64 design and soften.
  Upstream documents 64 and 20; its 32 is interpolated from them and has had no tuning
  pass of its own. `size` defaults to 64.
- **`color` tints the ink; leave it off for monochrome.** Upstream's stock ink is
  grey, light on dark pages and dark on light ones. `color` takes `#rgb`, `#rrggbb`
  or `rgb(r, g, b)` only (any other CSS color syntax is ignored, so `"orange"`
  keeps the grey) and keeps the orb's depth shading on the tint.
- **`theme="auto"` follows the page.** Upstream resolves auto from an ancestor
  `data-theme` attribute or `dark` / `light` class, else the operating system.
  Mantine sets neither, so `dlc` mirrors `data-mantine-color-scheme` from `<html>`
  onto the orb while that attribute is present: in a `dash-mantine-components` app
  the orbs follow its color scheme toggle live. Pin `theme="dark"` or `"light"` for
  a fixed ink.
- `dots` and `dot_size` are upstream's density and dot radius multipliers (1 is the
  tuned look). `rate` is upstream's `speed`, a multiplier on each state's own tempo,
  and `playing=False` freezes the frame (upstream `paused`). The orb pauses by itself
  while offscreen or in a hidden tab and draws one still frame under
  `prefers-reduced-motion`.

Every component is also exported prefixed at the top level
(`dlc.LoadingDevArc`, `dlc.LdrsRing`) for Dash callbacks that want a flat name.

Version pins, SPDX licenses, upstream URLs and React peers:
[docs/UPSTREAM-INVENTORY.md](docs/UPSTREAM-INVENTORY.md). Attribution:
[NOTICE](NOTICE).

## Relative tempo

`rate` is a rate, not a duration. `1.0` reproduces the tempo the upstream
component runs at on its own, and the value is translated per family in the
wrappers: a duration in milliseconds for loading-dev, epic and premium,
seconds per loop for ldrs, a multiplier for react-spinners, m3, flicker and
loadersz, a percentage for spinners-react, an offset for
react-loading-indicators, and seconds per cycle (inverted) for gridora.

That baseline is per spinner, not per family. `loading_dev.Compass` is normally
500ms and `loading_dev.Slide` is 2400ms, so `rate=1.0` gives each of them its
own tempo and `rate=2.0` halves both. `react-loader-spinner` has no tempo prop,
so `rate` does nothing there.

## Compared with dash-loading-spinners

[dash-loading-spinners](https://github.com/sidneykung/dash-loading-spinners) is
a focused package built largely around react-spinners-era indicators. `dlc` is
not a rename or a silent re-export of it. The goals differ:

- A multi-upstream umbrella with stable namespaces, `dlc.<family>.<Component>`
- An explicit React 19 / Dash ≥4.5 floor, driven by loading-dev
- A license inventory and NOTICE covering every wrapped family
- Room to add families without flattening name collisions

Where the APIs overlap, credit upstream; this is honest coexistence, not a
drop-in replacement.

## Contributing

Pull requests only, against `main`. Family wrappers land as focused follow-up
PRs, one family or a small batch per PR. This repo squash-merges, so **the PR
title becomes the commit subject on `main`**. Releases are cut by
[release-please](https://github.com/googleapis/release-please) from that
subject, so the PR title must carry a
[Conventional Commits](https://www.conventionalcommits.org/) type (`feat:`,
`fix:`, etc.). See [CONTRIBUTING.md](CONTRIBUTING.md) for the full rules.

Local setup:

```bash
pixi install           # Python, Node, Dash, the gallery's deps, test tooling
npm install
pixi run build         # JS bundle + generated Python wrappers
pixi run python usage.py   # minimal demo app
pixi run gallery       # the full gallery, http://127.0.0.1:8050/
pixi run test
```

The deployed gallery runs under gunicorn (`gallery:server`); `pixi run serve`
does the same locally.

`pixi run build-js` alone is enough when you have only changed React or CSS
under `src/`.

## License

MIT, Copyright (c) 2026 Phyla Technologies. See [LICENSE](LICENSE). Wrapped
third-party libraries remain under their own licenses, listed in the inventory.
