"""Setup module for Cloud Weather."""

import os
from pathlib import Path

from setuptools import find_packages, setup

PROJECT_DIR = Path(__file__).parent.resolve()
README_FILE = PROJECT_DIR / "README.md"
VERSION = os.getenv("PACKAGE_VERSION", "0.0.0")

setup(
    name="aiocloudweather",
    version=VERSION,
    url="https://github.com/lhw/aiocloudweather",
    download_url="https://github.com/lhw/aiocloudweather",
    author="Lennart Weller",
    description="Python wrapper for Cloud Weather protocols",
    long_description=README_FILE.read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=["tests.*", "tests"]),
    package_data={"aiocoudweather": ["py.typed"]},
    python_requires=">=3.12",
    install_requires=["aiohttp>3", "aiodns>3"],
    license_files=["LICENSE"],
    entry_points={
        "console_scripts": ["cloudweather-testserver = aiocloudweather.__main__:main"]
    },
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.12",
        "Topic :: Home Automation",
    ],
)
