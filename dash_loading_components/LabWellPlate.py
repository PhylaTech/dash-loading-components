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


class LabWellPlate(Component):
    """A LabWellPlate component.
LabWellPlate — a 96-well microplate (8 rows by 12 columns, A1 corner
cut off) that a pipette fills well by well, row after row, until it is full.
It then empties in the same order and the next plate starts. Drawn as SVG
and CSS; dlc.flicker.WellPlate is the 7x7 dot-matrix take on it.

Keyword arguments:

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- aria_label (string; optional):
    Accessible name, announced to assistive technology (default
    \"Loading\").

- className (string; optional):
    CSS class applied to the outer wrapper.

- color (string; optional):
    Color of the liquid, the pipette and the plate outline (default
    currentColor).

- off_color (string; optional):
    Color of an empty well, drawn at `off_opacity` (default `color`).

- off_opacity (number; optional):
    Opacity of the empty wells, 0 to 1 (default 0.16).

- on_opacity (number; optional):
    Opacity of the liquid, 0 to 1 (default 1).

- playing (boolean; optional):
    Set to False to pause the animation.

- rate (number; optional):
    Relative tempo: 1.0 is this spinner's own tempo (a plate in about
    11 seconds), 2.0 twice as fast, 0.5 half.

- size (number; optional):
    CSS pixel width (default 64); the height follows the plate."""
    _children_props: typing.List[str] = []
    _base_nodes = ['children']
    _namespace = 'dash_loading_components'
    _type = 'LabWellPlate'


    def __init__(
        self,
        id: typing.Optional[typing.Union[str, dict]] = None,
        className: typing.Optional[str] = None,
        style: typing.Optional[typing.Any] = None,
        size: typing.Optional[NumberType] = None,
        color: typing.Optional[str] = None,
        on_opacity: typing.Optional[NumberType] = None,
        off_color: typing.Optional[str] = None,
        off_opacity: typing.Optional[NumberType] = None,
        aria_label: typing.Optional[str] = None,
        rate: typing.Optional[NumberType] = None,
        playing: typing.Optional[bool] = None,
        **kwargs
    ):
        self._prop_names = ['id', 'aria_label', 'className', 'color', 'off_color', 'off_opacity', 'on_opacity', 'playing', 'rate', 'size', 'style']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'aria_label', 'className', 'color', 'off_color', 'off_opacity', 'on_opacity', 'playing', 'rate', 'size', 'style']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(LabWellPlate, self).__init__(**args)

setattr(LabWellPlate, "__init__", _explicitize_args(LabWellPlate.__init__))
