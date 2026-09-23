"""Shared (library, spinner) → component registry and relative-speed translation.

Used by ``dlc.Loading`` and the local gallery so IDs stay in sync.
"""
from __future__ import annotations

from typing import Any, Callable, Optional

from . import (
    epic,
    indicators,
    ldrs,
    loader_spinner,
    loading_dev,
    m3,
    premium,
    spinners,
    spinners_react,
)

# ---------------------------------------------------------------------------
# Catalog — same IDs the gallery uses
# ---------------------------------------------------------------------------

FAMILIES: list[tuple[str, str, list[tuple[str, Callable]]]] = [
    (
        "loading_dev",
        "loading-dev",
        [
            ("Arc", loading_dev.Arc),
            ("Atom", loading_dev.Atom),
            ("Orbit", loading_dev.Orbit),
            ("Wave", loading_dev.Wave),
            ("Ring", loading_dev.Ring),
            ("Pulse", loading_dev.Pulse),
            ("Cascade", loading_dev.Cascade),
            ("Comet", loading_dev.Comet),
            ("Morph", loading_dev.Morph),
            ("Loading", loading_dev.Loading),
            ("Blocks", loading_dev.Blocks),
            ("Clock", loading_dev.Clock),
            ("Dual", loading_dev.Dual),
            ("Eclipse", loading_dev.Eclipse),
            ("Radar", loading_dev.Radar),
            ("Ripple", loading_dev.Ripple),
            ("Snake", loading_dev.Snake),
            ("Swirl", loading_dev.Swirl),
            ("Trace", loading_dev.Trace),
            ("Flip", loading_dev.Flip),
            ("Gather", loading_dev.Gather),
            ("Leap", loading_dev.Leap),
            ("Slide", loading_dev.Slide),
            ("Classic", loading_dev.Classic),
            ("ClassicV2", loading_dev.ClassicV2),
            ("Compass", loading_dev.Compass),
            ("BouncingDots", loading_dev.BouncingDots),
            ("CircularDots", loading_dev.CircularDots),
            ("LinearDots", loading_dev.LinearDots),
        ],
    ),
    (
        "ldrs",
        "ldrs",
        [
            ("Ring", ldrs.Ring),
            ("Helix", ldrs.Helix),
            ("DotPulse", ldrs.DotPulse),
            ("LineSpinner", ldrs.LineSpinner),
            ("Orbit", ldrs.Orbit),
            ("Quantum", ldrs.Quantum),
            ("Jelly", ldrs.Jelly),
            ("Infinity", ldrs.Infinity),
            ("Hourglass", ldrs.Hourglass),
            ("DotWave", ldrs.DotWave),
            ("Mirage", ldrs.Mirage),
            ("Ping", ldrs.Ping),
        ],
    ),
    (
        "spinners",
        "react-spinners",
        [
            ("ClipLoader", spinners.ClipLoader),
            ("BeatLoader", spinners.BeatLoader),
            ("HashLoader", spinners.HashLoader),
            ("SyncLoader", spinners.SyncLoader),
            ("PropagateLoader", spinners.PropagateLoader),
            ("PulseLoader", spinners.PulseLoader),
            ("ScaleLoader", spinners.ScaleLoader),
            ("MoonLoader", spinners.MoonLoader),
            ("BarLoader", spinners.BarLoader),
            ("RingLoader", spinners.RingLoader),
            ("BounceLoader", spinners.BounceLoader),
            ("GridLoader", spinners.GridLoader),
        ],
    ),
    (
        "spinners_react",
        "spinners-react",
        [
            ("SpinnerCircular", spinners_react.SpinnerCircular),
            ("SpinnerCircularFixed", spinners_react.SpinnerCircularFixed),
            ("SpinnerCircularSplit", spinners_react.SpinnerCircularSplit),
            ("SpinnerInfinity", spinners_react.SpinnerInfinity),
            ("SpinnerDotted", spinners_react.SpinnerDotted),
            ("SpinnerRound", spinners_react.SpinnerRound),
            ("SpinnerRoundOutlined", spinners_react.SpinnerRoundOutlined),
            ("SpinnerRoundFilled", spinners_react.SpinnerRoundFilled),
            ("SpinnerDiamond", spinners_react.SpinnerDiamond),
        ],
    ),
    (
        "loader_spinner",
        "react-loader-spinner",
        [
            ("TailSpin", loader_spinner.TailSpin),
            ("Oval", loader_spinner.Oval),
            ("ThreeDots", loader_spinner.ThreeDots),
            ("Rings", loader_spinner.Rings),
            ("BallTriangle", loader_spinner.BallTriangle),
            ("Grid", loader_spinner.Grid),
            ("DNA", loader_spinner.DNA),
            ("InfinitySpin", loader_spinner.InfinitySpin),
            ("Circles", loader_spinner.Circles),
            ("Hourglass", loader_spinner.Hourglass),
        ],
    ),
    (
        "premium",
        "premium-react-loaders",
        [
            ("SpinnerCircle", premium.SpinnerCircle),
            ("SpinnerRing", premium.SpinnerRing),
            ("SpinnerDots", premium.SpinnerDots),
            ("SpinnerBars", premium.SpinnerBars),
            ("OrbitDots", premium.OrbitDots),
            ("OrbitRings", premium.OrbitRings),
            ("AtomLoader", premium.AtomLoader),
            ("PulseDots", premium.PulseDots),
            ("PulseWave", premium.PulseWave),
            ("BouncingDots", premium.BouncingDots),
            ("InfinityLoader", premium.InfinityLoader),
            ("MobiusLoader", premium.MobiusLoader),
            ("ShimmerBox", premium.ShimmerBox),
            ("ButtonSpinner", premium.ButtonSpinner),
            ("SuccessCheckmark", premium.SuccessCheckmark),
        ],
    ),
    (
        "indicators",
        "react-loading-indicators",
        [
            ("Atom", indicators.Atom),
            ("BlinkBlur", indicators.BlinkBlur),
            ("Commet", indicators.Commet),
            ("FourSquare", indicators.FourSquare),
            ("LifeLine", indicators.LifeLine),
            ("Mosaic", indicators.Mosaic),
            ("OrbitProgress", indicators.OrbitProgress),
            ("Riple", indicators.Riple),
            ("Slab", indicators.Slab),
            ("ThreeDot", indicators.ThreeDot),
            ("TrophySpin", indicators.TrophySpin),
        ],
    ),
    (
        "m3",
        "@alerix/m3-loading-indicator",
        [("LoadingIndicator", m3.LoadingIndicator)],
    ),
    (
        "epic",
        "react-epic-spinners",
        [
            ("AtomSpinner", epic.AtomSpinner),
            ("OrbitSpinner", epic.OrbitSpinner),
            ("FlowerSpinner", epic.FlowerSpinner),
            ("TrinityRingsSpinner", epic.TrinityRingsSpinner),
            ("HollowDotsSpinner", epic.HollowDotsSpinner),
            ("SpringSpinner", epic.SpringSpinner),
            ("SemipolarSpinner", epic.SemipolarSpinner),
            ("RadarSpinner", epic.RadarSpinner),
        ],
    ),
]

