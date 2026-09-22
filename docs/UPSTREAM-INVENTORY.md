# Upstream inventory — dash-loading-components (`dlc`)

**Status:** PR1 scaffold. All day-one wrappers are `planned` (or `gated`) until family PRs land.  
**Package license:** MIT (this repo). Upstream licenses in the SPDX column.  
**Baseline:** React ≥19 / Dash ≥4.5 (hard requirement for shipping `loading_dev`).

Update this table when a family is added, version-pinned, or wrap status changes. See also root `NOTICE`.

## Day-one families

| dlc namespace | Upstream npm + version | SPDX | Homepage / repo | React peers | Wrap status | Notes |
|--------------|------------------------|------|-----------------|-------------|-------------|-------|
| `loading_dev` | [loading-dev](https://www.npmjs.com/package/loading-dev) **0.3.4** | MIT | [loading.dev](https://loading.dev/) · [jakubkrehel/loading](https://github.com/jakubkrehel/loading) | ≥19 | `planned` | Product tent-pole; drives React 19 / Dash ≥4.5 floor |
| `ldrs` | [ldrs](https://www.npmjs.com/package/ldrs) **1.1.9** | MIT | [uiball.com/ldrs](https://uiball.com/ldrs/) · [GriffinJohnston/ldrs](https://github.com/GriffinJohnston/ldrs) | none declared | `planned` | Per-component CSS imports |
| `spinners` | [react-spinners](https://www.npmjs.com/package/react-spinners) **0.17.1** | MIT | [npm](https://www.npmjs.com/package/react-spinners) · [davidhu2000/react-spinners](https://github.com/davidhu2000/react-spinners) | ^16–^19 | `planned` | Classic zoo; also used by dash-loading-spinners |
| `spinners_react` | [spinners-react](https://www.npmjs.com/package/spinners-react) **1.0.11** | MIT | [npm](https://www.npmjs.com/package/spinners-react) · [adexin/spinners-react](https://github.com/adexin/spinners-react) | ^16–^19 | `planned` | Not in dash-loading-spinners |
| `loader_spinner` | [react-loader-spinner](https://www.npmjs.com/package/react-loader-spinner) **8.0.2** | MIT | [npm](https://www.npmjs.com/package/react-loader-spinner) · [mhnpd/react-loader-spinner](https://github.com/mhnpd/react-loader-spinner) | ≥17 `<20` | `planned` | High wrap friction (styled-components); own PR after core |
| `premium` | [premium-react-loaders](https://www.npmjs.com/package/premium-react-loaders) **4.2.0** | MIT | [npm](https://www.npmjs.com/package/premium-react-loaders) | ^18 \|\| ^19 | `planned` | One CSS import |
| `indicators` | [react-loading-indicators](https://www.npmjs.com/package/react-loading-indicators) **1.0.1** | MIT | [npm](https://www.npmjs.com/package/react-loading-indicators) | ≥16.8 | `planned` | Low friction |
| `svg_spinners` | [react-svg-spinners](https://www.npmjs.com/package/react-svg-spinners) **0.3.1** | MIT | [npm](https://www.npmjs.com/package/react-svg-spinners) · [theme-park/react-svg-spinners](https://github.com/theme-park/react-svg-spinners) | **^18.2 only** | `gated` | Do not merge until React 19 peer resolved (override/fork) or deferred |
| `m3` | [@alerix/m3-loading-indicator](https://www.npmjs.com/package/@alerix/m3-loading-indicator) **1.0.5** | Apache-2.0 | [npm](https://www.npmjs.com/package/@alerix/m3-loading-indicator) | ≥18 | `planned` | Day-one (LARGER): include with `epic`; Apache-2.0 OK with MIT wrapper + NOTICE |
| `epic` | [react-epic-spinners](https://www.npmjs.com/package/react-epic-spinners) **0.6.0** | MIT | [npm](https://www.npmjs.com/package/react-epic-spinners) · [bondz/react-epic-spinners](https://github.com/bondz/react-epic-spinners) | ≥16.8 | `planned` | Day-one (LARGER): include with `m3`; styled-components friction |

## Hard skips (license — do not wrap)

| Upstream | SPDX | Reason |
|----------|------|--------|
| [css-spinners](https://www.npmjs.com/package/css-spinners) | GPL-3.0 | Incompatible with MIT product distribution without Legal exception |
| [react18-loaders](https://www.npmjs.com/package/react18-loaders) | MPL-2.0 | Avoid unless Legal OK |

## Scaffold seed component

Cookiecutter seed: `Arc` (placeholder Function Component). Real family wrappers land in later PRs; this inventory is the day-one contract.

## Column legend

| Column | Meaning |
|--------|---------|
| Wrap status | `planned` = day-one intent, not yet wrapped; `gated` = blocked on peer/policy; `in-PR` / `shipped` = later |
| React peers | Declared upstream peerDependency range (npm), not our package floor |
