import pytest

from src.server_data import ServerData


@pytest.mark.parametrize(
    "ip,details,memory,cpu,service",
    [
        ("127.0.0.1", {}, -1, -1, "unknown"),
        ("127.0.0.1", {"cpu": "8%"}, -1, 8, "unknown"),
        ("127.0.0.1", {"cpu": "8%", "memory": "10%"}, 10, 8, "unknown"),
        (
            "127.0.0.1",
            {"cpu": "8%", "memory": "10%", "service": "something"},
            10,
            8,
            "something",
        ),
    ],
)
def test_server_data(ip, details, memory, cpu, service):
    s = ServerData(ip, details)
    assert s.cpu == cpu
    assert s.memory == memory
    assert s.service == service
    assert s.ip == ip
    assert ip in str(s)
