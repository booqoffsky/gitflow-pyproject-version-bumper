import argparse
import pathlib
import shutil
import stat

import git


def install(force: bool) -> None:
    """
    Install git post-checkout hook.

    :param force: overwrite hook if it exists.
    """
    repo = git.Repo()
    src = pathlib.Path(__file__).parent / "post_checkout.py"
    dst = pathlib.Path(repo.git_dir) / "hooks" / "post-checkout"

    if dst.exists() and not force:
        print(
            "Error: another post-checkout hook has already been installed. "
            "To overwrite it, use the --force option.",
        )
        exit(-1)

    shutil.copyfile(src, dst)
    dst.chmod(dst.stat().st_mode | stat.S_IEXEC)


def main() -> None:
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

    install_cmd_parser = subparsers.add_parser(
        "install",
        help="install git hook",
    )
    install_cmd_parser.add_argument(
        "--force",
        dest="force_install",
        action="store_true",
        default=False,
        help="overwrite hook if it exists",
    )
    args, _ = parser.parse_known_args()

    if args.subcommand is None:
        parser.print_help()
        return

    if args.subcommand == "install":
        install(args.force_install)


if __name__ == "__main__":
    main()
