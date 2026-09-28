"""The snippet on a gallery page has to be the call that page really is.

Every card and every component page shows `build_snippet` output for the user
to copy. The entry name is the callable for every family but gridora, whose
133 pages are all one `GridLoader` picked by `variant`; rendering
`dlc.gridora.orbit(...)` there shipped 133 pages of code that raises
AttributeError. So run every snippet.
"""
import gallery


def test_every_snippet_runs():
    namespace = {}
    for family, name in gallery.CATALOG:
        values = gallery.sent_values(
            family, name,
            gallery.default_values(
                family, name,
                gallery.configurable_props(family, name, gallery.COMPONENT_LOOKUP[(family, name)]),
            ),
        )
        snippet = gallery.build_snippet(family, name, values)
        exec(snippet, namespace)  # noqa: S102 - the snippet is ours, and must run
