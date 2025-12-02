#!/usr/bin/env python3
"""Setup configuration for mobsf-cli."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="mobsf-cli",
    version="0.1.0",
    author="Wojciech Zurek",
    author_email="mail@wojciechzurek.eu",
    description="CLI wrapper for Mobile Security Framework (MobSF) REST API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wojciech-zurek/mobsf-cli",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Security",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.28.0",
        "tabulate>=0.9.0",
        "python-dateutil>=2.8.0",
    ],
    entry_points={
        "console_scripts": [
            "mobsf-cli=cli.main:main",
        ],
    },
)
