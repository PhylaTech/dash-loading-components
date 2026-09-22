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


class SpinnersHashLoader(Component):
    """A SpinnersHashLoader component.
SpinnersHashLoader — Dash wrapper for upstream spinner.

Keyword arguments:

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- className (string; optional):
    CSS class applied to the outer wrapper.

- color (string; optional):
    Color.

- height (number | string; optional):
    Height where applicable.

- loading (boolean; optional):
    Whether to show the spinner.

- margin (number | string; optional):
    Margin between elements.

- size (number; optional):
    Size in pixels.

- speedMultiplier (number; optional):
    Speed multiplier.

- width (number | string; optional):
    Width where applicable."""
    _children_props: typing.List[str] = []
    _base_nodes = ['children']
    _namespace = 'dash_loading_components'
    _type = 'SpinnersHashLoader'


    def __init__(
        self,
        id: typing.Optional[typing.Union[str, dict]] = None,
        className: typing.Optional[str] = None,
        style: typing.Optional[typing.Any] = None,
        size: typing.Optional[NumberType] = None,
        color: typing.Optional[str] = None,
        loading: typing.Optional[bool] = None,
        speedMultiplier: typing.Optional[NumberType] = None,
        height: typing.Optional[typing.Union[NumberType, str]] = None,
        width: typing.Optional[typing.Union[NumberType, str]] = None,
        margin: typing.Optional[typing.Union[NumberType, str]] = None,
        **kwargs
    ):
        self._prop_names = ['id', 'className', 'color', 'height', 'loading', 'margin', 'size', 'speedMultiplier', 'style', 'width']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'className', 'color', 'height', 'loading', 'margin', 'size', 'speedMultiplier', 'style', 'width']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(SpinnersHashLoader, self).__init__(**args)

setattr(SpinnersHashLoader, "__init__", _explicitize_args(SpinnersHashLoader.__init__))
