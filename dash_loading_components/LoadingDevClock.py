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


class LoadingDevClock(Component):
    """A LoadingDevClock component.
LoadingDevClock — Dash wrapper for upstream spinner.

Keyword arguments:

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- className (string; optional):
    Extra class names merged onto the spinner root (loading.dev).

- color (string; optional):
    Any CSS color.

- duration (number; optional):
    Animation cycle length in milliseconds.

- easing (a value equal to: "linear", "ease-in-out", "stacked"; optional):
    Animation easing curve.

- play_state (a value equal to: "paused", "running"; optional):
    Whether the animation runs.

- playing (boolean; optional):
    Set to False to pause the animation.

- rate (number; optional):
    Relative tempo: 1.0 is this spinner's own tempo, 2.0 twice as
    fast, 0.5 half. Leave unset to keep the upstream tempo.

- size (number; optional):
    Width/height in pixels. Defaults to 20."""
    _children_props: typing.List[str] = []
    _base_nodes = ['children']
    _namespace = 'dash_loading_components'
    _type = 'LoadingDevClock'


    def __init__(
        self,
        id: typing.Optional[typing.Union[str, dict]] = None,
        className: typing.Optional[str] = None,
        style: typing.Optional[typing.Any] = None,
        size: typing.Optional[NumberType] = None,
        color: typing.Optional[str] = None,
        duration: typing.Optional[NumberType] = None,
        play_state: typing.Optional[Literal["paused", "running"]] = None,
        easing: typing.Optional[Literal["linear", "ease-in-out", "stacked"]] = None,
        rate: typing.Optional[NumberType] = None,
        playing: typing.Optional[bool] = None,
        **kwargs
    ):
        self._prop_names = ['id', 'className', 'color', 'duration', 'easing', 'play_state', 'playing', 'rate', 'size', 'style']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'className', 'color', 'duration', 'easing', 'play_state', 'playing', 'rate', 'size', 'style']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(LoadingDevClock, self).__init__(**args)

setattr(LoadingDevClock, "__init__", _explicitize_args(LoadingDevClock.__init__))
