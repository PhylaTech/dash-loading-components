# Changelog

## [0.1.1](https://github.com/PhylaTech/dash-loading-components/compare/v0.1.0...0.1.1) (2026-09-25)


### Features

* add the flicker family with 61 original flip-dot presets ([#27](https://github.com/PhylaTech/dash-loading-components/issues/27)) ([31530e2](https://github.com/PhylaTech/dash-loading-components/commit/31530e25a7442452192d498fc414766717ac96a7))
* **gallery:** social card and favicon in the site's style, animated Iconify header icons ([#20](https://github.com/PhylaTech/dash-loading-components/issues/20)) ([971a44b](https://github.com/PhylaTech/dash-loading-components/commit/971a44bf23f7277c05b66ed50e5c8bfa0b6a2de2))


### Bug Fixes

* **ci:** smoke-test the published wheel against the prop contract, not the removed factory ([#17](https://github.com/PhylaTech/dash-loading-components/issues/17)) ([fe4ad81](https://github.com/PhylaTech/dash-loading-components/commit/fe4ad81358642816e3d3a9795a1b1eba8ae560a7))
* **gallery:** author and publish date meta for LinkedIn previews ([#23](https://github.com/PhylaTech/dash-loading-components/issues/23)) ([cef5ce6](https://github.com/PhylaTech/dash-loading-components/commit/cef5ce6a3b9931ebc8403f3adf4c832c330ca3ce))
* **gallery:** keep every cycling brand mark inside its slot ([#21](https://github.com/PhylaTech/dash-loading-components/issues/21)) ([4794601](https://github.com/PhylaTech/dash-loading-components/commit/47946017841efa0568fb31b6b676473c53dd5aae))
* **gallery:** version the og:image URL so link previews refetch the card ([#22](https://github.com/PhylaTech/dash-loading-components/issues/22)) ([e701f42](https://github.com/PhylaTech/dash-loading-components/commit/e701f42612d1817489ca9af67a3054e95be79bc0))

## 0.1.0 (2026-09-25)


### ⚠ BREAKING CHANGES

* **gallery:** dlc.Loading, translate_relative_speed and supports_relative_speed are removed; upstream props are snake_case (ringCount -> ring_count); rate replaces speed as the relative tempo.
* dlc.Loading, translate_relative_speed and supports_relative_speed are removed; upstream props are snake_case (ringCount -> ring_count); rate replaces speed as the relative tempo.

### Features

* add Open Graph social preview cards for gallery ([#7](https://github.com/PhylaTech/dash-loading-components/issues/7)) ([a151c1d](https://github.com/PhylaTech/dash-loading-components/commit/a151c1d8948512a9dd5e5fbe3d801872f477319a))
* gallery MVP, common Loading API, release-please (0.1.0) ([#1](https://github.com/PhylaTech/dash-loading-components/issues/1)) ([4f91236](https://github.com/PhylaTech/dash-loading-components/commit/4f91236e78084583bb5dab2329fffd3dc0558d07))
* **gallery:** "Request a library" nav link with a GitHub issue template ([#16](https://github.com/PhylaTech/dash-loading-components/issues/16)) ([332fc19](https://github.com/PhylaTech/dash-loading-components/commit/332fc19be9a7ba887a7bbb0912aee0fb6902b621))
* **gallery:** cycling brand mark and a hero carousel of featured loaders ([#15](https://github.com/PhylaTech/dash-loading-components/issues/15)) ([586842e](https://github.com/PhylaTech/dash-loading-components/commit/586842e1ba885ddfabc83f4db2be82ec11748051))
* one prop contract on every component, gunicorn deploy, Mantine gallery ([#13](https://github.com/PhylaTech/dash-loading-components/issues/13)) ([db5a93a](https://github.com/PhylaTech/dash-loading-components/commit/db5a93a3372c0e43966c7cf0f2c7db1eadfc3044))


### Bug Fixes

* base relative speed on each spinner's own normal tempo ([#9](https://github.com/PhylaTech/dash-loading-components/issues/9)) ([42d4100](https://github.com/PhylaTech/dash-loading-components/commit/42d4100924f95fd2e47f6a95f4af237583f3d6c0))
* copy full dash_loading_components/ in Dockerfile builder stage ([#5](https://github.com/PhylaTech/dash-loading-components/issues/5)) ([ab0f964](https://github.com/PhylaTech/dash-loading-components/commit/ab0f9645d59e6491ccfdb86a59506932df856149))
* correct three premium loaders, stop cards clipping, and polish the gallery ([#12](https://github.com/PhylaTech/dash-loading-components/issues/12)) ([818164a](https://github.com/PhylaTech/dash-loading-components/commit/818164a8905e89be09eaad025913d45f01564b3b))
* **gallery:** Dash-native search, slider and color controls under React 19 ([#14](https://github.com/PhylaTech/dash-loading-components/issues/14)) ([5211cee](https://github.com/PhylaTech/dash-loading-components/commit/5211cee8245b6d9d440160749fc2eb1617f89515))
* pin dash&gt;=4.5.0rc0 so Render can install pre-release ([#3](https://github.com/PhylaTech/dash-loading-components/issues/3)) ([0011fce](https://github.com/PhylaTech/dash-loading-components/commit/0011fce823106fdd73574d5edfa63fd520d38ee4))
* remove unused styled-jsx to resolve React 19 peer-dep conflict ([#4](https://github.com/PhylaTech/dash-loading-components/issues/4)) ([9aaa6f6](https://github.com/PhylaTech/dash-loading-components/commit/9aaa6f6905ac9d76d513f005cc214f33a663a903))
* ship family subpackages and sync version in published wheel ([#8](https://github.com/PhylaTech/dash-loading-components/issues/8)) ([3914680](https://github.com/PhylaTech/dash-loading-components/commit/391468033734054e6bf434361eba766885924ec5))

## Changelog

All notable changes to this project will be documented in this file.

This changelog is automatically maintained by
[release-please](https://github.com/googleapis/release-please) from
[Conventional Commits](https://www.conventionalcommits.org/).
