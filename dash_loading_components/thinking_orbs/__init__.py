"""Namespace for dlc.thinking_orbs -- dotted canvas orbs from thinking-orbs.

``Orb`` renders one of nine named states an AI or agent can be in, as a
dotted sphere on a plain 2D canvas: ``working``, ``searching``, ``solving``,
``listening``, ``connecting``, ``weaving``, ``composing``, ``breathing`` and
``shaping``. The ink is monochrome by default (light on dark pages, dark on
light ones); ``color`` tints it.

Usage::

    import dash_loading_components as dlc

    dlc.thinking_orbs.Orb(state="searching", size=64)
    dlc.thinking_orbs.Orb(state="solving", size=20, color="#f97316", rate=1.5)
"""

from ..ThinkingOrbsOrb import ThinkingOrbsOrb as Orb

ORB_STATES = [
    "working", "searching", "solving", "listening", "connecting",
    "weaving", "composing", "breathing", "shaping",
]

__all__ = ["Orb", "ORB_STATES"]