FAMILY_LOOKUP = {key: (label, items) for key, label, items in FAMILIES}
COMPONENT_LOOKUP: dict[tuple[str, str], Callable] = {
    (key, name): component
    for key, _label, items in FAMILIES
    for name, component in items
}

# ---------------------------------------------------------------------------
# Relative speed → native prop translation
# speed=1.0 means "that family's normal tempo" — never a shared physical unit.
# ---------------------------------------------------------------------------

# Base cycle length (ms) for duration-style families at relative speed 1.0
DURATION_BASE_MS = 1000

# Families whose native tempo prop is a duration in ms: native = base_ms / speed
_DURATION_FAMILIES = {
    "loading_dev": "duration",
    "epic": "animationDuration",
}

# Families whose native tempo is a unitless multiplier (1.0 = normal)
_MULTIPLIER_FAMILIES = {
    "ldrs": "speed",
    "m3": "speed",
    "spinners": "speedMultiplier",
}

# premium-react-loaders: native ``speed`` is a token OR duration in **ms**
# (numbers are clamped 50–10000ms). Relative 1.0 → 1000ms (= upstream "normal").
_MS_SPEED_FAMILIES = {
    "premium": "speed",
}

# spinners-react: native speed is percent of default (100 = normal)
_PERCENT_FAMILIES = {
    "spinners_react": "speed",
}

