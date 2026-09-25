"""The flicker presets are data, so they are checked as data.

A preset that breaks one of these still renders, which is why they need a
test: a malformed row makes the player drop the whole spinner, a frame with
no lit dot reads as the loader vanishing, and a preset whose motion lives
only on the outer ring is a still picture at variant="5x5".
"""
import pytest

import dash_loading_components as dlc
from dash_loading_components.flicker import CATEGORIES, PRESETS

CASES = sorted(PRESETS.items())


def inner(frame):
    return tuple(row[1:6] for row in frame[1:6])


@pytest.mark.parametrize("name,preset", CASES)
def test_frames_are_seven_rows_of_seven(name, preset):
    assert preset.frames, name
    for i, frame in enumerate(preset.frames):
        assert len(frame) == 7 and all(len(row) == 7 and set(row) <= {"#", "."} for row in frame), (name, i)


@pytest.mark.parametrize("name,preset", CASES)
def test_every_frame_lights_a_dot(name, preset):
    dark = [i for i, frame in enumerate(preset.frames) if "#" not in "".join(frame)]
    assert not dark, (name, dark)


@pytest.mark.parametrize("name,preset", CASES)
def test_moves_inside_the_5x5_safe_area(name, preset):
    assert len({inner(frame) for frame in preset.frames}) > 1, name


@pytest.mark.parametrize("name,preset", CASES)
def test_loop_wraps_without_a_stutter(name, preset):
    # A last frame equal to the first plays twice in a row at every wrap.
    assert preset.frames[-1] != preset.frames[0], name


def test_no_two_presets_are_the_same_loop():
    loops = {}
    for name, preset in CASES:
        # Same frames from another starting point is the same loop.
        key = min(preset.frames[i:] + preset.frames[:i] for i in range(len(preset.frames)))
        assert key not in loops, (name, loops.get(key))
        loops[key] = name


def test_categories_and_the_naturalist_set():
    assert {p.category for p in PRESETS.values()} == set(CATEGORIES)
    assert sum(p.category == "field" for p in PRESETS.values()) >= 10


@pytest.mark.parametrize("name", sorted(PRESETS))
def test_each_preset_is_the_player_with_its_frames(name):
    node = getattr(dlc.flicker, name)(size=48).to_plotly_json()
    assert node["type"] == "FlickerSpinner"
    assert node["props"]["grids"] == [list(f) for f in PRESETS[name].frames]
    assert dlc.list_spinners("flicker") == list(PRESETS)
