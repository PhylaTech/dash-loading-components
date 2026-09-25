from dash import Dash, html
from dash._dash_renderer import _set_react_version

# The bundle is built against React 19; Dash still defaults to 18. Set it
# explicitly rather than via REACT_VERSION so import order cannot matter.
_set_react_version("19.2.4")

import dash_loading_components as dlc  # noqa: E402

app = Dash(__name__)

app.layout = html.Div(
    [
        # Every component takes size, color, rate (1.0 = its own tempo) and playing.
        dlc.loading_dev.Arc(size=48, color="#f97316", rate=1.5),
        # Upstream props are there too, in snake_case, in upstream units.
        dlc.ldrs.Mirage(id="mirage", size=60, color="#f97316", speed=2.5),
    ],
    id="demo",
)


if __name__ == '__main__':
    app.run(debug=True)
