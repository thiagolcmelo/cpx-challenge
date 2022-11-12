import pytest
from aiohttp import web

from json import dumps

from src.cpx_client import fetch_servers, fetch_details


async def get_servers_list(request):
    return web.Response(
        body=dumps(["10.58.1.67", "10.58.1.20", "10.58.1.95"]).encode("utf-8")
    )


async def get_server_details(request):
    return web.Response(
        body=dumps({"cpu": "33%", "memory": "14%", "service": "StorageService"}).encode(
            "utf-8"
        )
    )


@pytest.fixture
def cli(loop, aiohttp_client):
    app = web.Application()
    app.router.add_get("/servers", get_servers_list)
    app.router.add_get("/10.58.1.67", get_server_details)
    return loop.run_until_complete(aiohttp_client(app))


@pytest.mark.asyncio
async def test_fetch_servers(cli):
    servers = await fetch_servers("servers", cli)
    assert len(servers) == 3
    assert "10.58.1.67" in servers
    assert "10.58.1.20" in servers
    assert "10.58.1.95" in servers


@pytest.mark.asyncio
async def test_fetch_details(cli):
    details = await fetch_details("10.58.1.67", cli)
    assert details["cpu"] == "33%"
    assert details["memory"] == "14%"
    assert details["service"] == "StorageService"
