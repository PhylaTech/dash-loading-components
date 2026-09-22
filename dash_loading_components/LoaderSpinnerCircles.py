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


class LoaderSpinnerCircles(Component):
    """A LoaderSpinnerCircles component.
LoaderSpinnerCircles — Dash wrapper for upstream spinner.

Keyword arguments:

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- ariaLabel (string; optional):
    Aria label.

- className (string; optional):
    CSS class applied to the outer wrapper.

- color (string; optional):
    Color.

- height (number | string; optional):
    Height.

- radius (number | string; optional):
    Radius where applicable.

- secondaryColor (string; optional):
    Secondary color.

- strokeWidth (number | string; optional):
    Stroke width.

- visible (boolean; optional):
    Visibility.

- width (number | string; optional):
    Width."""
    _children_props: typing.List[str] = []
    _base_nodes = ['children']
    _namespace = 'dash_loading_components'
    _type = 'LoaderSpinnerCircles'


    def __init__(
        self,
        id: typing.Optional[typing.Union[str, dict]] = None,
        className: typing.Optional[str] = None,
        style: typing.Optional[typing.Any] = None,
        height: typing.Optional[typing.Union[NumberType, str]] = None,
        width: typing.Optional[typing.Union[NumberType, str]] = None,
        color: typing.Optional[str] = None,
        secondaryColor: typing.Optional[str] = None,
        radius: typing.Optional[typing.Union[NumberType, str]] = None,
        ariaLabel: typing.Optional[str] = None,
        visible: typing.Optional[bool] = None,
        strokeWidth: typing.Optional[typing.Union[NumberType, str]] = None,
        **kwargs
    ):
        self._prop_names = ['id', 'ariaLabel', 'className', 'color', 'height', 'radius', 'secondaryColor', 'strokeWidth', 'style', 'visible', 'width']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'ariaLabel', 'className', 'color', 'height', 'radius', 'secondaryColor', 'strokeWidth', 'style', 'visible', 'width']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(LoaderSpinnerCircles, self).__init__(**args)

setattr(LoaderSpinnerCircles, "__init__", _explicitize_args(LoaderSpinnerCircles.__init__))
