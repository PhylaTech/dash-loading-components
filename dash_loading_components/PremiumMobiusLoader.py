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


class PremiumMobiusLoader(Component):
    """A PremiumMobiusLoader component.
PremiumMobiusLoader — Dash wrapper for upstream spinner.

Keyword arguments:

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- className (string; optional):
    CSS class applied to the outer wrapper.

- color (string; optional):
    Color.

- playing (boolean; optional):
    Set to False to pause the animation.

- rate (number; optional):
    Relative tempo: 1.0 is this spinner's own tempo, 2.0 twice as
    fast, 0.5 half. Leave unset to keep the upstream tempo.

- reverse (boolean; optional):
    Reverse animation direction.

- secondary_color (string; optional):
    Secondary color for multi-color loaders.

- size (string | number; optional):
    Size (sm/md/lg or number).

- speed (string | number; optional):
    Speed (slow/normal/fast).

- visible (boolean; optional):
    Whether the loader is visible."""
    _children_props: typing.List[str] = []
    _base_nodes = ['children']
    _namespace = 'dash_loading_components'
    _type = 'PremiumMobiusLoader'


    def __init__(
        self,
        id: typing.Optional[typing.Union[str, dict]] = None,
        className: typing.Optional[str] = None,
        style: typing.Optional[typing.Any] = None,
        size: typing.Optional[typing.Union[str, NumberType]] = None,
        color: typing.Optional[str] = None,
        speed: typing.Optional[typing.Union[str, NumberType]] = None,
        reverse: typing.Optional[bool] = None,
        secondary_color: typing.Optional[str] = None,
        visible: typing.Optional[bool] = None,
        rate: typing.Optional[NumberType] = None,
        playing: typing.Optional[bool] = None,
        **kwargs
    ):
        self._prop_names = ['id', 'className', 'color', 'playing', 'rate', 'reverse', 'secondary_color', 'size', 'speed', 'style', 'visible']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'className', 'color', 'playing', 'rate', 'reverse', 'secondary_color', 'size', 'speed', 'style', 'visible']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(PremiumMobiusLoader, self).__init__(**args)

setattr(PremiumMobiusLoader, "__init__", _explicitize_args(PremiumMobiusLoader.__init__))
