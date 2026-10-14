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


class LoaderszLoader(Component):
    """A LoaderszLoader component.
LoaderszLoader -- Dash wrapper for loadersz's canvas-based loading indicators.

loadersz ships as a native Web Component (`<loadersz-loader>`). This wrapper
renders the custom element, forwarding Dash-friendly snake_case props to its
kebab-case attributes and managing the common dlc contract (rate, playing).

`rate` maps to upstream `speed` as: speed = rate (both are multipliers).
`size` maps directly (upstream also calls it `size`, CSS px).
`color` maps directly (upstream also calls it `color`, CSS colour string).

Keyword arguments:

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- aria_label (string; optional):
    Accessible label on the canvas. Default \"Loading\".

- className (string; optional):
    CSS class applied to the outer wrapper.

- color (string; optional):
    CSS colour string. Overrides hue when set.

- density (number; optional):
    Geometry detail multiplier. Clamped to 0.35-2 by upstream. Default
    1.

- force_motion (boolean; optional):
    Override reduced-motion preference.

- hue (number; optional):
    Overrides native colour palette with a single hue (0-360). -1
    (upstream default) keeps the loader's own colours. `color` wins
    over `hue` when both are set.

- particle_radius (number; optional):
    Particle thickness multiplier. Clamped to 0.5-2.5 by upstream.
    Default 1.

- paused (boolean; optional):
    Upstream pause flag. When `playing` is set and `paused` is not,
    paused = !playing. An explicit `paused` wins.

- playing (boolean; optional):
    Set to False to pause the animation.

- rate (number; optional):
    Relative tempo: 1.0 is normal speed, 2.0 twice as fast. Mapped to
    upstream speed = rate. Leave unset to keep the default.

- size (number; optional):
    Square canvas side in CSS pixels. Values below 16 are clamped by
    upstream. Default 96.

- speed (number; optional):
    Upstream timeline multiplier. 1 = normal speed. Prefer `rate` for
    the common contract; an explicit `speed` wins over `rate`.

- state (string; optional):
    Which loader animation to show. One of the 160 semantic state
    names (e.g. \"working\", \"searching\", \"heatmapping\"). Defaults
    to \"working\".

- theme (a value equal to: 'auto', 'dark', 'light'; optional):
    Canvas colour scheme: \"auto\", \"dark\", or \"light\". Default
    \"auto\"."""
    _children_props: typing.List[str] = []
    _base_nodes = ['children']
    _namespace = 'dash_loading_components'
    _type = 'LoaderszLoader'


    def __init__(
        self,
        id: typing.Optional[typing.Union[str, dict]] = None,
        className: typing.Optional[str] = None,
        style: typing.Optional[typing.Any] = None,
        state: typing.Optional[str] = None,
        size: typing.Optional[NumberType] = None,
        speed: typing.Optional[NumberType] = None,
        density: typing.Optional[NumberType] = None,
        particle_radius: typing.Optional[NumberType] = None,
        theme: typing.Optional[Literal["auto", "dark", "light"]] = None,
        hue: typing.Optional[NumberType] = None,
        color: typing.Optional[str] = None,
        paused: typing.Optional[bool] = None,
        force_motion: typing.Optional[bool] = None,
        aria_label: typing.Optional[str] = None,
        rate: typing.Optional[NumberType] = None,
        playing: typing.Optional[bool] = None,
        **kwargs
    ):
        self._prop_names = ['id', 'aria_label', 'className', 'color', 'density', 'force_motion', 'hue', 'particle_radius', 'paused', 'playing', 'rate', 'size', 'speed', 'state', 'style', 'theme']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'aria_label', 'className', 'color', 'density', 'force_motion', 'hue', 'particle_radius', 'paused', 'playing', 'rate', 'size', 'speed', 'state', 'style', 'theme']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(LoaderszLoader, self).__init__(**args)

setattr(LoaderszLoader, "__init__", _explicitize_args(LoaderszLoader.__init__))
