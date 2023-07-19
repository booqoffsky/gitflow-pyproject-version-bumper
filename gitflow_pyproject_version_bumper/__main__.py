import argparse
import pathlib
import shutil
import stat

import git


def install(force: bool, commit_message_template: str) -> None:
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

    version_bumper_section_name = "versionbumper"
    with repo.config_writer() as git_config:
        if not git_config.has_section(version_bumper_section_name):
            git_config.add_section(version_bumper_section_name)

        git_config.set(
            section=version_bumper_section_name,
            option="commitmessagetemplate",
            value=commit_message_template,
        )

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
    install_cmd_parser.add_argument(
        "--commit-message-template",
        dest="commit_message_template",
        action="store",
        default="Version bumped to {version}",
        help="commit message when updating the version. "
        "Default: Version bumped to {version}",
    )
    args, _ = parser.parse_known_args()

    if args.subcommand is None:
        parser.print_help()
        return

    if args.subcommand == "install":
        install(args.force_install, args.commit_message_template)


if __name__ == "__main__":
    main()
