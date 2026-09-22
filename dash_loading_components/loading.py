"""``dlc.Loading`` — thin factory over registered family spinners.

Day-one: registry lookup + common props with relative ``speed`` translation.
Namespaced ``dlc.<family>.<Name>(...)`` remains the fidelity / power path.
Children / overlay → ``dlc.LoadingOverlay`` (phase 2; not here).
"""
from __future__ import annotations

from typing import Any, Optional

from .registry import (
    NATIVE_TEMPO_CONFLICT_KEYS,
    get_component,
    list_libraries,
    list_spinners,
    playing_kwargs,
    supports_relative_speed,
    translate_relative_speed,
)


def Loading(
    library: Optional[str] = None,
    spinner: Optional[str] = None,
    *,
    size: Any = None,
    color: Optional[str] = None,
    speed: Optional[float] = 1.0,
    className: Optional[str] = None,
    playing: bool = True,
    id: Any = None,
    style: Any = None,
    **kwargs: Any,
):
    """Build a registered family spinner with a small common prop surface.

    Parameters
    ----------
    library, spinner :
        Registry IDs (same strings as the gallery). May be positional:
        ``Loading("loading_dev", "Dual", ...)``.
    size :
        Linear size in px (number), or family-native size token when that
        family uses tokens (e.g. indicators ``"medium"``).
    color :
        Primary CSS color string.
    speed :
        **Relative** rate. ``1.0`` = that family's normal tempo. Translated
        per family (duration ms, multiplier, percent, speedPlus, …).
        Never a shared physical unit across families.
    className :
        CSS class pass-through.
    playing :
        Whether the animation runs; mapped to pause/stop props when the
        family supports them, otherwise omitted.
    id, style :
        Dash component id / style.
    **kwargs :
        Exotic / upstream-native props (easing, cap, thickness, …).
        Passing a native tempo prop together with relative ``speed`` raises
        ``ValueError``.

    Returns
    -------
    The underlying Dash component instance (namespaced class).
    """
    if not library or not isinstance(library, str):
        raise ValueError(
            "library is required (non-empty string). "
            f"Known: {', '.join(list_libraries())}"
        )
    if not spinner or not isinstance(spinner, str):
        raise ValueError(
            "spinner is required (non-empty string). "
            f"For library {library!r}: {', '.join(list_spinners(library)) if library in list_libraries() else '(unknown library)'}"
        )

    component_cls = get_component(library, spinner)

    # Conflict: relative speed + native tempo unit under a different name
    conflicts = NATIVE_TEMPO_CONFLICT_KEYS.intersection(kwargs)
    # Also: if relative speed is set and kwargs already contains the native
    # tempo prop name for this family when that name is NOT "speed"
    # (when native IS "speed", the Loading kwarg `speed` is the relative one —
    # there is no separate escape hatch via the same name; use namespaced API).
    from .registry import native_tempo_prop

    native_prop = native_tempo_prop(library)
    if (
        speed is not None
        and native_prop
        and native_prop != "speed"
        and native_prop in kwargs
    ):
        conflicts = set(conflicts) | {native_prop}

    if speed is not None and conflicts:
        raise ValueError(
            f"Conflicting tempo props: pass relative speed=… OR native "
            f"{sorted(conflicts)}, not both. "
            "Omit speed to own the native unit via kwargs / namespaced API."
        )

    props: dict[str, Any] = {}
    if id is not None:
        props["id"] = id
    if style is not None:
        props["style"] = style
    if size is not None:
        props["size"] = size
    if color is not None:
        props["color"] = color
    if className is not None and className != "":
        props["className"] = className

    # Relative speed → native (only when family supports it)
    if speed is not None and supports_relative_speed(library):
        props.update(translate_relative_speed(library, speed))

    # playing → native pause/run when supported
    play_map = playing_kwargs(library, playing)
    for k, v in play_map.items():
        # Don't override if user already passed the native key
        if k not in kwargs:
            props[k] = v

    # Passthrough exotic / native extras (allowlisted by the component itself)
    for k, v in kwargs.items():
        if v is not None:
            props[k] = v

    return component_cls(**props)


__all__ = [
    "Loading",
    "list_libraries",
    "list_spinners",
    "translate_relative_speed",
    "supports_relative_speed",
]
