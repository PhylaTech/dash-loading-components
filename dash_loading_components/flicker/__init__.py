"""Namespace for dlc.flicker — flicker-dot's player and PhylaTech's presets.

``Spinner`` is the player: give it ``grids``. Every other name here is a
preset, the player with its frames filled in; see ``presets.py``.
"""

from ..FlickerSpinner import FlickerSpinner as Spinner
from ..FlickerWellPlate import FlickerWellPlate as WellPlate
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
MassSpec = _preset("MassSpec")
Jellyfish = _preset("Jellyfish")
TestTube = _preset("TestTube")
Fish = _preset("Fish")
Snail = _preset("Snail")
Leaf = _preset("Leaf")
Ant = _preset("Ant")
Frond = _preset("Frond")
Diatom = _preset("Diatom")
Cladogram = _preset("Cladogram")
Helix = _preset("Helix")
Colony = _preset("Colony")
Waggle = _preset("Waggle")
Mitosis = _preset("Mitosis")
Seedling = _preset("Seedling")
Chromatogram = _preset("Chromatogram")
HplcTrace = _preset("HplcTrace")
Scatter = _preset("Scatter")
Histogram = _preset("Histogram")
PieChart = _preset("PieChart")
Heatmap = _preset("Heatmap")
LineChart = _preset("LineChart")
Database = _preset("Database")
Cart = _preset("Cart")
Upload = _preset("Upload")
Magnifier = _preset("Magnifier")
Download = _preset("Download")
Mail = _preset("Mail")
Wifi = _preset("Wifi")
Battery = _preset("Battery")
Truck = _preset("Truck")
Bell = _preset("Bell")
Heart = _preset("Heart")
Chat = _preset("Chat")
CloudSync = _preset("CloudSync")
Lock = _preset("Lock")
Departures = _preset("Departures")
SplitFlap = _preset("SplitFlap")
Marquee = _preset("Marquee")
Scanline = _preset("Scanline")
Equalizer = _preset("Equalizer")
Typewriter = _preset("Typewriter")
Rain = _preset("Rain")
Stack = _preset("Stack")
Bricklayer = _preset("Bricklayer")
Orbit = _preset("Orbit")
Pinwheel = _preset("Pinwheel")
Beacon = _preset("Beacon")
Rebound = _preset("Rebound")
Coil = _preset("Coil")
Sandglass = _preset("Sandglass")
Sweep = _preset("Sweep")
Lemniscate = _preset("Lemniscate")
Tetrahedron = _preset("Tetrahedron")
Cube = _preset("Cube")
Octahedron = _preset("Octahedron")
Dodecahedron = _preset("Dodecahedron")
Icosahedron = _preset("Icosahedron")

# Spinners that draw themselves as SVG instead of playing frames on the 7x7
# grid, which has no room for them: name -> (category, blurb). They take their
# own props, not the player's.
DRAWN = {
    "WellPlate": ("field", "A pipette filling a 96-well microplate well by well, row after row, then emptying it in the same order."),
}


def category_of(name: str) -> str:
    return PRESETS[name].category if name in PRESETS else DRAWN[name][0]


def blurb_of(name: str) -> str:
    return PRESETS[name].blurb if name in PRESETS else DRAWN[name][1]


__all__ = ['Spinner', 'WellPlate', 'PRESETS', 'DRAWN', 'CATEGORIES', 'Preset', *PRESETS]
