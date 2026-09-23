# dash-loading-components (`dlc`)

Dash loading-indicators **umbrella** for Plotly Dash. Namespaced families of React loaders under one install:

```python
import dash_loading_components as dlc

# Common factory (relative speed=1.0 = that family's normal)
dlc.Loading(library="loading_dev", spinner="Dual", size=48, color="#f97316", speed=1.0)

# Namespaced power path (native prop names / units)
dlc.loading_dev.Dual(size=48, color="#f97316", duration=1000)
dlc.spinners.ClipLoader(size=24, color="#f97316")
dlc.ldrs.Ring()
```

**Hard requirement:** **React ≥19** and **Dash ≥4.5**. The day-one tent-pole family `loading_dev` ([loading-dev](https://www.npmjs.com/package/loading-dev) / [loading.dev](https://loading.dev/)) needs React 19. This package will not claim Dash 4.4 / React 18 compatibility.

## Status (PR1 scaffold)

This repository is bootstrapped from [plotly/dash-component-boilerplate](https://github.com/plotly/dash-component-boilerplate). The cookiecutter seed component is a placeholder `Arc`. **No upstream families are wrapped yet.**

Day-one planned namespaces (both Material 3 and epic-spinners included):

| Namespace | Upstream | Status |
|-----------|----------|--------|
| `loading_dev` | loading-dev 0.3.4 | planned |
| `ldrs` | ldrs 1.1.9 | planned |
| `spinners` | react-spinners 0.17.1 | planned |
| `spinners_react` | spinners-react 1.0.11 | planned |
| `loader_spinner` | react-loader-spinner 8.0.2 | planned |
| `premium` | premium-react-loaders 4.2.0 | planned |
| `indicators` | react-loading-indicators 1.0.1 | planned |
| `svg_spinners` | react-svg-spinners 0.3.1 | **gated** (React ^18.2 peer) |
| `m3` | @alerix/m3-loading-indicator 1.0.5 (Apache-2.0) | planned |
| `epic` | react-epic-spinners 0.6.0 | planned |

Full pins, SPDX licenses, URLs, and peers: **[docs/UPSTREAM-INVENTORY.md](docs/UPSTREAM-INVENTORY.md)**. Attribution: root **[NOTICE](NOTICE)**.

## vs dash-loading-spinners

[dash-loading-spinners](https://github.com/sidneykung/dash-loading-spinners) is a valuable, focused package built largely around react-spinners-era indicators. **`dlc` is not a rename or silent re-export of that project.** Goals differ:

- Broader multi-upstream umbrella with **stable namespaces** (`dlc.<family>.<Component>`)
- Explicit React 19 / Dash ≥4.5 floor (loading-dev)
- In-repo license inventory and NOTICE for every wrapped family
- Expansion path for ldrs, loading-dev, m3, epic, and more — without flattening name collisions

Where APIs overlap (e.g. react-spinners), credit upstream and prefer honest coexistence over claiming drop-in replacement.

## Releases

Releases are cut automatically by [release-please](https://github.com/googleapis/release-please) from [Conventional Commits](https://www.conventionalcommits.org/) (`feat:`, `fix:`, `chore:`, etc.) merged to `main`.

## License

MIT — Copyright (c) 2026 Evan Roy Rees. See [LICENSE](LICENSE). Third-party works remain under their own licenses listed in the inventory.

## Contributing

**PR-only to `main`.** Open a draft against `main` via compare URL; do not push commits to `main` and do not expect agents to open or merge GitHub PRs. Family wrappers should land as focused follow-up PRs (one family or small batch per PR).

### Local develop (after dependencies)

```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
npm install   # when ready to build JS
npm run build
python usage.py
```

`install_dependencies` was left false at cookiecutter time so the scaffold commit stays lean.


## Local gallery (MVP)

```bash
source /workspace/dash-loading/.venv/bin/activate
cd /workspace/dash-loading/dash-loading-components
REACT_VERSION=19.2.4 python gallery.py
# http://127.0.0.1:8050/
```

Both APIs work in the local gallery (detail pages show dual live snippets):

```python
import dash_loading_components as dlc
dlc.Loading(library="loading_dev", spinner="Arc", size=48, color="#f97316", speed=1.0)
dlc.loading_dev.Arc(size=48, color="#f97316")  # namespaced
# or prefixed: dlc.LoadingDevArc(...)
```

See `/workspace/dash-loading/GALLERY-MVP-STATUS.md` and `docs/UPSTREAM-INVENTORY.md`.
