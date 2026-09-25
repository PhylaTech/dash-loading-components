"""The gallery must show each spinner as it really is.

The overview card and the component page both start from
`gallery.default_values`. If one of those differs from what upstream does
with the prop left out, the gallery shows a spinner nobody gets from
`dlc.<family>.<Name>()`, which is how SpinnerDots came to show three dots on
its page and eight in the overview. And the wrappers share one prop list per
family, so a control can be a no-op for one spinner (ClipLoader has no
margin); the gallery must not offer those.

Both checks compare what renders, not markup: react-spinners spreads props it
does not use onto its root as bare attributes, which changes the markup but
not the spinner. Animations are frozen at t=0 first, so two instances compare
equal at the same instant.
"""
import dash
from dash import Dash, html

import gallery
from dash_loading_components.registry import FAMILIES

dash._dash_renderer._set_react_version("19.2.4")

# Serializes the rendered state under every [data-probe] root: geometry,
# painted styles (pseudo-elements included, ldrs draws with them), SMIL
# attributes and text, walking into shadow roots.
RENDERED_STATE = r"""
const freeze = (root) => root.getAnimations().forEach((a) => { a.pause(); a.currentTime = 0; });
freeze(document);
const walk = (n, f) => {
  f(n);
  if (n.shadowRoot) { freeze(n.shadowRoot); [...n.shadowRoot.children].forEach((c) => walk(c, f)); }
  [...n.children].forEach((c) => walk(c, f));
};
document.querySelectorAll('svg').forEach((s) => { if (s.pauseAnimations) { s.pauseAnimations(); s.setCurrentTime(0); } });
const STYLES = ['display', 'visibility', 'opacity', 'color', 'background-color', 'background-image',
  'border-top-width', 'border-top-color', 'border-right-color', 'border-bottom-color',
  'border-left-color', 'border-top-style', 'border-radius', 'box-shadow', 'transform', 'scale',
  'rotate', 'translate', 'transform-origin', 'animation-name', 'animation-duration',
  'animation-delay', 'animation-direction', 'animation-timing-function', 'animation-play-state',
  'fill', 'fill-opacity', 'stroke', 'stroke-width', 'stroke-opacity', 'stroke-dasharray',
  'stroke-dashoffset', 'stroke-linecap', 'r', 'cx', 'cy', 'x', 'y', 'd', 'filter', 'font-size'];
const SMIL = new Set(['animate', 'animatetransform', 'animatemotion', 'set', 'stop',
  'lineargradient', 'radialgradient']);
const state = (probe) => {
  const pr = probe.getBoundingClientRect();
  const out = [];
  walk(probe, (e) => {
    if (e === probe) return;
    const t = e.tagName.toLowerCase();
    if (t === 'style' || t === 'script') return;
    const c = getComputedStyle(e);
    const r = e.getBoundingClientRect();
    const rect = !(r.width || r.height) ? ''
      : [r.left - pr.left, r.top - pr.top, r.width, r.height].map((v) => Math.round(v * 2) / 2).join(',');
    let s = t + '[' + rect + ']' + STYLES.map((k) => c.getPropertyValue(k)).join('|');
    for (const pe of ['::before', '::after']) {
      const pc = getComputedStyle(e, pe);
      if (pc.content && pc.content !== 'none') {
        s += pe + STYLES.map((k) => pc.getPropertyValue(k)).join('|') + pc.width + pc.height + pc.top + pc.left;
      }
    }
    if (SMIL.has(t)) s += '{' + [...e.attributes].map((a) => a.name + '=' + a.value).sort().join(' ') + '}';
    if (t === 'svg') s += '{' + (e.getAttribute('viewBox') || '') + '}';
    [...e.childNodes].forEach((n) => { if (n.nodeType === 3 && n.textContent.trim()) s += '"' + n.textContent.trim() + '"'; });
    out.push(s);
  });
  // React useId values differ per instance and surface in url(#id) fills,
  // and flicker-dot folds them into keyframe names (fkr9_0101...).
  return out.join('\n').replace(/«r[0-9a-z]+»|_r_[0-9a-z]+_|:r[0-9a-z]+:|\bfkr[0-9a-z]+(?=_)/g, '');
};
return Object.fromEntries([...document.querySelectorAll('[data-probe]')].map((e) => [e.dataset.probe, state(e)]));
"""

