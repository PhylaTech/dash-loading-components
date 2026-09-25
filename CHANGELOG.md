# Changelog

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
