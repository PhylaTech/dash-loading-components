"""Namespace for dlc.gridora — gridora's grid-dot loading animations and text.

``GridLoader`` renders one of 133 motion variants (plus glyph variants) as a
grid of animated dots. ``Text`` renders text using gridora's bitmap font.

Usage::

    import dash_loading_components as dlc

    dlc.gridora.GridLoader(variant="orbit", color="#f97316", rate=1.5)
    dlc.gridora.Text(text="LOAD", color="#f97316")
"""

from ..GridoraGridLoader import GridoraGridLoader as GridLoader
from ..GridoraText import GridoraText as Text

MOTION_VARIANTS = [
    "tokenStream", "attention", "backprop", "compile", "deploy",
    "vectorIndex", "snakeTrail", "columnSnake", "staircase", "streamPair",
    "embedding", "webhook", "cacheWarm", "cron", "orbit",
    "starBurst", "binaryBloom", "ripple", "sonar", "pulseRings",
    "coreOut", "coreIn",
    "sync", "quantize", "authHandshake", "clusterSync", "indexBuild",
    "lattice", "checkerboard", "interlace", "columnBeat", "heartPulse",
    "plusPulse", "snowflake", "meshNetwork", "breathe", "strobe", "metronome",
    "gradientDescent", "bloom", "flowerBloom", "fountain", "avalanche",
    "diffusion", "hash", "constellation", "noise", "dither", "pixelSort", "sparkle",
    "rateLimit", "retryBackoff", "soundBars", "equalizer", "barcode", "countdown",
    "helix", "twinHelix", "swirl", "kaleidoscope", "gyro",
    "beacon", "drift", "elevator", "magnet", "current", "conveyor",
    "circular", "radar", "vortex", "clockHand", "carousel",
    "decrypt", "glitch", "matrix", "scramble", "corrupt", "bitFlip",
    "spiral", "spiralIn", "rain", "firework", "wave", "bounce",
    "pendulum", "shockwave", "supernova", "plasma", "moire",
    "diamond", "arrowRight", "arrowLeft", "triangleUp", "triangleDown",
    "xMark", "frame", "crosshair", "hourglass", "boxOut", "boxIn", "corners",
    "wipeRight", "wipeLeft", "wipeDown", "wipeUp", "wipeDiagonal",
    "curtain", "doors", "iris", "irisOut",
    "tornado", "waterfall", "lightning", "aurora", "galaxy",
    "dna", "flame", "smoke", "ocean", "sandstorm", "vine",
    "typewriter", "domino", "blink", "signal", "pinwheel",
    "zigzag", "checkerWave", "cornerPulse", "jitter", "marquee",
    "seesaw", "orbitDot",
]

CATEGORIES = {
    "sequential": ("Sequential", "patterns that light cells one after another"),
    "radial": ("Radial", "expanding from or converging to a center"),
    "pulse": ("Pulse", "cells beating in rhythm"),
    "cascade": ("Cascade", "waves that wash across the grid"),
    "scatter": ("Scatter", "randomness and noise"),
    "temporal": ("Temporal", "time-related patterns"),
    "rotational": ("Rotational", "spinning and twisting"),
    "flow": ("Flow", "directional movement"),
    "circular": ("Circular", "orbits and rotations"),
    "decrypt": ("Decrypt", "glitch and cipher aesthetics"),
    "special": ("Special", "unique animations"),
    "geometric": ("Geometric", "shapes revealed and concealed"),
    "wipe": ("Wipe", "transitions that sweep across"),
    "organic": ("Organic", "nature-inspired motion"),
    "motion": ("Motion", "kinetic patterns"),
}

VARIANT_CATEGORY = {
    **dict.fromkeys(["tokenStream", "attention", "backprop", "compile", "deploy",
                      "vectorIndex", "snakeTrail", "columnSnake", "staircase", "streamPair"], "sequential"),
    **dict.fromkeys(["embedding", "webhook", "cacheWarm", "cron", "orbit",
                      "starBurst", "binaryBloom", "ripple", "sonar", "pulseRings",
                      "coreOut", "coreIn"], "radial"),
    **dict.fromkeys(["sync", "quantize", "authHandshake", "clusterSync", "indexBuild",
                      "lattice", "checkerboard", "interlace", "columnBeat", "heartPulse",
                      "plusPulse", "snowflake", "meshNetwork", "breathe", "strobe", "metronome"], "pulse"),
    **dict.fromkeys(["gradientDescent", "bloom", "flowerBloom", "fountain", "avalanche"], "cascade"),
    **dict.fromkeys(["diffusion", "hash", "constellation", "noise", "dither", "pixelSort", "sparkle"], "scatter"),
    **dict.fromkeys(["rateLimit", "retryBackoff", "soundBars", "equalizer", "barcode", "countdown"], "temporal"),
    **dict.fromkeys(["helix", "twinHelix", "swirl", "kaleidoscope", "gyro"], "rotational"),
    **dict.fromkeys(["beacon", "drift", "elevator", "magnet", "current", "conveyor"], "flow"),
    **dict.fromkeys(["circular", "radar", "vortex", "clockHand", "carousel"], "circular"),
    **dict.fromkeys(["decrypt", "glitch", "matrix", "scramble", "corrupt", "bitFlip"], "decrypt"),
    **dict.fromkeys(["spiral", "spiralIn", "rain", "firework", "wave", "bounce",
                      "pendulum", "shockwave", "supernova", "plasma", "moire"], "special"),
    **dict.fromkeys(["diamond", "arrowRight", "arrowLeft", "triangleUp", "triangleDown",
                      "xMark", "frame", "crosshair", "hourglass", "boxOut", "boxIn", "corners"], "geometric"),
    **dict.fromkeys(["wipeRight", "wipeLeft", "wipeDown", "wipeUp", "wipeDiagonal",
                      "curtain", "doors", "iris", "irisOut"], "wipe"),
    **dict.fromkeys(["tornado", "waterfall", "lightning", "aurora", "galaxy",
                      "dna", "flame", "smoke", "ocean", "sandstorm", "vine"], "organic"),
    **dict.fromkeys(["typewriter", "domino", "blink", "signal", "pinwheel",
                      "zigzag", "checkerWave", "cornerPulse", "jitter", "marquee",
                      "seesaw", "orbitDot"], "motion"),
}

__all__ = ["GridLoader", "Text", "MOTION_VARIANTS", "CATEGORIES", "VARIANT_CATEGORY"]
