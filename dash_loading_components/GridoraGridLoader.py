# AUTO GENERATED FILE - DO NOT EDIT

import typing  # noqa: F401
from typing_extensions import TypedDict, NotRequired, Literal # noqa: F401
from dash.development.base_component import Component, _explicitize_args
try:
    from dash.types import NumberType  # noqa: F401
except ImportError:
    # Backwards compatibility for dash<=4.1.0
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


class GridoraGridLoader(Component):
    """A GridoraGridLoader component.
GridoraGridLoader — Dash wrapper for gridora's GridLoader.

Common `size` is overall CSS px, NOT upstream `size`/`cellSize` (which is
cell px). When common `size` is set and `cell_size` is not, we derive
`cellSize = (size - (gridSize - 1) * gap) / gridSize`, clamped ≥ 1.

Keyword arguments:

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- cell_size (number; optional):
    Size of each grid cell in pixels. Default 4.

- className (string; optional):
    CSS class applied to the outer wrapper.

- color (string; optional):
    Base color or first stop when colors is omitted.

- color_mode (a value equal to: 'solid', 'horizontal', 'vertical', 'diagonal', 'radial', 'angular', 'random', 'cycle'; optional):
    How colors map onto the grid.

- colors (list of strings; optional):
    Color ramp sampled according to color_mode.

- direction (string; optional):
    CSS animation direction.

- dot_size (number; optional):
    Size of the dot inside a cell in pixels. Default cellSize × 0.875.

- easing (string; optional):
    CSS timing function.

- effect (a value equal to: 'pulse', 'fade', 'scale', 'blink', 'bounce', 'swing', 'flip', 'jelly', 'glow', 'spin', 'wobble', 'swell', 'drop', 'rise', 'zoom', 'pop', 'flicker', 'ping', 'twist', 'morph'; optional):
    Keyframes applied to every dot.

- gap (number; optional):
    Space between cells in pixels. Default 2.5.

- glow (number; optional):
    Blur radius of the dot glow in pixels. Default 0.

- grid_size (number; optional):
    Number of rows and columns (2–12). Default 3.

- inactive (a value equal to: 'dim', 'hidden', 'solid'; optional):
    Rendering of cells not part of the shape.

- inactive_color (string; optional):
    Color used for inactive cells.

- inactive_opacity (number; optional):
    Opacity used when inactive is \"dim\".

- label (string; optional):
    Accessible label. Default \"Loading\".

- mask (list of list of numberss | string; optional):
    Custom bitmap mask (array of arrays of 0/1, or a slash-delimited
    string).

- mask_motion (a value equal to: 'write', 'writeReverse', 'fade', 'sweepX', 'sweepY', 'diagonal', 'radial', 'random', 'wave', 'drop', 'typewriter'; optional):
    Drawing order for glyph and mask variants.

- max_opacity (number; optional):
    Opacity at the peak. Default 1.

- max_scale (number; optional):
    Scale at the peak. Default 1.

- min_opacity (number; optional):
    Opacity at the resting point. Default 0.2.

- min_scale (number; optional):
    Scale at the resting point. Default 1.

- offset (number; optional):
    Extra phase offset in cycles.

- paused (boolean; optional):
    Upstream `paused`. When `playing` is set and `paused` is not,
    paused = !playing. An explicit `paused` wins.

- playing (boolean; optional):
    Set to False to pause the animation.

- rate (number; optional):
    Relative tempo: 1.0 = 1 s/cycle, 2.0 = 0.5 s/cycle. Mapped to
    upstream speed = 1/rate. Leave unset to keep the default.

- respect_reduced_motion (boolean; optional):
    Disables animation when user prefers reduced motion.

- reverse (boolean; optional):
    Plays the stagger backwards.

- sequence (list of numbers; optional):
    Ordered cell indices for custom animation order.

- shape (a value equal to: 'circle', 'square', 'rounded', 'squircle', 'diamond', 'triangle', 'hexagon', 'star', 'plus', 'ring', 'blob', 'bar'; optional):
    Dot silhouette.

- size (number; optional):
    Overall CSS pixel size (common contract). When set and `cell_size`
    is unset, derives cellSize = (size - (gridSize-1)*gap) / gridSize.
    NOT passed through as upstream `size`/`cellSize`.

- speed (number; optional):
    Upstream cycle duration in seconds. Higher = slower. Default 1.
    When `rate` is set and `speed` is not, speed = 1/rate.

- spread (number; optional):
    How much of the cycle the stagger spans (1 = full cycle).

- variant (string; optional):
    Animation pattern (one of the 133 motion variants, or a glyph)."""
    _children_props: typing.List[str] = []
    _base_nodes = ['children']
    _namespace = 'dash_loading_components'
    _type = 'GridoraGridLoader'


    def __init__(
        self,
        id: typing.Optional[typing.Union[str, dict]] = None,
        className: typing.Optional[str] = None,
        style: typing.Optional[typing.Any] = None,
        size: typing.Optional[NumberType] = None,
        variant: typing.Optional[str] = None,
        sequence: typing.Optional[typing.Sequence[NumberType]] = None,
        mask: typing.Optional[typing.Union[typing.Sequence[typing.Sequence[NumberType]], str]] = None,
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
        spread: typing.Optional[NumberType] = None,
        offset: typing.Optional[NumberType] = None,
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
        self._prop_names = ['id', 'cell_size', 'className', 'color', 'color_mode', 'colors', 'direction', 'dot_size', 'easing', 'effect', 'gap', 'glow', 'grid_size', 'inactive', 'inactive_color', 'inactive_opacity', 'label', 'mask', 'mask_motion', 'max_opacity', 'max_scale', 'min_opacity', 'min_scale', 'offset', 'paused', 'playing', 'rate', 'respect_reduced_motion', 'reverse', 'sequence', 'shape', 'size', 'speed', 'spread', 'style', 'variant']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'cell_size', 'className', 'color', 'color_mode', 'colors', 'direction', 'dot_size', 'easing', 'effect', 'gap', 'glow', 'grid_size', 'inactive', 'inactive_color', 'inactive_opacity', 'label', 'mask', 'mask_motion', 'max_opacity', 'max_scale', 'min_opacity', 'min_scale', 'offset', 'paused', 'playing', 'rate', 'respect_reduced_motion', 'reverse', 'sequence', 'shape', 'size', 'speed', 'spread', 'style', 'variant']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(GridoraGridLoader, self).__init__(**args)

setattr(GridoraGridLoader, "__init__", _explicitize_args(GridoraGridLoader.__init__))
