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


class FlickerSpinner(Component):
    """A FlickerSpinner component.
FlickerSpinner — Dash wrapper for flicker-dot's player. The named presets
in dlc.flicker are this component with their frames filled in.

Keyword arguments:

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- aria_label (string; optional):
    Accessible name, announced to assistive technology (default
    \"Loading\").

- className (string; optional):
    CSS class applied to the outer wrapper.

- color (string; optional):
    Color of a lit dot (default currentColor).

- grids (list of list of boolean | number | string | listss; required):
    The frames to play, in order, one every 150ms at rate 1.0. Each
    frame is the 7x7 grid as 49 values, as 7 rows of 7, or as 7
    strings of 7 characters where '#' is a lit dot. The named presets
    fill this in.

- mirror (boolean; optional):
    Mirror the animation left to right (before any rotation).

- off_color (string; optional):
    Color of an unlit dot, drawn at `off_opacity` (default `color`).

- off_opacity (number; optional):
    Opacity of the unlit dots, 0 to 1 (default 0.16). 0 leaves only
    the lit dots; 1 paints `off_color` solid.

- on_opacity (number; optional):
    Opacity of the lit dots, 0 to 1 (default 1).

- playing (boolean; optional):
    Set to False to pause the animation.

- rate (number; optional):
    Relative tempo: 1.0 is this spinner's own tempo, 2.0 twice as
    fast, 0.5 half. Leave unset to keep the upstream tempo.

- reverse (boolean; optional):
    Play the frames backwards.

- rotate (a value equal to: 0, 90, 180, 270; optional):
    Turn the animation clockwise, in degrees: 90 makes a loop that
    grows upward grow to the right.

- size (number; optional):
    CSS pixel size (default 28, or 16 for the 5x5 variant).

- speed (number; optional):
    Playback multiplier: 2 plays twice as fast.

- variant (a value equal to: '7x7', '5x5', '9x9'; optional):
    The grid: the full 7x7, its inner 5x5 (bigger dots), or the 7x7
    padded to 9x9 with a ring of unlit dots (smaller dots)."""
    _children_props: typing.List[str] = []
    _base_nodes = ['children']
    _namespace = 'dash_loading_components'
    _type = 'FlickerSpinner'


    def __init__(
        self,
        id: typing.Optional[typing.Union[str, dict]] = None,
        className: typing.Optional[str] = None,
        style: typing.Optional[typing.Any] = None,
        grids: typing.Optional[typing.Sequence[typing.Sequence[typing.Union[bool, NumberType, str, typing.Sequence]]]] = None,
        size: typing.Optional[NumberType] = None,
        color: typing.Optional[str] = None,
        on_opacity: typing.Optional[NumberType] = None,
        off_color: typing.Optional[str] = None,
        off_opacity: typing.Optional[NumberType] = None,
        variant: typing.Optional[Literal["7x7", "5x5", "9x9"]] = None,
        rotate: typing.Optional[Literal[0, 90, 180, 270]] = None,
        mirror: typing.Optional[bool] = None,
        reverse: typing.Optional[bool] = None,
        speed: typing.Optional[NumberType] = None,
        aria_label: typing.Optional[str] = None,
        rate: typing.Optional[NumberType] = None,
        playing: typing.Optional[bool] = None,
        **kwargs
    ):
        self._prop_names = ['id', 'aria_label', 'className', 'color', 'grids', 'mirror', 'off_color', 'off_opacity', 'on_opacity', 'playing', 'rate', 'reverse', 'rotate', 'size', 'speed', 'style', 'variant']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'aria_label', 'className', 'color', 'grids', 'mirror', 'off_color', 'off_opacity', 'on_opacity', 'playing', 'rate', 'reverse', 'rotate', 'size', 'speed', 'style', 'variant']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        for k in ['grids']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        super(FlickerSpinner, self).__init__(**args)

setattr(FlickerSpinner, "__init__", _explicitize_args(FlickerSpinner.__init__))
