#!/usr/bin/env python3
"""
This module contains a basic client for fetching CPX data using the provided
HTTP endpoints.
"""

import logging
import sys
from json import loads
from typing import Dict, List
from urllib.parse import urljoin
import aiohttp
from aiohttp import ClientSession


# this logger is useful only for debugging purposes, improvement is necessary
# to have an useful log structure
logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    level=logging.FATAL,
    datefmt="%Y-%m-%d %H:%M",
    stream=sys.stderr,
)
logger = logging.getLogger("cpx-client")
logging.getLogger("chardet.charsetprober").disabled = True


class CpxClientCannotConnect(Exception):
    """Used to inform that CPX server is unreachable."""


class CpxClientBadRequest(Exception):
    """Used to inform an error in the request."""


async def fetch_servers(url: str, session: ClientSession) -> List[str]:
    """Returns a list of servers ips from CPX."""
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
    return response


async def fetch_details(url: str, session: ClientSession) -> Dict[str, str]:
    """Returns details of a server from CPX."""
    try:
        resp = await session.get(url)
        resp.raise_for_status()
        logger.info("Got response [%s] for URL: %s", resp.status, url)
        response_text = await resp.text()
        return loads(response_text)
    except aiohttp.client_exceptions.ClientConnectorError as error:
        message = "Could not connect to URL: %s, error: %s", url, str(error)
        logger.error(message)
        raise CpxClientCannotConnect(message) from error
    except aiohttp.client_exceptions.ClientResponseError as error:
        message = (
            "Got response [%s] for URL: %s, error: %s",
            resp.status,
            url,
            str(error),
        )
        logger.error(message)
        raise CpxClientBadRequest(message) from error


class CpxClient:
    """Provides an interface for asynchronously fetching servers and details."""

    def __init__(self, host: str, port: int, ip_version: int = 4) -> None:
        assert ip_version in (4, 6), f"invalid ip version: {ip_version}"
        self.host = host
        self.port = port
        self.ip_version = ip_version

    @property
    def base_url(self) -> str:
        """Facilitates the base URL generation."""
        if self.ip_version == 4:
            return f"http://{self.host}:{self.port}"
        return f"http://[{self.host}]:{self.port}"

    def get_url(self, path: str) -> str:
        """Builds a full URL."""
        return urljoin(self.base_url, path)

    async def fetch_servers(self) -> List[str]:
        """Asynchronously fetches servers from CPX."""
        async with ClientSession() as session:
            return await fetch_servers(self.get_url("servers"), session)

    async def fetch_details(self, server: str) -> Dict[str, str]:
        """Asynchronously fetches details of a server from CPX."""
        async with ClientSession() as session:
            return await fetch_details(self.get_url(server), session)
