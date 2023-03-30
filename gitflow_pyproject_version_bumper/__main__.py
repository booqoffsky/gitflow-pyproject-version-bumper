import argparse
import os
import pathlib
import shutil
import stat
import sys

import git


def install(*args, **kwargs):
    """Install git post-checkout hook."""
    repo = git.Repo()
    src = pathlib.Path(os.path.dirname(__file__)).joinpath("post_checkout.py")
    dst = pathlib.Path(repo.git_dir).joinpath("hooks").joinpath("post-checkout")
    shutil.copyfile(src, dst)
    dst.chmod(dst.stat().st_mode | stat.S_IEXEC)


def main():
    """
    Main entrypoint.

    This function collects all python entrypoints
    and assembles a final argument parser.
    All found entrypoints are used as subcommands.
    """
    parser = argparse.ArgumentParser(
        description="CLI for gitflow_pyproject_version_bumper.",
    )
    subparsers = parser.add_subparsers(
        title="Available subcommands",
        metavar="",
        dest="subcommand",
    )
    subparsers.add_parser(
        "install",
        help="install git hook",
        add_help=False,
    )
    subcommands = {
        "install": install,
    }
    args, _ = parser.parse_known_args()

    if args.subcommand is None:
        parser.print_help()
        return

    command = subcommands[args.subcommand]
    sys.argv.pop(0)
    command(sys.argv[1:])


if __name__ == "__main__":
    main()
