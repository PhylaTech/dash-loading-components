from dash.testing.application_runners import import_app


# Smoke test that the bundled JS actually mounts a spinner in a browser.
# The dash_duo pytest fixture is installed with dash (v1.0+).
def test_render_component(dash_duo):
    app = import_app('usage')
    dash_duo.start_server(app)

    dash_duo.wait_for_element('#demo')
    # ldrs drives its animation off --uib-speed, in seconds per loop.
    dash_duo.wait_for_element('#mirage div[style*="--uib-speed"]')

    assert dash_duo.driver.execute_script(
        "return getComputedStyle("
        "  document.querySelector('#mirage div[style*=\"--uib-speed\"]')"
        ").getPropertyValue('--uib-speed').trim();"
    ) == '2.5s'

    assert dash_duo.get_logs() == []
