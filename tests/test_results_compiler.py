import pytest

from src.results_compiler import ResultsCompiler
from src.server_data import ServerData


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


def test_results_compiler_summary(servers):
    simple = ResultsCompiler.summary(servers, "simple")
    complete = ResultsCompiler.summary(servers, "complete")
    assert len(simple) == 2
    assert len(complete) == 2


def test_results_compiler_full(servers):
    simple = ResultsCompiler.full(servers, "simple")
    complete = ResultsCompiler.full(servers, "complete")
    assert len(simple) == 10
    assert len(complete) == 10
