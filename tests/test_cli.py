import io, sys
from contextlib import contextmanager
import pytest
from src.cli import create_parser


@contextmanager
def captured_output():
    new_out, new_err = io.StringIO(), io.StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err


def test_parser_snapshot_with_basic_args():
    parser = create_parser()
    args = parser.parse_args(
        [
            "-b",
            "localhost",
            "-p",
            "8080",
            "snapshot",
        ]
    )
    assert args.host == "localhost"
    assert args.port == 8080
    assert args.ip_version == 4
    assert args.format == "table"
    assert args.details == "summary"


def test_parser_snapshot_with_specific_args():
    parser = create_parser()
    args = parser.parse_args(
        [
            "-b",
            "localhost",
            "-p",
            "8080",
            "-i",
            "6",
            "snapshot",
            "-d",
            "full",
            "-f",
            "csv",
        ]
    )
    assert args.host == "localhost"
    assert args.port == 8080
    assert args.ip_version == 6
    assert args.format == "csv"
    assert args.details == "full"


def test_parser_watch_with_basic_args():
    parser = create_parser()
    args = parser.parse_args(
        [
            "-b",
            "localhost",
            "-p",
            "8080",
            "watch",
        ]
    )
    assert args.host == "localhost"
    assert args.port == 8080
    assert args.mode == "simple"
    assert args.refresh == 1


def test_parser_watch_with_specific_args():
    parser = create_parser()
    args = parser.parse_args(
        [
            "-b",
            "localhost",
            "-p",
            "8080",
            "-i",
            "6",
            "watch",
            "-m",
            "complete",
            "-r",
            "20",
        ]
    )
    assert args.host == "localhost"
    assert args.port == 8080
    assert args.ip_version == 6
    assert args.mode == "complete"
    assert args.refresh == 20


def test_parser_watch_enforces_refresh_range():
    with captured_output() as (_, err):
        with pytest.raises(SystemExit):
            parser = create_parser()
            args = parser.parse_args(
                [
                    "-b",
                    "localhost",
                    "-p",
                    "8080",
                    "watch",
                    "-m",
                    "complete",
                    "-r",
                    "90",
                ]
            )
        assert "refresh must be between 1 and 60 inclusive, found 90" in err.getvalue()
