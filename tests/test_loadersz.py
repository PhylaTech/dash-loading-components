"""Tests for the loadersz family wrap.

Checks: rate->speed mapping, size passthrough, color passthrough,
registry contains exactly the 160 loader states, namespace exports,
and category coverage.
"""
from __future__ import annotations

import pytest

import dash_loading_components as dlc
from dash_loading_components import loadersz
from dash_loading_components.registry import FAMILY_LOOKUP, list_libraries, list_spinners


class TestRateSpeedMapping:
    """rate -> upstream speed (timeline multiplier): speed = rate."""

    def test_rate_1_gives_speed_1(self):
        node = dlc.loadersz.Loader(state="working", rate=1.0).to_plotly_json()["props"]
        assert node["rate"] == 1.0

    def test_rate_2_gives_double_speed(self):
        node = dlc.loadersz.Loader(state="working", rate=2.0).to_plotly_json()["props"]
        assert node["rate"] == 2.0

    def test_native_speed_wins_over_rate(self):
        node = dlc.loadersz.Loader(state="working", rate=2.0, speed=3.0).to_plotly_json()["props"]
        assert node["speed"] == 3.0
        assert node["rate"] == 2.0


class TestSizePassthrough:
    """Common `size` maps directly to upstream size (CSS px)."""

    def test_size_prop_is_recorded(self):
        node = dlc.loadersz.Loader(state="working", size=48).to_plotly_json()["props"]
        assert node["size"] == 48

    def test_size_default_unset(self):
        node = dlc.loadersz.Loader(state="working").to_plotly_json()["props"]
        assert "size" not in node or node.get("size") is None


class TestColorPassthrough:
    """Common `color` maps directly to upstream color (CSS colour string)."""

    def test_color_prop_is_recorded(self):
        node = dlc.loadersz.Loader(state="working", color="#f97316").to_plotly_json()["props"]
        assert node["color"] == "#f97316"

    def test_hue_prop_is_recorded(self):
        node = dlc.loadersz.Loader(state="working", hue=200).to_plotly_json()["props"]
        assert node["hue"] == 200


class TestPlayingPaused:
    """playing -> paused = !playing; explicit paused wins."""

    def test_playing_false(self):
        node = dlc.loadersz.Loader(state="working", playing=False).to_plotly_json()["props"]
        assert node["playing"] is False

    def test_native_paused_wins(self):
        node = dlc.loadersz.Loader(
            state="working", playing=False, paused=False
        ).to_plotly_json()["props"]
        assert node["paused"] is False
        assert node["playing"] is False


class TestRegistryLoaderStates:
    """The Loading registry must list exactly the 160 loader states."""

    def test_loadersz_in_libraries(self):
        assert "loadersz" in list_libraries()

    def test_state_count(self):
        spinners = list_spinners("loadersz")
        assert len(spinners) == 160, f"Expected 160, got {len(spinners)}: {spinners[:5]}..."

    def test_all_states_present(self):
        spinners = set(list_spinners("loadersz"))
        for s in loadersz.LOADER_STATES:
            assert s in spinners, f"Loader state {s} missing from registry"

    def test_no_extra_states(self):
        spinners = set(list_spinners("loadersz"))
        expected = set(loadersz.LOADER_STATES)
        extra = spinners - expected
        assert not extra, f"Extra states in registry: {extra}"


class TestNamespaceExports:
    """dlc.loadersz.Loader must be importable."""

    def test_loader_importable(self):
        assert callable(dlc.loadersz.Loader)

    def test_no_flat_export(self):
        assert not hasattr(dlc, "Loader"), "Bare flat export found: dlc.Loader (collision risk)"

    def test_loader_states_list(self):
        assert len(loadersz.LOADER_STATES) == 160

    def test_categories_present(self):
        assert "loaders" in loadersz.CATEGORIES
        assert "data" in loadersz.CATEGORIES
        assert "reasoning" in loadersz.CATEGORIES
        assert "atmosphere" in loadersz.CATEGORIES
        assert "motion" in loadersz.CATEGORIES
        assert "systems" in loadersz.CATEGORIES


class TestCategoryCompleteness:
    """Every state must appear in exactly one category."""

    def test_all_states_categorized(self):
        categorized = set(loadersz.STATE_CATEGORY.keys())
        all_states = set(loadersz.LOADER_STATES)
        missing = all_states - categorized
        assert not missing, f"States missing from categories: {missing}"

    def test_no_duplicate_categories(self):
        from collections import Counter
        cat_states = []
        for states in loadersz._CATEGORY_STATES.values():
            cat_states.extend(states)
        dupes = [s for s, c in Counter(cat_states).items() if c > 1]
        assert not dupes, f"States in multiple categories: {dupes}"


class TestChartStates:
    """Chart-shaped states must be in the data category."""

    CHART_STATES = [
        "heatmapping", "candlesticking", "treemapping", "sankeying",
        "bar-charting", "bubble-charting",
    ]

    def test_chart_states_exist(self):
        all_states = set(loadersz.LOADER_STATES)
        for s in self.CHART_STATES:
            assert s in all_states, f"Chart state {s} not in LOADER_STATES"

    def test_chart_states_in_data_category(self):
        for s in self.CHART_STATES:
            assert loadersz.STATE_CATEGORY.get(s) == "data", (
                f"Chart state {s} should be in 'data', got {loadersz.STATE_CATEGORY.get(s)}"
            )


class TestLoaderComponent:
    """dlc.loadersz.Loader(state=...) must work."""

    def test_state_is_recorded(self):
        node = dlc.loadersz.Loader(state="searching").to_plotly_json()["props"]
        assert node["state"] == "searching"

    def test_default_state_unset(self):
        node = dlc.loadersz.Loader().to_plotly_json()["props"]
        assert "state" not in node or node.get("state") is None

    def test_theme_prop(self):
        node = dlc.loadersz.Loader(state="working", theme="dark").to_plotly_json()["props"]
        assert node["theme"] == "dark"

    def test_density_prop(self):
        node = dlc.loadersz.Loader(state="working", density=1.5).to_plotly_json()["props"]
        assert node["density"] == 1.5