# react-spinners' GridLoader draws random delays; pin them so two renders agree.
SEEDED = "<head><script>Math.random = () => 0.5</script>"

# m3 draws on a canvas from requestAnimationFrame, so there is no DOM state to
# compare and no way to freeze it.
UNINSPECTABLE_FAMILIES = {"m3"}

# Props that change behaviour but not a frame: an accessible name, and a class
# that only does something once the page defines it.
NOT_VISUAL = {"aria_label", "className"}


def _spinners():
    for family, _label, items in FAMILIES:
        for name, component in items:
            props = gallery.configurable_props(family, name, component)
            yield family, name, component, props, gallery.default_values(family, name, props)


def _render(dash_duo, probes):
    app = Dash(__name__)
    app.index_string = app.index_string.replace("<head>", SEEDED, 1)
    app.layout = html.Div([html.Div(node, **{"data-probe": key}) for key, node in probes])
    dash_duo.start_server(app)
    dash_duo.wait_for_element("[data-probe]")
    dash_duo.driver.execute_script("return new Promise((r) => setTimeout(r, 1500));")
    return dash_duo.driver.execute_script(RENDERED_STATE)


def test_page_defaults_render_like_upstream(dash_duo):
    probes = []
    for family, name, component, _props, values in _spinners():
        explicit = {k: v for k, v in values.items() if v not in ("", None)}
        bare = {k: v for k, v in values.items() if k in gallery.ALWAYS_SENT}
        probes.append((f"{family}/{name}/gallery", gallery.instantiate(family, name, explicit)))
        probes.append((f"{family}/{name}/upstream", component(**bare)))
    state = _render(dash_duo, probes)

    drift = [
        key.rsplit("/", 1)[0]
        for key in state
        if key.endswith("/gallery") and state[key] != state[key.replace("/gallery", "/upstream")]
    ]
    assert not drift, (
        f"gallery defaults render differently from upstream for {drift}; "
        "correct them in gallery.UPSTREAM_DEFAULTS"
    )


def _changed(family, name, prop, value):
    spec = gallery.prop_spec(family, prop, name) or {"kind": "text"}
    if prop == "size":
        return "large" if family == "indicators" else 96
    if prop in ("color", "secondary_color", "text_color", "container_color"):
        return "#123456"
    if prop == "className":
        return "opacity-40"
    kind = spec["kind"]
    if kind == "slider":
        return spec["min"] if value != spec["min"] else spec["max"]
    if kind == "bool":
        return not value
    if kind in ("enum", "dropdown"):
        return [o for o in spec["options"] if o != value]
    return "Loading"


def test_every_control_changes_the_spinner(dash_duo):
    probes = []
    for family, name, _component, props, values in _spinners():
        if family in UNINSPECTABLE_FAMILIES:
            continue
        # A label color only shows once there is a label.
        base = {**values, **({"text": "Loading"} if "text_color" in props else {})}
        probes.append((f"{family}/{name}/-", gallery.instantiate(
            family, name, gallery.sent_values(family, name, base))))
        for prop in props:
            if prop in NOT_VISUAL or prop == "text" and "text_color" in props:
                continue
            # A choice is live if any option renders differently: an easing
            # control whose first option is the spinner's own curve still works.
            options = _changed(family, name, prop, values[prop])
            for i, option in enumerate(options if isinstance(options, list) else [options]):
                changed = {**base, prop: option}
                probes.append((f"{family}/{name}/{prop}#{i}", gallery.instantiate(
                    family, name, gallery.sent_values(family, name, changed))))
    state = _render(dash_duo, probes)

    live, tried = set(), set()
    for key, rendered in state.items():
        if key.endswith("/-"):
            continue
        control, spinner = key.split("#")[0], key.rsplit("/", 1)[0]
        tried.add(control)
        if rendered != state[spinner + "/-"]:
            live.add(control)
    dead = sorted(tried - live)
    assert not dead, f"controls that change nothing: {dead}; list them in gallery.IGNORED_PROPS"
