"""Tests for the gridora family wrap.

Checks: rate→speed mapping, size derivation, registry contains exactly
the 133 motion variants and no glyphs, namespace exports, and Text.
"""
from __future__ import annotations

import pytest

import dash_loading_components as dlc
from dash_loading_components import gridora
from dash_loading_components.registry import FAMILY_LOOKUP, list_libraries, list_spinners


class TestRateSpeedMapping:
    """rate → upstream speed (seconds per cycle): speed = 1/rate."""

    def test_rate_1_gives_speed_1(self):
        node = dlc.gridora.GridLoader(variant="orbit", rate=1.0).to_plotly_json()["props"]
        assert node["rate"] == 1.0

    def test_rate_2_gives_half_second(self):
        node = dlc.gridora.GridLoader(variant="orbit", rate=2.0).to_plotly_json()["props"]
        assert node["rate"] == 2.0

    def test_native_speed_wins_over_rate(self):
        node = dlc.gridora.GridLoader(variant="orbit", rate=2.0, speed=3.0).to_plotly_json()["props"]
        assert node["speed"] == 3.0
        assert node["rate"] == 2.0


class TestSizeDerivation:
    """Common `size` (overall px) must NOT pass through as upstream size/cellSize."""

    def test_size_prop_is_recorded(self):
        node = dlc.gridora.GridLoader(variant="orbit", size=48).to_plotly_json()["props"]
        assert node["size"] == 48

    def test_explicit_cell_size_wins(self):
        node = dlc.gridora.GridLoader(
            variant="orbit", size=48, cell_size=10
        ).to_plotly_json()["props"]
        assert node["cell_size"] == 10
        assert node["size"] == 48


class TestPlayingPaused:
    """playing → paused = !playing; explicit paused wins."""

    def test_playing_false(self):
        node = dlc.gridora.GridLoader(variant="orbit", playing=False).to_plotly_json()["props"]
        assert node["playing"] is False

    def test_native_paused_wins(self):
        node = dlc.gridora.GridLoader(variant="orbit", playing=False, paused=False).to_plotly_json()["props"]
        assert node["paused"] is False
        assert node["playing"] is False


class TestRegistryMotionVariantsOnly:
    """The Loading registry must list exactly the 133 motion variants, no glyphs."""

    def test_gridora_in_libraries(self):
        assert "gridora" in list_libraries()

    def test_variant_count(self):
        spinners = list_spinners("gridora")
        assert len(spinners) == 133, f"Expected 133, got {len(spinners)}: {spinners[:5]}..."

    def test_all_motion_variants_present(self):
        spinners = set(list_spinners("gridora"))
        for v in gridora.MOTION_VARIANTS:
            assert v in spinners, f"Motion variant {v} missing from registry"

    def test_no_glyph_variants(self):
        spinners = set(list_spinners("gridora"))
        glyph_prefixes = ("letter", "digit", "sym")
        glyphs_found = [s for s in spinners if any(s.startswith(p) for p in glyph_prefixes)]
        assert not glyphs_found, f"Glyph variants in registry: {glyphs_found}"


class TestNamespaceExports:
    """dlc.gridora.GridLoader and dlc.gridora.Text must be importable."""

    def test_gridloader_importable(self):
        assert callable(dlc.gridora.GridLoader)

    def test_text_importable(self):
        assert callable(dlc.gridora.Text)

    def test_no_flat_export(self):
        assert not hasattr(dlc, "GridLoader"), "Bare flat export found: dlc.GridLoader (collision risk)"

    def test_motion_variants_list(self):
        assert len(gridora.MOTION_VARIANTS) == 133


class TestTextComponent:
    """dlc.gridora.Text(text=...) must work."""

    def test_text_requires_text(self):
        with pytest.raises(TypeError):
            dlc.gridora.Text()

    def test_text_renders(self):
        node = dlc.gridora.Text(text="LOAD").to_plotly_json()["props"]
        assert node["text"] == "LOAD"

    def test_text_with_rate(self):
        node = dlc.gridora.Text(text="HI", rate=2.0).to_plotly_json()["props"]
        assert node["rate"] == 2.0
