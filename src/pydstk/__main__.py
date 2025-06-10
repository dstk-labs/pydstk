import argparse
import sys

from . import __version__


def main_cli(argv=None):
    """
    Main entry point for the pydstk CLI.
    """
    if argv is None:
        argv = sys.argv[1:]

    parser = argparse.ArgumentParser(description="Python CLI/SDK for DSTK.")
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )

    parser.parse_args(argv)


if __name__ == "__main__":
    main_cli()
