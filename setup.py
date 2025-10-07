"""
Setup script for timeitPro.

This script allows the project to be installed as a Python package.
It specifies metadata, dependencies, minimum Python version, and entry points.

Usage:
    python setup.py install
    or
    python -m pip install .
"""

from setuptools import setup, find_packages

# -----------------------------
# Read long description from README.md
# -----------------------------
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

# -----------------------------
# Package setup
# -----------------------------
setup(
    # Package name
    name="timeitPro",

    # Package version
    version="0.2.2",

    # Author details
    author="Farahbakhsh3",
    author_email="farahbakhsh3@gmail.com",

    # Short description of the package
    description="Advanced Python function profiler with JSON logging and Flask dashboard",

    # Long description from README.md
    long_description=long_description,
    long_description_content_type="text/markdown",

    # Project URL / repository
    url="https://github.com/farahbakhsh3/timeitPro",

    # Automatically find all packages in this directory
    packages=find_packages(),

    # Minimum Python version required
    python_requires=">=3.9",

    # Dependencies required for this package
    install_requires=[
        "Flask>=2.0.0",  # Flask framework for the dashboard
        "psutil>=5.9.0"  # psutil for CPU and memory profiling
    ],

    # Classifiers help PyPI categorize the package
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],

    # Entry points for command-line scripts
    # Users can run 'timeitPro-dashboard' to start the Flask dashboard
    entry_points={
        "console_scripts": [
            "timeitPro-dashboard=timeitPro.dashboard:run_dashboard",
        ],
    },
)
