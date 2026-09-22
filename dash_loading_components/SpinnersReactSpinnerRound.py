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


class SpinnersReactSpinnerRound(Component):
    """A SpinnersReactSpinnerRound component.
SpinnersReactSpinnerRound — Dash wrapper for upstream spinner.

Keyword arguments:

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- className (string; optional):
    CSS class applied to the outer wrapper.

- color (string; optional):
    Primary color.

- enabled (boolean; optional):
    Whether enabled.

- secondaryColor (string; optional):
    Secondary color.

- size (number | string; optional):
    Size.

- speed (number; optional):
    Speed.

- still (boolean; optional):
    Disable animation while keeping the spinner visible.

- thickness (number; optional):
    Thickness."""
    _children_props: typing.List[str] = []
    _base_nodes = ['children']
    _namespace = 'dash_loading_components'
    _type = 'SpinnersReactSpinnerRound'


    def __init__(
        self,
        id: typing.Optional[typing.Union[str, dict]] = None,
        className: typing.Optional[str] = None,
        style: typing.Optional[typing.Any] = None,
        size: typing.Optional[typing.Union[NumberType, str]] = None,
        color: typing.Optional[str] = None,
        secondaryColor: typing.Optional[str] = None,
        thickness: typing.Optional[NumberType] = None,
        speed: typing.Optional[NumberType] = None,
        enabled: typing.Optional[bool] = None,
        still: typing.Optional[bool] = None,
        **kwargs
    ):
        self._prop_names = ['id', 'className', 'color', 'enabled', 'secondaryColor', 'size', 'speed', 'still', 'style', 'thickness']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'className', 'color', 'enabled', 'secondaryColor', 'size', 'speed', 'still', 'style', 'thickness']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(SpinnersReactSpinnerRound, self).__init__(**args)

setattr(SpinnersReactSpinnerRound, "__init__", _explicitize_args(SpinnersReactSpinnerRound.__init__))
