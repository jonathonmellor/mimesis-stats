import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


def read_requirements(file):
    with open(file) as f:
        return f.read().splitlines()


requires = read_requirements("requirements.txt")

dev_requires = read_requirements("requirements.dev.txt") + requires

setuptools.setup(
    name="mimesis_stats",
    version="0.0.1",
    author="Jonathon Mellor",
    author_email="mellorjonathon1@gmail.com",
    description=("Extension of mimesis library for data generation with statistical properties"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    download_url="https://github.com/jonathonmellor/mimesis-stats/archive/refs/tags/v0.0.1.tar.gz",
    url="https://github.com/jonathonmellor/mimesis-stats",
    project_urls={
        "Bug Tracker": "https://github.com/jonathonmellor/mimesis-stats/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(where="src"),
    python_requires="==3.6.8",
    install_requires=requires,
    extras_require={"dev": dev_requires, "ci": dev_requires},
)
