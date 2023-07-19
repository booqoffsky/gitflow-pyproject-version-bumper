#!/usr/bin/env python
import pathlib
import sys

import git
import tomlkit

BRANCH_CHECKOUT_TYPE = "1"

checkout_type = sys.argv[-1]
if checkout_type != BRANCH_CHECKOUT_TYPE:
    exit()

repo = git.Repo()
try:
    head = repo.active_branch
except TypeError:
    exit()

pyproject_toml_path = pathlib.Path(repo.working_dir).joinpath("pyproject.toml")
with repo.config_reader() as git_config:
    gitflow_release_prefix = git_config.get(
        section='gitflow "prefix"',
        option="release",
        fallback="release/",
    )
    gitflow_hotfix_prefix = git_config.get(
        section='gitflow "prefix"',
        option="hotfix",
        fallback="hotfix/",
    )
    commit_message_template = git_config.get(
        section="versionbumper",
        option="commitmessagetemplate",
        fallback="Version bumped to {version}",
    )

if head.name.startswith(gitflow_release_prefix):
    new_version = repo.active_branch.name[len(gitflow_release_prefix) :]
elif head.name.startswith(gitflow_hotfix_prefix):
    new_version = repo.active_branch.name[len(gitflow_hotfix_prefix) :]
else:
    exit()

with open(pyproject_toml_path, "rb") as f:
    pyproject = tomlkit.load(f)

if pyproject["tool"]["poetry"]["version"] == new_version:
    exit()

pyproject["tool"]["poetry"]["version"] = new_version
with open(pyproject_toml_path, "w") as f:
    tomlkit.dump(pyproject, f)

repo.index.add(str(pyproject_toml_path))
repo.index.commit(commit_message_template.format(version=new_version))
