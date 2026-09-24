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


class PremiumOrbitDots(Component):
    """A PremiumOrbitDots component.
PremiumOrbitDots — Dash wrapper for upstream OrbitDots.
Requires premium-react-loaders CSS (see ./styles).

Keyword arguments:

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- className (string; optional):
    CSS class applied to the upstream spinner root.

- color (string; optional):
    Primary color.

- dotCount (number; optional):
    Number of orbiting dots.

- dotSize (number; optional):
    Size of each dot.

- orbitRadius (number; optional):
    Orbit radius relative to size.

- reverse (boolean; optional):
    Reverse animation direction.

- secondaryColor (string; optional):
    Secondary color for alternating dots.

- size (string | number; optional):
    Size (xs/sm/md/lg/xl or number px).

- speed (string | number; optional):
    Speed: 'slow' | 'normal' | 'fast' or duration in milliseconds.
    Common API relative speed is translated to ms before reaching this
    prop.

- stagger (boolean; optional):
    Stagger animation between dots.

- thickness (number; optional):
    Thickness of orbit path / elements.

- visible (boolean; optional):
    Whether the loader is visible."""
    _children_props: typing.List[str] = []
    _base_nodes = ['children']
    _namespace = 'dash_loading_components'
    _type = 'PremiumOrbitDots'


    def __init__(
        self,
        id: typing.Optional[typing.Union[str, dict]] = None,
        className: typing.Optional[str] = None,
        style: typing.Optional[typing.Any] = None,
        size: typing.Optional[typing.Union[str, NumberType]] = None,
        color: typing.Optional[str] = None,
        speed: typing.Optional[typing.Union[str, NumberType]] = None,
        reverse: typing.Optional[bool] = None,
        secondaryColor: typing.Optional[str] = None,
        visible: typing.Optional[bool] = None,
        thickness: typing.Optional[NumberType] = None,
        dotCount: typing.Optional[NumberType] = None,
        dotSize: typing.Optional[NumberType] = None,
        orbitRadius: typing.Optional[NumberType] = None,
        stagger: typing.Optional[bool] = None,
        **kwargs
    ):
        self._prop_names = ['id', 'className', 'color', 'dotCount', 'dotSize', 'orbitRadius', 'reverse', 'secondaryColor', 'size', 'speed', 'stagger', 'style', 'thickness', 'visible']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'className', 'color', 'dotCount', 'dotSize', 'orbitRadius', 'reverse', 'secondaryColor', 'size', 'speed', 'stagger', 'style', 'thickness', 'visible']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(PremiumOrbitDots, self).__init__(**args)

setattr(PremiumOrbitDots, "__init__", _explicitize_args(PremiumOrbitDots.__init__))
