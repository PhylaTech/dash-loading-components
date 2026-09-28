# AUTO GENERATED FILE - DO NOT EDIT

import typing  # noqa: F401
from typing_extensions import TypedDict, NotRequired, Literal # noqa: F401
from dash.development.base_component import Component, _explicitize_args
try:
    from dash.types import NumberType  # noqa: F401
except ImportError:
    if typing.TYPE_CHECKING:
        raise
    NumberType = typing.Union[  # noqa: F401
        typing.SupportsFloat, typing.SupportsInt, typing.SupportsComplex
    ]

ComponentSingleType = typing.Union[str, int, float, Component, None]
ComponentType = typing.Union[
    ComponentSingleType,
    typing.Sequence[ComponentSingleType],
]


class GridoraText(Component):
    """A GridoraText component.
GridoraText — Dash wrapper for gridora's GridLoaderText.

Same tempo/color/effect surface as GridLoader, plus `text`, `letter_gap`,
`letter_span`, `simultaneous`. No `variant`/`mask`/`sequence`.

Keyword arguments:

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- cell_size (number; optional):
    Size of each grid cell in pixels. Default 4.

- className (string; optional):
    CSS class applied to the outer wrapper.

- color (string; optional):
    Base color.

- color_mode (a value equal to: 'solid', 'horizontal', 'vertical', 'diagonal', 'radial', 'angular', 'random', 'cycle'; optional):
    How colors map onto the grid.

- colors (list of strings; optional):
    Color ramp sampled according to color_mode.

- direction (string; optional):
    CSS animation direction.

- dot_size (number; optional):
    Size of the dot inside a cell in pixels.

- easing (string; optional):
    CSS timing function.

- effect (a value equal to: 'pulse', 'fade', 'scale', 'blink', 'bounce', 'swing', 'flip', 'jelly', 'glow', 'spin', 'wobble', 'swell', 'drop', 'rise', 'zoom', 'pop', 'flicker', 'ping', 'twist', 'morph'; optional):
    Keyframes applied to every dot.

- gap (number; optional):
    Space between cells in pixels. Default 2.5.

- glow (number; optional):
    Blur radius of the dot glow in pixels.

- grid_size (number; optional):
    Number of rows and columns (2–12). Default 3.

- inactive (a value equal to: 'dim', 'hidden', 'solid'; optional):
    Rendering of cells not part of the shape.

- inactive_color (string; optional):
    Color used for inactive cells.

- inactive_opacity (number; optional):
    Opacity used when inactive is "dim".

- label (string; optional):
    Accessible label.

- letter_gap (number; optional):
    Space between glyphs in pixels.

- letter_span (number; optional):
    Fraction of the cycle each glyph occupies.

- mask_motion (a value equal to: 'write', 'writeReverse', 'fade', 'sweepX', 'sweepY', 'diagonal', 'radial', 'random', 'wave', 'drop', 'typewriter'; optional):
    Drawing order for mask variants.

- max_opacity (number; optional):
    Opacity at the peak.

- max_scale (number; optional):
    Scale at the peak.

- min_opacity (number; optional):
    Opacity at the resting point.

- min_scale (number; optional):
    Scale at the resting point.

- paused (boolean; optional):
    Upstream `paused`. Explicit paused wins over playing.

- playing (boolean; optional):
    Set to False to pause the animation.

- rate (number; optional):
    Relative tempo: rate=1 → 1s/cycle, rate=2 → 0.5s/cycle.

- respect_reduced_motion (boolean; optional):
    Disables animation when user prefers reduced motion.

- reverse (boolean; optional):
    Plays the stagger backwards.

- shape (a value equal to: 'circle', 'square', 'rounded', 'squircle', 'diamond', 'triangle', 'hexagon', 'star', 'plus', 'ring', 'blob', 'bar'; optional):
    Dot silhouette.

- simultaneous (boolean; optional):
    Draws every glyph at the same time instead of sequentially.

- size (number; optional):
    Overall CSS pixel size (common contract). When set and `cell_size`
    is unset, derives cellSize from grid geometry. NOT passed as
    upstream `size`/`cellSize`.

- speed (number; optional):
    Upstream cycle duration in seconds. Higher = slower. Default 1.

- text (string; required):
    Text drawn with the bitmap font. Required."""
    _children_props: typing.List[str] = []
    _base_nodes = ['children']
    _namespace = 'dash_loading_components'
    _type = 'GridoraText'

    def __init__(
        self,
        id: typing.Optional[typing.Union[str, dict]] = None,
        className: typing.Optional[str] = None,
        style: typing.Optional[typing.Any] = None,
        text: typing.Optional[str] = None,
        letter_gap: typing.Optional[NumberType] = None,
        letter_span: typing.Optional[NumberType] = None,
        simultaneous: typing.Optional[bool] = None,
        size: typing.Optional[NumberType] = None,
        grid_size: typing.Optional[NumberType] = None,
        cell_size: typing.Optional[NumberType] = None,
        dot_size: typing.Optional[NumberType] = None,
        gap: typing.Optional[NumberType] = None,
        speed: typing.Optional[NumberType] = None,
        color: typing.Optional[str] = None,
        colors: typing.Optional[typing.Sequence[str]] = None,
        color_mode: typing.Optional[Literal["solid", "horizontal", "vertical", "diagonal", "radial", "angular", "random", "cycle"]] = None,
        effect: typing.Optional[Literal["pulse", "fade", "scale", "blink", "bounce", "swing", "flip", "jelly", "glow", "spin", "wobble", "swell", "drop", "rise", "zoom", "pop", "flicker", "ping", "twist", "morph"]] = None,
        shape: typing.Optional[Literal["circle", "square", "rounded", "squircle", "diamond", "triangle", "hexagon", "star", "plus", "ring", "blob", "bar"]] = None,
        easing: typing.Optional[str] = None,
        inactive: typing.Optional[Literal["dim", "hidden", "solid"]] = None,
        inactive_opacity: typing.Optional[NumberType] = None,
        inactive_color: typing.Optional[str] = None,
        min_opacity: typing.Optional[NumberType] = None,
        max_opacity: typing.Optional[NumberType] = None,
        min_scale: typing.Optional[NumberType] = None,
        max_scale: typing.Optional[NumberType] = None,
        glow: typing.Optional[NumberType] = None,
        mask_motion: typing.Optional[Literal["write", "writeReverse", "fade", "sweepX", "sweepY", "diagonal", "radial", "random", "wave", "drop", "typewriter"]] = None,
        reverse: typing.Optional[bool] = None,
        direction: typing.Optional[str] = None,
        label: typing.Optional[str] = None,
        respect_reduced_motion: typing.Optional[bool] = None,
        paused: typing.Optional[bool] = None,
        rate: typing.Optional[NumberType] = None,
        playing: typing.Optional[bool] = None,
        **kwargs
    ):
        self._prop_names = ['id', 'cell_size', 'className', 'color', 'color_mode', 'colors', 'direction', 'dot_size', 'easing', 'effect', 'gap', 'glow', 'grid_size', 'inactive', 'inactive_color', 'inactive_opacity', 'label', 'letter_gap', 'letter_span', 'mask_motion', 'max_opacity', 'max_scale', 'min_opacity', 'min_scale', 'paused', 'playing', 'rate', 'respect_reduced_motion', 'reverse', 'shape', 'simultaneous', 'size', 'speed', 'style', 'text']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'cell_size', 'className', 'color', 'color_mode', 'colors', 'direction', 'dot_size', 'easing', 'effect', 'gap', 'glow', 'grid_size', 'inactive', 'inactive_color', 'inactive_opacity', 'label', 'letter_gap', 'letter_span', 'mask_motion', 'max_opacity', 'max_scale', 'min_opacity', 'min_scale', 'paused', 'playing', 'rate', 'respect_reduced_motion', 'reverse', 'shape', 'simultaneous', 'size', 'speed', 'style', 'text']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)
        args = {k: _locals[k] for k in _explicit_args}

        for k in ['text']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        super(GridoraText, self).__init__(**args)

setattr(GridoraText, "__init__", _explicitize_args(GridoraText.__init__))
