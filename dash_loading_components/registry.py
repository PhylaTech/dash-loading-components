"""Catalog of every family and spinner, in gallery order.

The common props (size, color, rate, playing) live on the components
themselves; the translation of ``rate`` into each family's native tempo prop
is in src/lib/contract.js.
"""
from __future__ import annotations

from typing import Callable

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
