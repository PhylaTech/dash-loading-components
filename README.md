# dash-loading-components (`dlc`)

Loading indicators for [Plotly Dash](https://dash.plotly.com), wrapping ten
React spinner libraries as one install. 138 components under stable namespaces,
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
dlc.list_libraries()          # ['loading_dev', 'ldrs', 'spinners', ...]
dlc.list_spinners("ldrs")     # ['Ring', 'Helix', 'DotPulse', ...]
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
| `flicker` | [flicker-dot](https://www.npmjs.com/package/flicker-dot) | 31 |

## Flip-dot presets

flicker-dot is a player: it animates whatever 7x7 frames it is given. `dlc.flicker`
ships 31 original presets for it, drawn by PhylaTech and MIT licensed with this
package, in three sets: Field (the naturalist set: `Mycelium`, `Osculum`,
`Diatom`, `Cladogram`, `Chromatogram`, ...), Board (flip-dot panel classics) and
Geometry. Each is the player with its frames filled in:

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
`variant` picks the grid: `"7x7"`, its inner `"5x5"` (bigger dots) or `"9x9"`,
the 7x7 padded with a ring of unlit dots (smaller dots at the same size).
Lit dots are `color` at `on_opacity` (default `1`). Unlit dots are `off_color`
(default: `color`) at `off_opacity` (default `0.16`)
rather than upstream's fixed light grey, so one `color` reads on light and dark
pages; `off_opacity=0` shows only the lit dots.

Every component is also exported prefixed at the top level
(`dlc.LoadingDevArc`, `dlc.LdrsRing`) for Dash callbacks that want a flat name.

Version pins, SPDX licenses, upstream URLs and React peers:
[docs/UPSTREAM-INVENTORY.md](docs/UPSTREAM-INVENTORY.md). Attribution:
[NOTICE](NOTICE).

## Relative tempo

`rate` is a rate, not a duration. `1.0` reproduces the tempo the upstream
component runs at on its own, and the value is translated per family in the
wrappers: a duration in milliseconds for loading-dev, epic and premium,
seconds per loop for ldrs, a multiplier for react-spinners, m3 and flicker, a
percentage for spinners-react, an offset for react-loading-indicators.

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
PRs, one family or a small batch per PR. Releases are cut by
[release-please](https://github.com/googleapis/release-please) from
[Conventional Commits](https://www.conventionalcommits.org/) merged to `main`,
so commit subjects need a `feat:` / `fix:` / `chore:` prefix.

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
