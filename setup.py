#!/usr/bin/env python3
from setuptools import setup, find_packages

setup(
    name="antigravity-manager",
    version="1.0.0",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "agm=agm.cli:main",
            "agy-multi=agm.cli:main",
        ],
    },
)
