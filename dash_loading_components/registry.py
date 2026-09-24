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
# speed=1.0 means "this spinner's normal tempo", never a shared physical unit.
# ---------------------------------------------------------------------------

# Families whose native tempo prop is a *period*: one full animation loop.
# Larger native value = slower, so native = normal_period / speed.
#   loading-dev ``duration``           milliseconds
#   react-epic-spinners ``animationDuration``  milliseconds
#   ldrs ``speed``                     seconds (upstream's own wording)
#   premium-react-loaders ``speed``    milliseconds (clamped 50-10000 upstream)
_PERIOD_FAMILIES = {
    "loading_dev": "duration",
    "epic": "animationDuration",
    "ldrs": "speed",
    "premium": "speed",
}

# The native period each spinner runs at with the prop omitted, i.e. what
# relative speed 1.0 must reproduce. Transcribed from upstream:
#   loading-dev      SPINNER_MOTION  (dist/motion.d.ts)
#   ldrs             applyDefaultProps in each dist/elements/<name>.js
#   react-epic-spinners  per-component animationDuration default prop
# A family whose upstream tempo really is one constant lives in
# _FAMILY_PERIOD instead; anything absent from both falls back to 1000.
_SPINNER_PERIOD: dict[str, dict[str, float]] = {
    # milliseconds
    "loading_dev": {
        "Arc": 800,
        "Atom": 1000,
        "Blocks": 1300,
        "BouncingDots": 500,
        "Cascade": 1500,
        "CircularDots": 800,
        "Classic": 1200,
        "ClassicV2": 800,
        "Clock": 1200,
        "Comet": 700,
        "Compass": 500,
        "Dual": 1000,
        "Eclipse": 1200,
        "Flip": 1200,
        "Gather": 1600,
        "Leap": 1800,
        "LinearDots": 900,
        "Loading": 1000,
        "Morph": 1200,
        "Orbit": 750,
        "Pulse": 1200,
        "Radar": 1500,
        "Ring": 800,
        "Ripple": 1200,
        "Slide": 2400,
        "Snake": 1400,
        "Swirl": 1200,
        "Trace": 1200,
        "Wave": 900,
    },
    # seconds
    "ldrs": {
        "DotPulse": 1.3,
        "DotWave": 1.0,
        "Helix": 2.5,
        "Hourglass": 1.75,
        "Infinity": 1.3,
        "Jelly": 0.9,
        "LineSpinner": 1.0,
        "Mirage": 2.5,
        "Orbit": 1.5,
        "Ping": 2.0,
        "Quantum": 1.75,
        "Ring": 2.0,
    },
    # milliseconds
    "epic": {
        "AtomSpinner": 1000,
        "FlowerSpinner": 2500,
        "HollowDotsSpinner": 1000,
        "OrbitSpinner": 1000,
        "RadarSpinner": 2000,
        "SemipolarSpinner": 2000,
        "SpringSpinner": 3000,
        "TrinityRingsSpinner": 1500,
    },
}

# Families where every spinner shares one normal period.
# premium resolves the ``"normal"`` token to 1s for all loaders
# (getAnimationDuration in dist/index4.js).
_FAMILY_PERIOD: dict[str, float] = {
    "premium": 1000,
}

# Fallback period when a spinner is missing from the tables above, and the
# period assumed when the caller does not say which spinner it is building.
DEFAULT_PERIOD_MS = 1000

# Families whose native tempo is a unitless multiplier (1.0 = normal)
_MULTIPLIER_FAMILIES = {
    "m3": "speed",
    "spinners": "speedMultiplier",
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
    if library in _PERIOD_FAMILIES:
        return _PERIOD_FAMILIES[library]
    if library in _MULTIPLIER_FAMILIES:
        return _MULTIPLIER_FAMILIES[library]
    if library in _PERCENT_FAMILIES:
        return _PERCENT_FAMILIES[library]
    if library == "indicators":
        return _INDICATORS_PROP
    return None


def supports_relative_speed(library: str) -> bool:
    return native_tempo_prop(library) is not None


def normal_period(library: str, spinner: Optional[str] = None) -> float:
    """Native period a spinner runs at with its tempo prop omitted.

    The unit is the family's own (ms for loading-dev / epic / premium,
    seconds for ldrs). Only meaningful for ``_PERIOD_FAMILIES``.
    """
    if spinner is not None:
        per_spinner = _SPINNER_PERIOD.get(library)
        if per_spinner and spinner in per_spinner:
            return per_spinner[spinner]
    if library in _FAMILY_PERIOD:
        return _FAMILY_PERIOD[library]
    return DEFAULT_PERIOD_MS


def _tidy(value: float) -> Any:
    """Whole numbers as ``int``; otherwise round off float noise."""
    if abs(value - round(value)) < 1e-9:
        return int(round(value))
    return round(value, 4)


def translate_relative_speed(
    library: str, speed: float, spinner: Optional[str] = None
) -> dict[str, Any]:
    """Translate relative ``speed`` (1.0 = normal) into native prop kwargs.

    ``spinner`` is required to hit the right baseline for families whose
    normal tempo is per-spinner (loading-dev, ldrs, epic). Omitting it falls
    back to the family default, which is only correct for premium.

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

    if library in _PERIOD_FAMILIES:
        # Faster relative speed means a shorter loop, so divide the baseline.
        prop = _PERIOD_FAMILIES[library]
        return {prop: _tidy(normal_period(library, spinner) / speed_f)}

    if library in _MULTIPLIER_FAMILIES:
        prop = _MULTIPLIER_FAMILIES[library]
        return {prop: speed_f}

    if library in _PERCENT_FAMILIES:
        prop = _PERCENT_FAMILIES[library]
        return {prop: _tidy(100.0 * speed_f)}

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
