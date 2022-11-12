import asyncio
from dataclasses import dataclass
from json import dumps
from typing import Dict, List

from src.cpx_client import CpxClient, CpxClientCannotConnect
from src.printer import Printer
from src.results_compiler import ResultsCompiler
from src.server_data import ServerData


class Fetcher:
    """Fetches and compiles servers and services from CPX API"""

    def __init__(self, host: str, port: int, ip_version: int) -> None:
        self.host = host
        self.port = port
        self.ip_version = ip_version

    async def fetch_all(self) -> List[ServerData]:
        """Fetches a list of servers ips and corresponding details of each one from CPX."""
        client = CpxClient(self.host, self.port, self.ip_version)
        server_ips = await client.fetch_servers()
        if len(server_ips) > 0:
            tasks = [self.fetch_details(client, ip) for ip in server_ips]
            return await asyncio.gather(*tasks)
        return []

    @staticmethod
    async def fetch_details(
        client: CpxClient, ip: str, retry: int = 5, delay: int = 1, backoff: int = 2
    ) -> ServerData:
        """Fetches details of a single server from CPX with retry and backoff mechanism."""
        while retry > 0:
            try:
                details = await client.fetch_details(ip)
                return ServerData(ip, details)
            except CpxClientCannotConnect:
                retry -= 1
                delay *= backoff
                await asyncio.sleep(delay)
        return ServerData(
            ip,
            {
                "cpu": None,
                "memory": None,
                "service": None,
            },
        )

    async def display_once(
        self, format: str, details: str, mode: str = "complete", window=None
    ) -> None:
        """Prints all information fetchable from CPX to stdout."""
        assert format in ("csv", "json", "table")
        assert details in ("summary", "full")

        results = await self.fetch_all()
        if details == "summary":
            compiled_results = ResultsCompiler.summary(results, mode)
            Printer.print_summary(compiled_results, format, window)
        else:
            compiled_results = ResultsCompiler.full(results, mode)
            Printer.print_full(compiled_results, format)