# indicators: speedPlus in [-5, 5], 0 = normal
# Map: speedPlus = clamp(round((speed - 1.0) * 5), -5, 5)
#   speed=1.0 → 0; speed=2.0 → 5; speed=0.5 → -2 (approx)
_INDICATORS_PROP = "speedPlus"
_INDICATORS_SCALE = 5

# Native tempo kwarg names that conflict with relative ``speed`` on Loading(...)
NATIVE_TEMPO_CONFLICT_KEYS = frozenset(
    {
        "duration",
        "speedMultiplier",
        "speedPlus",
        "animationDuration",
    }
)


def list_libraries() -> list[str]:
    return [key for key, _label, _items in FAMILIES]


def list_spinners(library: str) -> list[str]:
    if library not in FAMILY_LOOKUP:
        raise ValueError(
            f"Unknown library {library!r}. Known: {', '.join(list_libraries())}"
        )
    return [name for name, _comp in FAMILY_LOOKUP[library][1]]


def get_component(library: str, spinner: str) -> Callable:
    key = (library, spinner)
    if library not in FAMILY_LOOKUP:
        raise ValueError(
            f"Unknown library {library!r}. Known libraries: "
            f"{', '.join(list_libraries())}. See the local gallery for IDs."
        )
    if key not in COMPONENT_LOOKUP:
        known = ", ".join(list_spinners(library))
        raise ValueError(
            f"Unknown spinner {spinner!r} for library {library!r}. "
            f"Known for {library}: {known}"
        )
    return COMPONENT_LOOKUP[key]


def native_tempo_prop(library: str) -> Optional[str]:
    """Return the upstream tempo prop name for ``library``, or None if unsupported."""
    if library in _DURATION_FAMILIES:
        return _DURATION_FAMILIES[library]
    if library in _MS_SPEED_FAMILIES:
        return _MS_SPEED_FAMILIES[library]
    if library in _MULTIPLIER_FAMILIES:
        return _MULTIPLIER_FAMILIES[library]
    if library in _PERCENT_FAMILIES:
        return _PERCENT_FAMILIES[library]
    if library == "indicators":
        return _INDICATORS_PROP
    return None


def supports_relative_speed(library: str) -> bool:
    return native_tempo_prop(library) is not None


def translate_relative_speed(library: str, speed: float) -> dict[str, Any]:
    """Translate relative ``speed`` (1.0 = normal) into native prop kwargs.

    Returns ``{}`` when the family has no tempo prop (do not invent one).
    """
    if speed is None:
        return {}
    try:
        speed_f = float(speed)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"speed must be a number, got {speed!r}") from exc
    if speed_f <= 0:
        raise ValueError(f"speed must be > 0, got {speed_f}")

    if library in _DURATION_FAMILIES:
        prop = _DURATION_FAMILIES[library]
        # Faster relative speed → shorter cycle
        value = DURATION_BASE_MS / speed_f
        # Prefer int ms when close to whole milliseconds
        if abs(value - round(value)) < 1e-9:
            value = int(round(value))
        return {prop: value}

    if library in _MS_SPEED_FAMILIES:
        # Same formula as duration families; prop name is still ``speed``
        prop = _MS_SPEED_FAMILIES[library]
        value = DURATION_BASE_MS / speed_f
        if abs(value - round(value)) < 1e-9:
            value = int(round(value))
        return {prop: value}

    if library in _MULTIPLIER_FAMILIES:
        prop = _MULTIPLIER_FAMILIES[library]
        return {prop: speed_f}

    if library in _PERCENT_FAMILIES:
        prop = _PERCENT_FAMILIES[library]
        native = 100.0 * speed_f
        if abs(native - round(native)) < 1e-9:
            native = int(round(native))
        return {prop: native}

    if library == "indicators":
        # Documented scale: speedPlus = clamp(round((speed - 1) * 5), -5, 5)
        raw = round((speed_f - 1.0) * _INDICATORS_SCALE)
        clamped = int(max(-5, min(5, raw)))
        return {_INDICATORS_PROP: clamped}

    return {}


def playing_kwargs(library: str, playing: bool) -> dict[str, Any]:
    """Map common ``playing`` to a family-native pause/run prop when supported."""
    if library == "loading_dev":
        return {"playState": "running" if playing else "paused"}
    if library == "m3":
        return {"paused": not playing}
    if library == "spinners":
        return {"loading": playing}
    if library == "spinners_react":
        return {"enabled": playing}
    if library == "loader_spinner":
        return {"visible": playing}
    return {}
