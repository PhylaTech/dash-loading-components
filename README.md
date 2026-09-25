# dash-loading-components (`dlc`)

Loading indicators for [Plotly Dash](https://dash.plotly.com), wrapping nine
React spinner libraries as one install. 107 components under stable namespaces,
with a common factory over the top so you can switch families without
relearning each one's props.

Browse them all in the live gallery: **<https://dash-loading-components.phylatech.com>**

```bash
pip install dash-loading-components
```

## Two APIs

```python
import dash_loading_components as dlc

# Common factory. `speed` is relative: 1.0 is this spinner's normal tempo,
# translated to whatever native unit its family uses.
dlc.Loading(library="loading_dev", spinner="Dual", size=48, color="#f97316", speed=1.0)

# Namespaced. Upstream prop names and units, and every exotic prop a family has.
dlc.loading_dev.Dual(size=48, color="#f97316", duration=1000)
dlc.spinners.ClipLoader(size=24, color="#f97316")
dlc.ldrs.Ring()
```

`dlc.Loading` covers the props every family shares (`size`, `color`, `speed`,
`playing`, `class_name`) and forwards anything else through. Reach for the
namespaced form when you want a family's own vocabulary.

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

Every component is also exported prefixed at the top level
(`dlc.LoadingDevArc`, `dlc.LdrsRing`) for Dash callbacks that want a flat name.

Version pins, SPDX licenses, upstream URLs and React peers:
[docs/UPSTREAM-INVENTORY.md](docs/UPSTREAM-INVENTORY.md). Attribution:
[NOTICE](NOTICE).

## Relative speed

`speed` on `dlc.Loading` is a rate, not a duration. `1.0` reproduces the tempo
the upstream component runs at on its own, and the value is translated per
family: a duration in milliseconds for loading-dev and epic, seconds per loop
for ldrs, a multiplier for react-spinners, a percentage for spinners-react, an
offset for react-loading-indicators.

That baseline is per spinner, not per family. `loading_dev.Compass` is normally
500ms and `loading_dev.Slide` is 2400ms, so `speed=1.0` gives each of them its
own tempo and `speed=2.0` runs either at twice its own rate.

To set a native unit directly, use the namespaced form. Passing both a relative
`speed` and a native tempo prop raises `ValueError` rather than silently
picking one.

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
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt -r tests/requirements.txt
npm install
npm run build          # JS bundle + generated Python wrappers
python usage.py        # minimal demo app
python gallery.py      # the full gallery, http://127.0.0.1:8050/
pytest
```

`npm run build:js` alone is enough when you have only changed React or CSS
under `src/`.

## License

MIT, Copyright (c) 2026 Evan Roy Rees. See [LICENSE](LICENSE). Wrapped
third-party libraries remain under their own licenses, listed in the inventory.
