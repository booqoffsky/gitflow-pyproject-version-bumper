![python version](https://img.shields.io/pypi/pyversions/gitflow-pyproject-version-bumper?style=for-the-badge) 
[![version](https://img.shields.io/pypi/v/gitflow-pyproject-version-bumper?style=for-the-badge)](https://pypi.org/project/gitflow-pyproject-version-bumper/)

# gitflow-pyproject-version-bumper
> A git hook to automatically update the application version 
> in pyproject.toml when a release is started using [gitflow](https://github.com/nvie/gitflow).

# Installation
From PyPi:

```
pip3 install gitflow-pyproject-version-bumper
python3 -m gitflow_pyproject_version_bumper install
```

If you want to install it from sources, try this:

```
python3 -m pip install poetry
python3 -m pip install .
python3 -m gitflow_pyproject_version_bumper install
```

Install options:
```
  --force               overwrite hook if it exists
  --commit-message-template COMMIT_MESSAGE_TEMPLATE
                        commit message when updating the version. 
                        Default: Version bumped to {version}
```
`{version}` - placeholder for the new version.

# Usage
Just start a release, as you usually do:
`git flow release start 1.2.3`

That's it.
The app version in pyproject.toml has already been updated, 
and the change has been committed.
