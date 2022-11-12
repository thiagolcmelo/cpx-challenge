#!/usr/bin/env python3

import asyncio
from dataclasses import dataclass
import logging
import sys
from json import dumps, loads
from typing import Any, Dict, List
from urllib.parse import urljoin
import aiohttp
from aiohttp import ClientSession


logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    level=logging.FATAL,
    datefmt="%Y-%m-%d %H:%M",
    stream=sys.stderr,
)
logger = logging.getLogger("cpx-client")
logging.getLogger("chardet.charsetprober").disabled = True


class CpxClientCannotConnect(Exception):
    pass


class CpxClientBadRequest(Exception):
    pass


async def fetch_servers(url: str, session: ClientSession) -> List[str]:
    response = []
    try:
        resp = await session.get(url)
        resp.raise_for_status()
        logger.info("Got response [%s] for URL: %s", resp.status, url)
        response_text = await resp.text()
        response = loads(response_text)
    except aiohttp.client_exceptions.ClientConnectorError as error:
        logger.error("Could not connect to URL: %s, error: %s", url, str(error))
    except aiohttp.client_exceptions.ClientResponseError as error:
        logger.info(
            "Got response [%s] for URL: %s, error: %s", resp.status, url, str(error)
        )
    finally:
        return response


async def fetch_details(url: str, session: ClientSession) -> Dict[str, str]:
    try:
        resp = await session.get(url)
        resp.raise_for_status()
        logger.info("Got response [%s] for URL: %s", resp.status, url)
        response_text = await resp.text()
        return loads(response_text)
    except aiohttp.client_exceptions.ClientConnectorError as error:
        message = "Could not connect to URL: %s, error: %s", url, str(error)
        logger.error(message)
        raise CpxClientCannotConnect(message)
    except aiohttp.client_exceptions.ClientResponseError as error:
        message = (
            "Got response [%s] for URL: %s, error: %s",
            resp.status,
            url,
            str(error),
        )
        logger.error(message)
        raise CpxClientBadRequest(message)


class CpxClient:
    """Provides an interface for asynchronously fetching servers and details."""

    def __init__(self, host: str, port: int, ip_version: int = 4) -> None:
        assert ip_version in (4, 6), f"invalid ip version: {ip_version}"
        self.host = host
        self.port = port
        self.ip_version = ip_version

    @property
    def base_url(self) -> str:
        if self.ip_version == 4:
            return f"http://{self.host}:{self.port}"
        return f"http://[{self.host}]:{self.port}"

    def get_url(self, path: str) -> str:
        return urljoin(self.base_url, path)

    async def fetch_servers(self) -> List[str]:
        async with ClientSession() as session:
            return await fetch_servers(self.get_url("servers"), session)

    async def fetch_details(self, server: str) -> Dict[str, str]:
        async with ClientSession() as session:
            return await fetch_details(self.get_url(server), session)


async def dummy():
    client = CpxClient("localhost", 8080)
    servers = await client.fetch_servers()
    if len(servers) > 0:
        details = await client.fetch_details(servers[0])
        print(details)


if __name__ == "__main__":
    asyncio.run(dummy())
