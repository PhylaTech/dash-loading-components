"""Namespace for dlc.lab -- PhylaTech's own SVG spinners for science waits.

Unlike the other families these wrap no upstream package: each is drawn here as
SVG and animated with plain CSS, so ``rate`` and ``playing`` need no timer.

``HplcTrace``
    The detector trace of an HPLC or UPLC run, the kind that feeds a mass
    spectrometer: a pen draws the baseline across retention time, compounds
    elute as peaks of their own height, and each apex is marked as it passes.
``WellPlate``
    A 96-well microplate (8 rows by 12 columns, A1 corner cut off) that a
    pipette fills well by well, then empties in the same order.

Usage::

    import dash_loading_components as dlc

    dlc.lab.HplcTrace(size=96, color="#f97316")
    dlc.lab.WellPlate(size=96, rate=1.5)
"""

from ..LabHplcTrace import LabHplcTrace as HplcTrace
from ..LabWellPlate import LabWellPlate as WellPlate

# name -> blurb, in gallery order.
SPINNERS = {
    "HplcTrace": "A liquid chromatography detector trace drawn across retention time, compounds eluting as peaks of their own height.",
    "WellPlate": "A pipette filling a 96-well microplate well by well, row after row, then emptying it in the same order.",
}

__all__ = ["HplcTrace", "WellPlate", "SPINNERS"]
