"""
Setup script for PyPerf-AI-CLI
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pyperf-ai-cli",
    version="1.0.0",
    author="gitstq",
    author_email="",
    description="🔥 Lightweight Terminal Python Code Performance Intelligence Engine",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gitstq/PyPerf-AI-CLI",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Debuggers",
        "Topic :: Software Development :: Testing",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "pyperf-ai=pyperf_ai.cli:main",
        ],
    },
    keywords="performance profiling python ai optimization cli terminal",
    project_urls={
        "Bug Reports": "https://github.com/gitstq/PyPerf-AI-CLI/issues",
        "Source": "https://github.com/gitstq/PyPerf-AI-CLI",
    },
)
