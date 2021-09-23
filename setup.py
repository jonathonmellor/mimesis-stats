import pathlib

import pkg_resources
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


with pathlib.Path("requirements.txt").open() as requirements_txt:
    install_requires = [str(requirement) for requirement in pkg_resources.parse_requirements(requirements_txt)]

with pathlib.Path("requirements.dev.txt").open() as dev_requirements_txt:
    dev_specific_install_requires = [
        str(requirement) for requirement in pkg_resources.parse_requirements(dev_requirements_txt)
    ]

dev_install_requires = dev_specific_install_requires + install_requires

setuptools.setup(
    name="mimesis_stats",
    version="0.0.3",
    author="Jonathon Mellor",
    author_email="mellorjonathon1@gmail.com",
    description=("Extension of mimesis library for data generation with statistical properties"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    download_url="https://github.com/jonathonmellor/mimesis-stats/archive/refs/tags/v0.0.3.tar.gz",
    url="https://github.com/jonathonmellor/mimesis-stats",
    project_urls={
        "Bug Tracker": "https://github.com/jonathonmellor/mimesis-stats/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6.8",
    install_requires=install_requires,
    extras_require={"dev": dev_install_requires, "ci": dev_install_requires},
)
