import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

install_requires = ["mimesis>=4.1.3", "numpy>=1.19.5"]

dev_specific_install_requires = [
    "pre-commit==2.12.1",
    "pandas>=1.1.5",
    "pytest>=3.6,<4",
    "pytest-regressions==2.2.0",
    "scipy>=1.5.4",
]

dev_install_requires = dev_specific_install_requires + install_requires

setuptools.setup(
    name="mimesis_stats",
    version="0.1.1",
    author="Jonathon Mellor",
    author_email="mellorjonathon1@gmail.com",
    description=("Extension of mimesis library for data generation with statistical properties"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    download_url="https://github.com/jonathonmellor/mimesis-stats/archive/refs/tags/v0.1.1.tar.gz",
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
    package_dir={"": "src"},
    python_requires=">=3.6.8",
    install_requires=install_requires,
    extras_require={"dev": dev_install_requires, "ci": dev_install_requires},
)
