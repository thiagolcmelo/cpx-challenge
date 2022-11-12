import pytest

from unittest.mock import AsyncMock, patch
from src.cpx_client import CpxClientCannotConnect

from src.fetcher import Fetcher
from src.server_data import ServerData
from tests.utils import captured_output, servers


@pytest.fixture
def cpx_client_mock():
    cpx_client = AsyncMock()
    cpx_client.fetch_details = AsyncMock(
        return_value={
            "cpu": "7%",
            "memory": "10%",
            "service": "some",
        }
    )
    cpx_client.fetch_servers = AsyncMock(return_value=["192.168.1.100"])
    return cpx_client


@pytest.fixture
def cpx_client_fail_once_mock():
    cpx_client = AsyncMock()
    cpx_client.failed = 0

    def fetch_details(_):
        if cpx_client.failed == 0:
            cpx_client.failed = 1
            raise CpxClientCannotConnect()
        return {
            "cpu": "7%",
            "memory": "10%",
            "service": "some",
        }

    cpx_client.fetch_details = AsyncMock(side_effect=fetch_details)
    cpx_client.fetch_servers = AsyncMock(return_value=["192.168.1.100"])
    return cpx_client


@pytest.fixture
def cpx_client_fail_always():
    cpx_client = AsyncMock()

    def fetch_details(_):
        raise CpxClientCannotConnect()

    cpx_client.fetch_details = AsyncMock(side_effect=fetch_details)
    cpx_client.fetch_servers = AsyncMock(return_value=["192.168.1.100"])
    return cpx_client


@pytest.fixture
def cpx_client_empty_mock():
    cpx_client = AsyncMock()
    cpx_client.fetch_servers = AsyncMock(return_value=[])
    return cpx_client


@pytest.mark.asyncio
async def test_fetch_details(cpx_client_mock):
    response = await Fetcher.fetch_details(cpx_client_mock, "192.168.1.100")
    assert response.cpu == 7
    assert response.memory == 10
    assert response.service == "some"


@pytest.mark.asyncio
@patch("src.fetcher.asyncio")
async def test_fetch_details_retry(asyncio_mock, cpx_client_fail_once_mock):
    asyncio_mock.sleep = AsyncMock()
    response = await Fetcher.fetch_details(cpx_client_fail_once_mock, "192.168.1.100")
    assert response.cpu == 7
    assert response.memory == 10
    assert response.service == "some"


@pytest.mark.asyncio
@patch("src.fetcher.CpxClient")
async def test_fetch_all(client, cpx_client_mock):
    client.return_value = cpx_client_mock

    fetcher = Fetcher("192.168.1.100", 8080, 4)
    servers = await fetcher.fetch_all()

    assert len(servers) == 1
    server = servers[0]
    assert server.cpu == 7
    assert server.memory == 10
    assert server.service == "some"


@pytest.mark.asyncio
@patch("src.fetcher.CpxClient")
@patch("src.fetcher.asyncio.sleep")
async def test_fetch_all_fail(asyncio_sleep_mock, client, cpx_client_fail_always):
    asyncio_sleep_mock = AsyncMock()
    client.return_value = cpx_client_fail_always

    fetcher = Fetcher("192.168.1.100", 8080, 4)
    servers = await fetcher.fetch_all()

    assert len(servers) == 1
    server = servers[0]
    assert server.cpu is -1
    assert server.memory is -1
    assert server.service is "unknown"


@pytest.mark.asyncio
@patch("src.fetcher.CpxClient")
async def test_fetch_all_empty(client, cpx_client_empty_mock):
    client.return_value = cpx_client_empty_mock

    fetcher = Fetcher("192.168.1.100", 8080, 4)
    servers = await fetcher.fetch_all()

    assert len(servers) == 0


@pytest.mark.asyncio
@patch.object(Fetcher, "fetch_all")
async def test_display_summary(fetcher_fetch_all_mock, servers):
    fetcher_fetch_all_mock.return_value = servers
    fetcher = Fetcher("10.0.0.1", 8080, 4)
    with captured_output() as (out, _):
        await fetcher.display_once("table", "summary")
        output = out.getvalue()
        assert "something" in output
        assert "somethingElse" in output
        assert "192.168.1.105" in output
        assert "10.0.0.5" in output


@pytest.mark.asyncio
@patch.object(Fetcher, "fetch_all")
async def test_display_full(fetcher_fetch_all_mock, servers):
    fetcher_fetch_all_mock.return_value = servers
    fetcher = Fetcher("10.0.0.1", 8080, 4)
    with captured_output() as (out, _):
        await fetcher.display_once("table", "full")
        output = out.getvalue()
        assert "something" in output
        assert "somethingElse" in output
        assert "10.0.0.1" in output
        assert "10.0.0.2" in output
        assert "10.0.0.3" in output
        assert "10.0.0.4" in output
        assert "10.0.0.5" in output
        assert "192.168.1.101" in output
        assert "192.168.1.102" in output
        assert "192.168.1.103" in output
        assert "192.168.1.104" in output
        assert "192.168.1.105" in output
