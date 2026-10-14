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


class ThinkingOrbsOrb(Component):
    """A ThinkingOrbsOrb component.


Keyword arguments:

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- aria_label (string; optional):
    Accessible label on the canvas. Defaults to a per-state label such
    as \"Searching...\".

- className (string; optional):
    CSS class applied to the outer wrapper.

- color (string; optional):
    Optional ink tint as \"#rgb\", \"#rrggbb\" or \"rgb(r, g, b)\";
    any other CSS colour syntax is ignored by upstream. The orb's
    depth shading is kept on the tint. Leave unset for the stock
    monochrome ink.

- dot_size (number; optional):
    Dot-radius multiplier. 1 (default) is the tuned look; 0.7 reads
    finer, 1.5 bolder. Upstream floors it at 0.1.

- dots (number; optional):
    Dot-count multiplier, applied while keeping the state's balance. 1
    (default) is the tuned look; upstream floors it at 0.1.

- paused (boolean; optional):
    Upstream pause flag. When `playing` is set and `paused` is not,
    paused = !playing. An explicit `paused` wins.

- playing (boolean; optional):
    Set to False to freeze the animation on its current frame.

- rate (number; optional):
    Relative tempo: 1.0 is the state's own tempo, 2.0 twice as fast.
    Mapped to upstream speed = rate. Leave unset to keep the default.

- size (number; optional):
    Square canvas side in CSS pixels. Upstream has three designs, at
    64 (chat avatar), 32 and 20 (inline text); the nearest one is
    drawn and scaled to this size. Sizes above 64 upscale the 64
    design, so they soften. Default 64.

- speed (number; optional):
    Upstream tempo multiplier on the state's own speed. 1 = normal.
    Prefer `rate` for the common contract; an explicit `speed` wins
    over `rate`.

- state (a value equal to: 'working', 'searching', 'solving', 'listening', 'connecting', 'weaving', 'composing', 'breathing', 'shaping'; optional):
    Which orb animation to show: \"working\", \"searching\",
    \"solving\", \"listening\", \"connecting\", \"weaving\",
    \"composing\", \"breathing\" or \"shaping\". Defaults to
    \"working\".

- theme (a value equal to: 'auto', 'dark', 'light'; optional):
    Ink for the dots: \"auto\", \"dark\" or \"light\". Dark is light
    ink for dark backgrounds; light is dark ink for light ones.
    \"auto\" follows an ancestor data-theme attribute or dark/light
    class, the Mantine colour scheme, or else the operating system.
    Default \"auto\"."""
    _children_props: typing.List[str] = []
    _base_nodes = ['children']
    _namespace = 'dash_loading_components'
    _type = 'ThinkingOrbsOrb'


    def __init__(
        self,
        id: typing.Optional[typing.Union[str, dict]] = None,
        className: typing.Optional[str] = None,
        style: typing.Optional[typing.Any] = None,
        state: typing.Optional[Literal["working", "searching", "solving", "listening", "connecting", "weaving", "composing", "breathing", "shaping"]] = None,
        size: typing.Optional[NumberType] = None,
        theme: typing.Optional[Literal["auto", "dark", "light"]] = None,
        speed: typing.Optional[NumberType] = None,
        paused: typing.Optional[bool] = None,
        color: typing.Optional[str] = None,
        dots: typing.Optional[NumberType] = None,
        dot_size: typing.Optional[NumberType] = None,
        aria_label: typing.Optional[str] = None,
        rate: typing.Optional[NumberType] = None,
        playing: typing.Optional[bool] = None,
        **kwargs
    ):
        self._prop_names = ['id', 'aria_label', 'className', 'color', 'dot_size', 'dots', 'paused', 'playing', 'rate', 'size', 'speed', 'state', 'style', 'theme']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'aria_label', 'className', 'color', 'dot_size', 'dots', 'paused', 'playing', 'rate', 'size', 'speed', 'state', 'style', 'theme']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(ThinkingOrbsOrb, self).__init__(**args)

setattr(ThinkingOrbsOrb, "__init__", _explicitize_args(ThinkingOrbsOrb.__init__))
