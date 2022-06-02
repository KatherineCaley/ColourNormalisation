#!/usr/bin/env python
import pathlib
import sys

from setuptools import find_packages, setup

__author__ = "Katherine Caley"
__credits__ = ["Katherine Caley"]
__maintainer__ = "Katherine Caley"
__version__ = "2022.06.02"


if sys.version_info < (3, 6):
    py_version = ".".join([str(n) for n in sys.version_info])
    raise RuntimeError(
        "Python-3.6 or greater is required, Python-%s used." % py_version
    )

PROJECT_URLS = {
    "Documentation": "https://github.com/KatherineCaley/ColourNormalisation",
    "Bug Tracker": "https://github.com/KatherineCaley/ColourNormalisation/issues",
    "Source Code": "https://github.com/KatherineCaley/ColourNormalisation",
}

short_description = "ColourNormalisation"

readme_path = pathlib.Path(__file__).parent / "README.md"

long_description = readme_path.read_text()

PACKAGE_DIR = "src"

setup(
    name="ColourNormalisation",
    version=__version__,
    author="Katherine Caley",
    author_email="katherine.caley@anu.edu.au",
    description=short_description,
    long_description=long_description,
    long_description_content_type="text/x-rst",  # change if it's in markdown format
    platforms=["any"],
    keywords=["science"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    packages=find_packages(where="src"),
    package_dir={"": PACKAGE_DIR},
    url="https://github.com/KatherineCaley/ColourNormalisation",
    project_urls=PROJECT_URLS,
    install_requires=["numpy", "cogent3", "click", "accupy", "scipy"],
    entry_points={
        "console_scripts": [
            "demo_cli=colour_norm.demo:main"  # cli_name=python_package.module_name:function_name
        ]
    },
)
