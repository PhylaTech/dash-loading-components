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


class PremiumShimmerBox(Component):
    """A PremiumShimmerBox component.
PremiumShimmerBox — Dash wrapper for upstream spinner.

Upstream ShimmerBox takes width/height (defaults 200x100) and baseColor.
`size` and `color` map onto those so the box behaves like every other
dlc component.

Keyword arguments:

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- className (string; optional):
    CSS class applied to the outer wrapper.

- color (string; optional):
    Mapped to upstream baseColor (fill behind the shimmer).

- height (string | number; optional):
    Explicit box height (px or CSS length). Overrides size-derived
    height.

- playing (boolean; optional):
    Set to False to pause the animation.

- rate (number; optional):
    Relative tempo: 1.0 is this spinner's own tempo, 2.0 twice as
    fast, 0.5 half. Leave unset to keep the upstream tempo.

- secondary_color (string; optional):
    Mapped to upstream highlightColor (shimmer highlight).

- size (string | number; optional):
    Common API size. Mapped to width≈2×size and height≈size when
    width/height are not set (upstream defaults are 200×100).

- speed (string | number; optional):
    Speed (slow/normal/fast or duration token).

- visible (boolean; optional):
    Whether the loader is visible.

- width (string | number; optional):
    Explicit box width (px or CSS length). Overrides size-derived
    width."""
    _children_props: typing.List[str] = []
    _base_nodes = ['children']
    _namespace = 'dash_loading_components'
    _type = 'PremiumShimmerBox'


    def __init__(
        self,
        id: typing.Optional[typing.Union[str, dict]] = None,
        className: typing.Optional[str] = None,
        style: typing.Optional[typing.Any] = None,
        size: typing.Optional[typing.Union[str, NumberType]] = None,
        width: typing.Optional[typing.Union[str, NumberType]] = None,
        height: typing.Optional[typing.Union[str, NumberType]] = None,
        color: typing.Optional[str] = None,
        speed: typing.Optional[typing.Union[str, NumberType]] = None,
        secondary_color: typing.Optional[str] = None,
        visible: typing.Optional[bool] = None,
        rate: typing.Optional[NumberType] = None,
        playing: typing.Optional[bool] = None,
        **kwargs
    ):
        self._prop_names = ['id', 'className', 'color', 'height', 'playing', 'rate', 'secondary_color', 'size', 'speed', 'style', 'visible', 'width']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'className', 'color', 'height', 'playing', 'rate', 'secondary_color', 'size', 'speed', 'style', 'visible', 'width']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(PremiumShimmerBox, self).__init__(**args)

setattr(PremiumShimmerBox, "__init__", _explicitize_args(PremiumShimmerBox.__init__))
