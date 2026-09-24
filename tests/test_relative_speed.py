"""Relative ``speed`` must reproduce each spinner's own upstream tempo.

``speed=1.0`` is documented as "this spinner's normal tempo". For families
whose native tempo prop is an absolute period (loading-dev ``duration``,
epic ``animationDuration``, ldrs ``speed``) that baseline differs per
spinner, so a single family-wide constant silently retimes most of the
catalog. These expectations are transcribed from the upstream packages and
are the reason ``translate_relative_speed`` takes a spinner name.
"""
import pytest

from dash_loading_components.registry import (
    list_spinners,
    native_tempo_prop,
    supports_relative_speed,
    translate_relative_speed,
)

# Upstream tempo with the prop omitted, in the family's native unit.
#   loading_dev: SPINNER_MOTION in loading-dev/dist/motion.d.ts (ms)
#   ldrs:        applyDefaultProps in ldrs/dist/elements/<name>.js (seconds)
#   epic:        per-component animationDuration default (ms)
UPSTREAM_NORMAL = {
    "loading_dev": {
        "Arc": 800, "Atom": 1000, "Blocks": 1300, "BouncingDots": 500,
        "Cascade": 1500, "CircularDots": 800, "Classic": 1200,
        "ClassicV2": 800, "Clock": 1200, "Comet": 700, "Compass": 500,
        "Dual": 1000, "Eclipse": 1200, "Flip": 1200, "Gather": 1600,
        "Leap": 1800, "LinearDots": 900, "Loading": 1000, "Morph": 1200,
        "Orbit": 750, "Pulse": 1200, "Radar": 1500, "Ring": 800,
        "Ripple": 1200, "Slide": 2400, "Snake": 1400, "Swirl": 1200,
        "Trace": 1200, "Wave": 900,
    },
    "ldrs": {
        "DotPulse": 1.3, "DotWave": 1.0, "Helix": 2.5, "Hourglass": 1.75,
        "Infinity": 1.3, "Jelly": 0.9, "LineSpinner": 1.0, "Mirage": 2.5,
        "Orbit": 1.5, "Ping": 2.0, "Quantum": 1.75, "Ring": 2.0,
    },
    "epic": {
        "AtomSpinner": 1000, "FlowerSpinner": 2500, "HollowDotsSpinner": 1000,
        "OrbitSpinner": 1000, "RadarSpinner": 2000, "SemipolarSpinner": 2000,
        "SpringSpinner": 3000, "TrinityRingsSpinner": 1500,
    },
    # premium resolves its "normal" token to 1s for every loader
    "premium": {
        "SpinnerCircle": 1000, "SpinnerRing": 1000, "SpinnerDots": 1000,
        "SpinnerBars": 1000, "OrbitDots": 1000, "OrbitRings": 1000,
        "AtomLoader": 1000, "PulseDots": 1000, "PulseWave": 1000,
        "BouncingDots": 1000, "InfinityLoader": 1000, "MobiusLoader": 1000,
        "ShimmerBox": 1000, "ButtonSpinner": 1000, "SuccessCheckmark": 1000,
    },
}

PERIOD_CASES = [
    (family, spinner, normal)
    for family, spinners in UPSTREAM_NORMAL.items()
    for spinner, normal in spinners.items()
]


@pytest.mark.parametrize("family,spinner,normal", PERIOD_CASES)
def test_speed_one_matches_upstream_normal(family, spinner, normal):
    prop = native_tempo_prop(family)
    assert translate_relative_speed(family, 1.0, spinner) == {prop: normal}


@pytest.mark.parametrize("family,spinner,normal", PERIOD_CASES)
def test_doubling_speed_halves_the_period(family, spinner, normal):
    """Period families are inverted: faster speed means a *smaller* native value."""
    prop = native_tempo_prop(family)
    assert translate_relative_speed(family, 2.0, spinner)[prop] == pytest.approx(
        normal / 2
    )


@pytest.mark.parametrize("family", sorted(UPSTREAM_NORMAL))
def test_every_registered_spinner_has_a_baseline(family):
    """A spinner missing here would silently fall back to the generic 1000."""
    assert set(list_spinners(family)) == set(UPSTREAM_NORMAL[family])


@pytest.mark.parametrize(
    "family,expected",
    [
        ("spinners", {"speedMultiplier": 2.0}),
        ("m3", {"speed": 2.0}),
        ("spinners_react", {"speed": 200}),
        ("indicators", {"speedPlus": 5}),
    ],
)
def test_relative_families_are_unchanged(family, expected):
    """Families whose native unit is already relative keep pass-through semantics."""
    assert translate_relative_speed(family, 2.0, None) == expected


def test_families_without_a_tempo_prop_get_nothing():
    assert not supports_relative_speed("loader_spinner")
    assert translate_relative_speed("loader_spinner", 2.0, "Oval") == {}
