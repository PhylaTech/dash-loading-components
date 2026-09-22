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


class IndicatorsSlab(Component):
    """An IndicatorsSlab component.
IndicatorsSlab — Dash wrapper for upstream spinner.

Keyword arguments:

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- className (string; optional):
    CSS class applied to the outer wrapper.

- color (string | list of strings; optional):
    Color or color array.

- size (string | number; optional):
    Size (small/medium/large or number).

- speedPlus (number; optional):
    Speed adjustment.

- text (string; optional):
    Optional text.

- textColor (string; optional):
    Text color.

- variant (string; optional):
    Variant where supported (OrbitProgress, ThreeDot)."""
    _children_props: typing.List[str] = []
    _base_nodes = ['children']
    _namespace = 'dash_loading_components'
    _type = 'IndicatorsSlab'


    def __init__(
        self,
        id: typing.Optional[typing.Union[str, dict]] = None,
        className: typing.Optional[str] = None,
        style: typing.Optional[typing.Any] = None,
        size: typing.Optional[typing.Union[str, NumberType]] = None,
        color: typing.Optional[typing.Union[str, typing.Sequence[str]]] = None,
        text: typing.Optional[str] = None,
        textColor: typing.Optional[str] = None,
        speedPlus: typing.Optional[NumberType] = None,
        variant: typing.Optional[str] = None,
        **kwargs
    ):
        self._prop_names = ['id', 'className', 'color', 'size', 'speedPlus', 'style', 'text', 'textColor', 'variant']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'className', 'color', 'size', 'speedPlus', 'style', 'text', 'textColor', 'variant']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(IndicatorsSlab, self).__init__(**args)

setattr(IndicatorsSlab, "__init__", _explicitize_args(IndicatorsSlab.__init__))
