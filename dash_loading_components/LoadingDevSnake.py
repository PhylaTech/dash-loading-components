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


class LoadingDevSnake(Component):
    """A LoadingDevSnake component.
LoadingDevSnake — Dash wrapper for upstream spinner.

Keyword arguments:

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- cap (a value equal to: "round", "flat"; optional):
    Stroke line cap style.

- className (string; optional):
    CSS class applied to the outer wrapper.

- color (string; optional):
    Any CSS color.

- duration (number; optional):
    Animation cycle length in milliseconds.

- easing (a value equal to: "linear", "ease-in-out", "stacked"; optional):
    Animation easing curve.

- playState (a value equal to: "paused", "running"; optional):
    Whether the animation runs.

- size (number; optional):
    Width/height in pixels. Defaults to 20."""
    _children_props: typing.List[str] = []
    _base_nodes = ['children']
    _namespace = 'dash_loading_components'
    _type = 'LoadingDevSnake'


    def __init__(
        self,
        id: typing.Optional[typing.Union[str, dict]] = None,
        className: typing.Optional[str] = None,
        style: typing.Optional[typing.Any] = None,
        size: typing.Optional[NumberType] = None,
        color: typing.Optional[str] = None,
        duration: typing.Optional[NumberType] = None,
        playState: typing.Optional[Literal["paused", "running"]] = None,
        easing: typing.Optional[Literal["linear", "ease-in-out", "stacked"]] = None,
        cap: typing.Optional[Literal["round", "flat"]] = None,
        **kwargs
    ):
        self._prop_names = ['id', 'cap', 'className', 'color', 'duration', 'easing', 'playState', 'size', 'style']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'cap', 'className', 'color', 'duration', 'easing', 'playState', 'size', 'style']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(LoadingDevSnake, self).__init__(**args)

setattr(LoadingDevSnake, "__init__", _explicitize_args(LoadingDevSnake.__init__))
