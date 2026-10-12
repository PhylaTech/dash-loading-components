"""Namespace for dlc.loadersz -- canvas-based loading indicators from loadersz.

``Loader`` renders one of 160 semantic state animations on a hardware-
accelerated canvas. States range from product loaders (``loading``,
``buffering``) through reasoning indicators (``searching``, ``pondering``)
to chart-shaped data visualisations (``heatmapping``, ``sankeying``,
``treemapping``, ``candlesticking``, ``bar-charting``).

Usage::

    import dash_loading_components as dlc

    dlc.loadersz.Loader(state="searching", size=96, color="#f97316", rate=1.5)
    dlc.loadersz.Loader(state="heatmapping", size=144, theme="dark")
"""

from ..LoaderszLoader import LoaderszLoader as Loader

LOADER_STATES = [
    "working", "searching", "connecting", "weaving", "shaping",
    "listening", "breathing", "composing", "solving", "observing",
    "dreaming", "charging", "flowing", "awakening", "coding",
    "transcending", "singing", "growing", "blooming", "wandering",
    "decoding", "calibrating", "attracting", "shattering", "crystallizing",
    "constellating", "folding", "echoing", "balancing", "weathering",
    "mapping", "forging", "orbiting", "racing", "bubbling",
    "spinning", "electrifying", "flocking", "throbbing", "cascading",
    "spiraling", "juggling", "eclipsing", "resonating", "condensing",
    "dispersing", "prisming", "levitating", "synchronizing", "unraveling",
    "pondering", "deducing", "branching", "focusing", "reflecting",
    "weighing", "recalling", "tracing", "converging", "questioning",
    "glimmering", "radiating", "harmonizing", "twinkling", "flickering",
    "shimmering", "surfacing", "vibrating", "illuminating", "sparkling",
    "loading", "buffering", "typing", "processing", "synthesizing",
    "considering", "uploading", "queuing", "associating", "evaluating",
    "reasoning", "exploring", "linking", "resolving", "imagining",
    "settling", "loading-bars", "progressing", "placeholder", "monitoring",
    "checking", "tracking", "waiting", "pulsing", "signaling",
    "stepping", "streaming", "equalizing", "wiring", "marqueeing",
    "orbiting-dots", "charting", "plotting", "sampling", "forecasting",
    "metering", "image-decoding", "unblurring", "rendering", "denoising",
    "upscaling", "segmenting", "masking", "inpainting", "interpolating",
    "heatmapping", "candlesticking", "graphing", "waterfalling", "clustering",
    "indexing", "benchmarking", "profiling", "binning", "aggregating",
    "scrubbing", "telemetry", "polling", "correlating", "routing",
    "bar-charting", "comparing", "accumulating", "sequencing", "transmitting",
    "summarizing", "gauging", "funneling", "treemapping", "areamapping",
    "downloading", "retrying", "scanning", "compiling", "paginating",
    "bubble-charting", "sankeying", "radaring", "scheduling", "calendarizing",
    "bulletting", "boxing", "dispatching", "batching", "checkpointing",
    "prioritizing", "verifying", "pendulating", "drifting", "raining",
]

CATEGORIES = {
    "loaders": ("Loaders", "product loading states"),
    "systems": ("Systems", "system and infrastructure states"),
    "data": ("Data visualizations", "chart-shaped and telemetry loaders"),
    "reasoning": ("Reasoning", "thinking and reasoning indicators"),
    "atmosphere": ("Atmosphere", "ambient and atmospheric effects"),
    "motion": ("Motion studies", "kinetic and exploratory animations"),
}

_CATEGORY_STATES = {
    "loaders": [
        "loading", "buffering", "typing", "processing", "loading-bars",
        "progressing", "placeholder", "waiting", "pulsing", "downloading",
        "retrying", "scanning", "compiling", "paginating",
    ],
    "systems": [
        "uploading", "queuing", "signaling", "stepping", "wiring",
        "marqueeing", "orbiting-dots", "dispatching", "batching",
        "checkpointing", "prioritizing", "verifying",
    ],
    "data": [
        "monitoring", "checking", "tracking", "streaming", "equalizing",
        "charting", "plotting", "sampling", "forecasting", "metering",
        "image-decoding", "unblurring", "rendering", "denoising", "upscaling",
        "segmenting", "masking", "inpainting", "interpolating", "heatmapping",
        "candlesticking", "graphing", "waterfalling", "clustering", "indexing",
        "benchmarking", "profiling", "binning", "aggregating", "scrubbing",
        "telemetry", "polling", "correlating", "routing", "bar-charting",
        "comparing", "accumulating", "sequencing", "transmitting", "summarizing",
        "gauging", "funneling", "treemapping", "bubble-charting", "areamapping",
        "sankeying", "radaring", "scheduling", "calendarizing", "bulletting",
        "boxing",
    ],
    "reasoning": [
        "breathing", "listening", "connecting", "searching", "observing",
        "shaping", "weaving", "pondering", "deducing", "branching",
        "focusing", "reflecting", "weighing", "recalling", "tracing",
        "converging", "questioning", "considering", "associating", "evaluating",
        "reasoning", "exploring", "linking", "resolving", "imagining",
        "settling",
    ],
    "atmosphere": [
        "glimmering", "radiating", "harmonizing", "twinkling", "flickering",
        "shimmering", "surfacing", "vibrating", "illuminating", "sparkling",
        "raining",
    ],
    "motion": [
        "working", "composing", "solving", "dreaming", "charging", "flowing",
        "awakening", "coding", "transcending", "singing", "growing", "blooming",
        "wandering", "decoding", "calibrating", "attracting", "shattering",
        "crystallizing", "constellating", "folding", "echoing", "balancing",
        "weathering", "mapping", "forging", "orbiting", "racing", "bubbling",
        "spinning", "electrifying", "flocking", "throbbing", "cascading",
        "spiraling", "juggling", "eclipsing", "resonating", "condensing",
        "dispersing", "prisming", "levitating", "synchronizing", "unraveling",
        "synthesizing", "pendulating", "drifting",
    ],
}

STATE_CATEGORY = {}
for _cat, _states in _CATEGORY_STATES.items():
    for _s in _states:
        STATE_CATEGORY[_s] = _cat

__all__ = ["Loader", "LOADER_STATES", "CATEGORIES", "STATE_CATEGORY"]
