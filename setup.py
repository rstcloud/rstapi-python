import re
from pathlib import Path

from setuptools import setup

LONG_DESCRIPTION = (Path(__file__).parent / "README.md").read_text()

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
    author_email="support@rstcloud.net, ysergeev@rstcloud.net",
    license="MIT",
    packages=["rstapi"],
    keywords=["threat intelligence", "RST Cloud", "IoC lookup", "Whois API"],
    install_requires=[
        "requests"
    ],
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
