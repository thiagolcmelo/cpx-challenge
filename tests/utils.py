import io, sys
from contextlib import contextmanager

import pytest

from src.server_data import ServerData


@contextmanager
def captured_output():
    new_out, new_err = io.StringIO(), io.StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err


@pytest.fixture
def servers():
    return [
        ServerData(
            "192.168.1.101",
            {"cpu": "1%", "memory": "11%", "service": "something"},
        ),
        ServerData(
            "192.168.1.102",
            {"cpu": "2%", "memory": "12%", "service": "something"},
        ),
        ServerData(
            "192.168.1.103",
            {"cpu": "3%", "memory": "13%", "service": "something"},
        ),
        ServerData(
            "192.168.1.104",
            {"cpu": "4%", "memory": "14%", "service": "something"},
        ),
        ServerData(
            "192.168.1.105",
            {"cpu": "5%", "memory": "15%", "service": "something"},
        ),
        ServerData(
            "10.0.0.1",
            {"cpu": "1%", "memory": "11%", "service": "somethingElse"},
        ),
        ServerData(
            "10.0.0.2",
            {"cpu": "2%", "memory": "12%", "service": "somethingElse"},
        ),
        ServerData(
            "10.0.0.3",
            {"cpu": "3%", "memory": "13%", "service": "somethingElse"},
        ),
        ServerData(
            "10.0.0.4",
            {"cpu": "4%", "memory": "14%", "service": "somethingElse"},
        ),
        ServerData(
            "10.0.0.5",
            {"cpu": "5%", "memory": "15%", "service": "somethingElse"},
        ),
    ]
