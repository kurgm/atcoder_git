#!/usr/bin/env python3
from setuptools import setup
from setuptools import find_packages

import atcoder_git


setup(
    name="atcoder_git",
    version=atcoder_git.__version__,
    author="kurgm",
    license="MIT",
    description="Build git repository from AtCoder submissions",
    url="https://github.com/kurgm/atcoder_git",
    packages=find_packages(),
    install_requires=list(open("requirements.txt")),
    entry_points={
        "console_scripts": [
            "atcoder_git = atcoder_git.atcoder_git:main",
        ],
    },
)
