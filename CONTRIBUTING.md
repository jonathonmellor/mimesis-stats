# Contributing

Welcome to the project! Thanks for taking a look.

This is an extension package for `mimesis` intending to make data with statistical and structured properties work better with `mimesis` data providers.

Any contribution is welcome, but in particular:

* Bug reporting
* Feature ideas / enhancements

It's important most of all that this package is _useful_, for that to be the case we need example use cases that can be solved using this package.

### Issue Tracking

Please add issues to the [issues tab](https://github.com/jonathonmellor/mimesis-stats/issues) of the GitHub repository.

Please also use the issues feature for any enhancements or additions you would like to see in the project.

### Pull Requests

1. Branch of the `main` branch, with an informative branch name.
2. Update the README.md and other documentation with any relevant changes.
3. Ensure if new behaviours are being added that relevant tests are included in the PR.
4. Complete the [PR Template](https://github.com/jonathonmellor/mimesis-stats/blob/main/.github/PULL_REQUEST_TEMPLATE.md)
4. Submit the merge request and select @jonathonmellor as reviewer.
5. Merge to `main` once the code has been approved.

All existing tests are expected to run locally, and the hooks from `.pre-commit-config.yaml` run.

### Code Style

The code in this project:

* Uses type hinting for all functions/classes/methods.
* Otherwise follows [numpydoc](https://numpydoc.readthedocs.io/en/latest/format.html) for doctrings.
* Uses styling through `black` and `flake8`.
* Uses lowercase naming conventions where appropriate following PEP8.

### Development Setup

Development installation
Create a new virtual environment, including python 3.6.8. conda can be used for this purpose:

```sh
conda create -n "mimesis-stats" python=3.6.8
```

Download the repository using git clone and change directory into the project.

Activate the conda environment and install the project development dependencies:

```sh
activate mimesis-stats
pip install -e .[dev]
```




The contents of this document has largely been taken from the [CIS CONTRIBUTING.md](https://github.com/ONS-SST/cis_households/blob/main/CONTRIBUTING.md) and @foster999, a big thank you to them.
