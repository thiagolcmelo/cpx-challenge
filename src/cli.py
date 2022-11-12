from datetime import datetime
import sys
from argparse import ArgumentParser, Namespace, ArgumentTypeError
from csv import DictWriter
from pathlib import Path
from typing import List


DESCRIPTION = "CLI tool for fetching and watching CPX servers"
SNAPSHOT_PROG = "cpx_utils snapshot"
SNAPSHOT_EPILOG = """
Fetches information from CPX one single time and display as specified.
The default format is 'table', but 'csv' and 'json' are also available.
"""
WATCH_PROG = "cps_utils watch"
WATCH_EPILOG = """
Continuously fetches information from CPX and display as specified.
"""
DETAILS_HELP = "the level of detail in the output information"
FORMAT_HELP = "determines the output format"
REFRESH_HELP = "the refresh period in seconds, between 1 and 60 inclusive"
MODE_HELP = "the amount of information displayed"
HOST_HELP = "cpx api host"
PORT_HELP = "cpx api port"
IPV_HELP = "ip protocol version"


def snapshot(args: Namespace, parser: ArgumentParser) -> None:
    """Main helper for snapshot operation that fetches information once."""
    pass


def watch(args: Namespace, parser: ArgumentParser) -> None:
    """Main helper for watch operation that continuously fetches information."""
    pass


def config_parser_snapshot(parser: ArgumentParser) -> None:
    """Configures sub parser for snapshot."""
    parser.add_argument(
        "--format",
        "-f",
        dest="format",
        required=False,
        choices=("csv", "json", "table"),
        default="table",
        help=FORMAT_HELP,
    )
    parser.add_argument(
        "--details",
        "-d",
        dest="details",
        required=False,
        choices=("summary", "full"),
        default="summary",
        help=DETAILS_HELP,
    )
    parser.set_defaults(func=snapshot)


def config_parser_watch(parser: ArgumentParser) -> None:
    """Configures sub parser for watch."""

    def check_refresh_range(value):
        ivalue = int(value)
        if ivalue < 1 or ivalue > 60:
            raise ArgumentTypeError(
                f"refresh must be between 1 and 60 inclusive, found {value}"
            )
        return ivalue

    parser.add_argument(
        "--refresh",
        "-r",
        dest="refresh",
        required=False,
        type=check_refresh_range,
        default=1,
        help=REFRESH_HELP,
    )
    parser.add_argument(
        "--mode",
        "-m",
        dest="mode",
        required=False,
        type=str,
        choices=("simple", "complete"),
        default="simple",
        help=MODE_HELP,
    )
    parser.set_defaults(func=watch)


def create_parser():
    """Builds a parser."""
    parser = ArgumentParser(description=DESCRIPTION)
    parser.add_argument(
        "--host",
        "-b",
        dest="host",
        required=True,
        type=str,
        help=HOST_HELP,
    )
    parser.add_argument(
        "--port",
        "-p",
        dest="port",
        required=True,
        type=int,
        help=PORT_HELP,
    )
    parser.add_argument(
        "--ip-version",
        "-i",
        dest="ip_version",
        required=False,
        type=int,
        choices=(4, 6),
        default=4,
        help=PORT_HELP,
    )
    subparsers = parser.add_subparsers(help="actions")
    parser_snapshot = subparsers.add_parser(
        "snapshot",
        help="fetch cpx information",
        prog=SNAPSHOT_PROG,
        epilog=SNAPSHOT_EPILOG,
    )
    config_parser_snapshot(parser_snapshot)
    parser_watch = subparsers.add_parser(
        "watch",
        help="continuously fetch cpx information",
        prog=WATCH_PROG,
        epilog=WATCH_EPILOG,
    )
    config_parser_watch(parser_watch)
    return parser


def main():
    """CLI entry point."""
    parser = create_parser()
    if not sys.stdin.isatty():
        input_string = sys.stdin.read()
        args = parser.parse_args([input_string] + sys.argv[1:])
    else:
        args = parser.parse_args()
    args.func(args, parser)


if __name__ == "__main__":
    main()
