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


class PremiumOrbitRings(Component):
    """A PremiumOrbitRings component.
PremiumOrbitRings — Dash wrapper for upstream OrbitRings.
Requires premium-react-loaders CSS (see ./styles).

Keyword arguments:

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- alternate (boolean; optional):
    Alternate ring rotation directions.

- className (string; optional):
    CSS class applied to the upstream spinner root.

- color (string; optional):
    Primary color.

- playing (boolean; optional):
    Set to False to pause the animation.

- rate (number; optional):
    Relative tempo: 1.0 is this spinner's own tempo, 2.0 twice as
    fast, 0.5 half. Leave unset to keep the upstream tempo.

- reverse (boolean; optional):
    Reverse animation direction.

- ring_count (number; optional):
    Number of concentric rings.

- ring_gap (number; optional):
    Gap between rings in px.

- secondary_color (string; optional):
    Secondary color for alternating rings.

- size (string | number; optional):
    Size (xs/sm/md/lg/xl or number px).

- speed (string | number; optional):
    Speed: 'slow' | 'normal' | 'fast' or duration in milliseconds.
    Common API relative speed is translated to ms before reaching this
    prop.

- thickness (number; optional):
    Ring border thickness in px.

- visible (boolean; optional):
    Whether the loader is visible."""
    _children_props: typing.List[str] = []
    _base_nodes = ['children']
    _namespace = 'dash_loading_components'
    _type = 'PremiumOrbitRings'


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
        thickness: typing.Optional[NumberType] = None,
        ring_count: typing.Optional[NumberType] = None,
        ring_gap: typing.Optional[NumberType] = None,
        alternate: typing.Optional[bool] = None,
        rate: typing.Optional[NumberType] = None,
        playing: typing.Optional[bool] = None,
        **kwargs
    ):
        self._prop_names = ['id', 'alternate', 'className', 'color', 'playing', 'rate', 'reverse', 'ring_count', 'ring_gap', 'secondary_color', 'size', 'speed', 'style', 'thickness', 'visible']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'alternate', 'className', 'color', 'playing', 'rate', 'reverse', 'ring_count', 'ring_gap', 'secondary_color', 'size', 'speed', 'style', 'thickness', 'visible']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(PremiumOrbitRings, self).__init__(**args)

setattr(PremiumOrbitRings, "__init__", _explicitize_args(PremiumOrbitRings.__init__))
