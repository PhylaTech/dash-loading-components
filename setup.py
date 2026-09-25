import json
from setuptools import setup, find_packages
from pathlib import Path

here = Path(__file__).parent
with open('package.json') as f:
    package = json.load(f)
long_description = (here / 'README.md').read_text()

package_name = package["name"].replace(" ", "_").replace("-", "_")

# npm stores one "Name <email>" string; Python wants the two apart, so that
# PyPI renders a name and a mailto rather than one run-together field.
# dash-generate-components parses this field the same way, which is why
# package.json cannot use npm's object form here.
author_name, _, author_email = package["author"].partition(" <")
author_email = author_email.rstrip(">")

setup(
    name=package_name,
    version=package["version"],
    author=author_name,
    author_email=author_email,
    # The family namespaces (dlc.epic, dlc.ldrs, ...) are real subpackages and
    # are imported from __init__.py, so they must ship in the distribution.
    packages=find_packages(include=[package_name, package_name + '.*']),
    include_package_data=True,
    license=package['license'],
    description=package.get('description', package_name),
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=['dash>=4.5.0rc0'],
    classifiers = [
        'Framework :: Dash',
    ],    
)
