import pytest

from json import dumps

from src.server_data import ServerData
from src.services_statistics import get_quantiles, SerivesStatistics


@pytest.mark.parametrize(
    "numbers,expected",
    [
        ([], [0.0, 0.0, 0.0, 0.0, 0.0]),
        ([1, 2], [1.0, 0.0, 0.0, 0.0, 2.0]),
        ([1, 2, 3, 4, 5], [1.0, 1.5, 3.0, 4.5, 5.0]),
    ],
)
def test_get_quantiles(numbers, expected):
    actual = get_quantiles(numbers)
    assert len(actual) == len(expected)
    for actual_value, expected_value in zip(actual, expected):
        assert actual_value == pytest.approx(expected_value)


def test_services_statistics():
    servers = [
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
    ]

    expected_memory_counts = {"something": [11, 12, 13, 14, 15]}
    expected_cpu_counts = {"something": [1, 2, 3, 4, 5]}
    expected_ips = {
        "something": [
            "192.168.1.101",
            "192.168.1.102",
            "192.168.1.103",
            "192.168.1.104",
            "192.168.1.105",
        ]
    }
    expected_ip_cpu_min = {"something": "192.168.1.101"}
    expected_ip_cpu_max = {"something": "192.168.1.105"}
    expected_ip_memory_min = {"something": "192.168.1.101"}
    expected_ip_memory_max = {"something": "192.168.1.105"}
    expected_memory_quantiles = {"something": [11.0, 11.5, 13.0, 14.5, 15.0]}
    expected_cpu_quantiles = {"something": [1.0, 1.5, 3.0, 4.5, 5.0]}
    expected_services = {
        "something",
    }

    ss = SerivesStatistics(servers)

    def compare_dicts(dict1, dict2) -> bool:
        return dumps(dict1, sort_keys=True) == dumps(dict2, sort_keys=True)

    assert ss.services == expected_services
    assert compare_dicts(dict(ss.memory_counts), expected_memory_counts)
    assert compare_dicts(dict(ss.cpu_counts), expected_cpu_counts)
    assert compare_dicts(dict(ss.ips), expected_ips)
    assert compare_dicts(dict(ss.ip_cpu_min), expected_ip_cpu_min)
    assert compare_dicts(dict(ss.ip_cpu_max), expected_ip_cpu_max)
    assert compare_dicts(dict(ss.ip_memory_min), expected_ip_memory_min)
    assert compare_dicts(dict(ss.ip_memory_max), expected_ip_memory_max)
    assert compare_dicts(dict(ss.memory_quantiles), expected_memory_quantiles)
    assert compare_dicts(dict(ss.cpu_quantiles), expected_cpu_quantiles)
