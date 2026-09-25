"""The generated wrappers have to match the React sources they come from.

Everything in `dash_loading_components/` except `loading.py`, `registry.py` and
the family packages is emitted by `dash-generate-components`. Edit a React
wrapper without re-running the build and the committed Python keeps the old
prop list, silently rejecting props the component really supports. That is how
`PremiumShimmerBox` came to ship without `width` or `height`.

Comparing the generated Python against `metadata.json` would not catch it:
both come out of the same build, so they go stale together. The React sources
are the only independent truth here.
"""
import json
import pathlib
import re

import pytest

REPO = pathlib.Path(__file__).resolve().parent.parent
SOURCES = sorted((REPO / "src" / "lib" / "components").rglob("*.react.js"))

# Dash's own callback hook, not a settable property.
NOT_A_PROPERTY = {"setProps"}


def react_prop_names(source: pathlib.Path) -> tuple[str, list[str]]:
    """Return (component name, declared propTypes keys) for one wrapper."""
    text = source.read_text()
    match = re.search(r"(\w+)\.propTypes\s*=\s*\{", text)
    assert match, f"no propTypes block in {source.name}"
    name = match.group(1)

    depth, index = 1, match.end()
    while depth and index < len(text):
        depth += {"{": 1, "}": -1}.get(text[index], 0)
        index += 1
    block = text[match.end(): index - 1]

    # Only keys at the top level of the block are props; anything deeper
    # belongs to a PropTypes.shape or an oneOf list.
    props, depth = [], 0
    for line in block.splitlines():
        if depth == 0:
            key = re.match(r"\s*(\w+):\s*PropTypes\b", line)
            if key:
                props.append(key.group(1))
        depth += line.count("{") + line.count("[") - line.count("}") - line.count("]")
    return name, props


CASES = [react_prop_names(s) for s in SOURCES]


def test_every_source_was_parsed():
    assert len(CASES) == 107, len(CASES)


@pytest.mark.parametrize("display_name,react_props", CASES)
def test_generated_wrapper_exposes_every_react_prop(display_name, react_props):
    import dash_loading_components as dlc

    assert react_props, display_name
    component = getattr(dlc, display_name)
    exposed = set(component().available_properties)
    missing = {p for p in react_props if p not in NOT_A_PROPERTY} - exposed
    assert not missing, (
        f"{display_name} was generated from an older version of "
        f"{display_name}.react.js and is missing {sorted(missing)}. "
        "Re-run `npm run build`."
    )


def test_package_author_is_the_company():
    package = json.loads((REPO / "package.json").read_text())
    assert package["author"] == "Phyla Technologies <hello@phylatech.com>"
