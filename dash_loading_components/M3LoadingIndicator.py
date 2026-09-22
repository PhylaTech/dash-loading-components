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


class M3LoadingIndicator(Component):
    """A M3LoadingIndicator component.
M3LoadingIndicator — Dash wrapper for upstream spinner.

Keyword arguments:

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- className (string; optional):
    CSS class applied to the outer wrapper.

- color (string; optional):
    Fill color.

- contained (boolean; optional):
    Render with circular container background.

- containerColor (string; optional):
    Container background when contained.

- paused (boolean; optional):
    Pause the animation.

- size (number; optional):
    CSS pixel size (default 48).

- sizeRatio (number; optional):
    Ratio of indicator shape to container.

- speed (number; optional):
    Animation speed multiplier."""
    _children_props: typing.List[str] = []
    _base_nodes = ['children']
    _namespace = 'dash_loading_components'
    _type = 'M3LoadingIndicator'


    def __init__(
        self,
        id: typing.Optional[typing.Union[str, dict]] = None,
        className: typing.Optional[str] = None,
        style: typing.Optional[typing.Any] = None,
        size: typing.Optional[NumberType] = None,
        color: typing.Optional[str] = None,
        sizeRatio: typing.Optional[NumberType] = None,
        speed: typing.Optional[NumberType] = None,
        paused: typing.Optional[bool] = None,
        contained: typing.Optional[bool] = None,
        containerColor: typing.Optional[str] = None,
        **kwargs
    ):
        self._prop_names = ['id', 'className', 'color', 'contained', 'containerColor', 'paused', 'size', 'sizeRatio', 'speed', 'style']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'className', 'color', 'contained', 'containerColor', 'paused', 'size', 'sizeRatio', 'speed', 'style']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(M3LoadingIndicator, self).__init__(**args)

setattr(M3LoadingIndicator, "__init__", _explicitize_args(M3LoadingIndicator.__init__))
