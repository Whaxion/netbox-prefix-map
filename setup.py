from pathlib import Path
from setuptools import find_packages, setup

readme = Path(__file__).parent / "README.md"
long_description = readme.read_text()

setup(
    name='netbox-prefix-map',
    version='0.1',
    description='NetBox plugin to view usage of prefixes in an IP map',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)