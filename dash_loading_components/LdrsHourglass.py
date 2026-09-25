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


class LdrsHourglass(Component):
    """A LdrsHourglass component.
LdrsHourglass — Dash wrapper for upstream spinner.

Keyword arguments:

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- bg_opacity (number | string; optional):
    Background opacity (0–1).

- className (string; optional):
    CSS class applied to the outer wrapper.

- color (string; optional):
    Color.

- playing (boolean; optional):
    Set to False to pause the animation.

- rate (number; optional):
    Relative tempo: 1.0 is this spinner's own tempo, 2.0 twice as
    fast, 0.5 half. Leave unset to keep the upstream tempo.

- size (number | string; optional):
    Size in px.

- speed (number | string; optional):
    Animation speed.

- stroke (number | string; optional):
    Stroke width where applicable."""
    _children_props: typing.List[str] = []
    _base_nodes = ['children']
    _namespace = 'dash_loading_components'
    _type = 'LdrsHourglass'


    def __init__(
        self,
        id: typing.Optional[typing.Union[str, dict]] = None,
        className: typing.Optional[str] = None,
        style: typing.Optional[typing.Any] = None,
        size: typing.Optional[typing.Union[NumberType, str]] = None,
        color: typing.Optional[str] = None,
        speed: typing.Optional[typing.Union[NumberType, str]] = None,
        stroke: typing.Optional[typing.Union[NumberType, str]] = None,
        bg_opacity: typing.Optional[typing.Union[NumberType, str]] = None,
        rate: typing.Optional[NumberType] = None,
        playing: typing.Optional[bool] = None,
        **kwargs
    ):
        self._prop_names = ['id', 'bg_opacity', 'className', 'color', 'playing', 'rate', 'size', 'speed', 'stroke', 'style']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'bg_opacity', 'className', 'color', 'playing', 'rate', 'size', 'speed', 'stroke', 'style']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(LdrsHourglass, self).__init__(**args)

setattr(LdrsHourglass, "__init__", _explicitize_args(LdrsHourglass.__init__))
