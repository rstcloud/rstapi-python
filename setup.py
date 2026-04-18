import re
from pathlib import Path

from setuptools import setup

LONG_DESCRIPTION = (Path(__file__).parent / "README.md").read_text(encoding="utf-8")

with open("rstapi/__init__.py", "r") as fd:
    version = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', fd.read(), re.MULTILINE
    ).group(1)

if not version:
    raise RuntimeError("Could not find version information")

setup(
    name="rstapi",
    version=version,
    description="Python library to access the RST Cloud API.",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/rstcloud/rstapi-python",
    author="RST Cloud Pty Ltd",
    author_email="support@rstcloud.com, ysergeev@rstcloud.com",
    license="MIT",
    packages=["rstapi"],
    keywords=["threat intelligence", "RST Cloud", "IoC lookup", "Whois API", "Enrichment API"],
    install_requires=[
        "requests"
    ],
    extras_require={
        "test": ["pytest>=7"],
    },
    package_data={
        "": ["*.md", "LICENSE"],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Security",
        "Programming Language :: Python :: 3",
    ],
)
