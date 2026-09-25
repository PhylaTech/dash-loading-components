"""No overview card may clip its own spinner.

Card previews are a fixed slot with `overflow: hidden`, and several loaders
animate well outside their layout box: dots that bounce above it, dots that
propagate sideways, sweeps that run off both edges. A loader whose extent is
only checked at rest looks fine in a screenshot and is visibly chopped in
motion, so this samples every card over a couple of animation cycles and
measures the ink that actually paints.
"""
import time

from dash.testing.application_runners import import_app

# Returns {"family/Name": [overTop, overLeft, overBottom, overRight]} in px,
# negative past the top/left edge and positive past the bottom/right, 0 when
# the loader stays inside. Only elements that paint something count, and each
# rect is intersected with any clipping ancestor first: several loaders
# (react-spinners BarLoader, premium ShimmerBox) deliberately overflow inside
# their own `overflow: hidden` wrapper, which is not a clipped card.
CLIP_SCAN = """
const paints = (el) => {
  const c = getComputedStyle(el);
  if (c.visibility === 'hidden' || c.display === 'none') return false;
  if (parseFloat(c.opacity) === 0) return false;
  if (c.backgroundColor && c.backgroundColor !== 'rgba(0, 0, 0, 0)') return true;
  if (c.backgroundImage && c.backgroundImage !== 'none') return true;
  if (c.boxShadow && c.boxShadow !== 'none') return true;
  for (const s of ['Top', 'Right', 'Bottom', 'Left']) {
    if (parseFloat(c['border' + s + 'Width']) > 0) {
      const col = c['border' + s + 'Color'];
      if (col && col !== 'rgba(0, 0, 0, 0)') return true;
    }
  }
  const tag = el.tagName.toLowerCase();
  if (['svg', 'circle', 'path', 'rect', 'ellipse', 'line', 'polyline', 'polygon'].includes(tag)) {
    const fill = c.fill && c.fill !== 'none' && c.fill !== 'rgba(0, 0, 0, 0)';
    const stroke = c.stroke && c.stroke !== 'none' && c.stroke !== 'rgba(0, 0, 0, 0)'
      && parseFloat(c.strokeWidth) > 0;
    return fill || stroke;
  }
  return false;
};
const visibleRect = (el, stop) => {
  let r = el.getBoundingClientRect();
  let p = el.parentElement;
  while (p && p !== stop) {
    if (getComputedStyle(p).overflow !== 'visible') {
      const pr = p.getBoundingClientRect();
      const top = Math.max(r.top, pr.top), left = Math.max(r.left, pr.left);
      const bottom = Math.min(r.bottom, pr.bottom), right = Math.min(r.right, pr.right);
      if (bottom <= top || right <= left) return null;
      r = {top, left, bottom, right, width: right - left, height: bottom - top};
    }
    p = p.parentElement;
  }
  return r;
};
const out = {};
document.querySelectorAll('.dlc-card').forEach((card) => {
  const prev = card.querySelector('.preview');
  if (!prev) return;
  const pr = prev.getBoundingClientRect();
  const o = [0, 0, 0, 0];
  prev.querySelectorAll('*').forEach((k) => {
    if (!paints(k)) return;
    const r = visibleRect(k, prev);
    if (!r || (!r.width && !r.height)) return;
    o[0] = Math.min(o[0], r.top - pr.top);
    o[1] = Math.min(o[1], r.left - pr.left);
    o[2] = Math.max(o[2], r.bottom - pr.bottom);
    o[3] = Math.max(o[3], r.right - pr.right);
  });
  out[card.dataset.family + '/' + card.dataset.name] = o;
});
return out;
"""

# Sub-pixel rounding and antialiasing put rects a pixel or two outside the slot
# without anything being visibly cut, and the exact amount moves with the
# driver. Every real clip this test was written for was 8px or more.
TOLERANCE_PX = 2.0


def test_no_overview_card_clips_its_spinner(dash_duo):
    app = import_app('gallery')
    dash_duo.start_server(app)
    dash_duo.driver.set_window_size(1440, 1200)
    dash_duo.wait_for_element('.dlc-card')

    worst: dict[str, list[float]] = {}
    deadline = time.time() + 3.0
    while time.time() < deadline:
        for key, over in dash_duo.driver.execute_script(CLIP_SCAN).items():
            prev = worst.setdefault(key, [0.0, 0.0, 0.0, 0.0])
            prev[0] = min(prev[0], over[0])
            prev[1] = min(prev[1], over[1])
            prev[2] = max(prev[2], over[2])
            prev[3] = max(prev[3], over[3])
        time.sleep(0.05)

    assert worst, "no cards were measured"
    clipped = {
        key: [round(v, 1) for v in over]
        for key, over in worst.items()
        if min(over[0], over[1]) < -TOLERANCE_PX or max(over[2], over[3]) > TOLERANCE_PX
    }
    assert not clipped, (
        "overview cards clip their spinner (px past top/left/bottom/right): "
        f"{clipped}. Give them an OVERVIEW_SCALE entry or a smaller preview size."
    )
