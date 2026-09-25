"""Namespace for dlc.flicker — flicker-dot's player and PhylaTech's presets.

``Spinner`` is the player: give it ``grids``. Every other name here is a
preset, the player with its frames filled in; see ``presets.py``.
"""

from ..FlickerSpinner import FlickerSpinner as Spinner
from .presets import CATEGORIES, PRESETS, Preset


def _preset(name: str):
    preset = PRESETS[name]

    def component(**kwargs) -> Spinner:
        return Spinner(grids=[list(frame) for frame in preset.frames], **kwargs)

    component.__name__ = component.__qualname__ = name
    component.__doc__ = (
        f"{preset.blurb}\n\n"
        f"dlc.flicker.Spinner playing the {name} preset; takes every Spinner prop but grids."
    )
    return component


Mycelium = _preset("Mycelium")
SporeRing = _preset("SporeRing")
Firefly = _preset("Firefly")
Tide = _preset("Tide")
Osculum = _preset("Osculum")
Frond = _preset("Frond")
Diatom = _preset("Diatom")
Cladogram = _preset("Cladogram")
Helix = _preset("Helix")
Colony = _preset("Colony")
Waggle = _preset("Waggle")
Mitosis = _preset("Mitosis")
Seedling = _preset("Seedling")
Chromatogram = _preset("Chromatogram")
Departures = _preset("Departures")
SplitFlap = _preset("SplitFlap")
Marquee = _preset("Marquee")
Scanline = _preset("Scanline")
Equalizer = _preset("Equalizer")
Typewriter = _preset("Typewriter")
Rain = _preset("Rain")
Stack = _preset("Stack")
Orbit = _preset("Orbit")
Pinwheel = _preset("Pinwheel")
Beacon = _preset("Beacon")
Rebound = _preset("Rebound")
Coil = _preset("Coil")
Sandglass = _preset("Sandglass")
Sweep = _preset("Sweep")
Lemniscate = _preset("Lemniscate")

__all__ = ['Spinner', 'PRESETS', 'CATEGORIES', 'Preset', *PRESETS]
