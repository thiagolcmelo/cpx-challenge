#!/usr/bin/env python3
"""
The ServerData provides basic functionality for holding and parsing server
data fetched from CPX.
"""

from dataclasses import dataclass
from json import dumps
from typing import Dict


@dataclass
class ServerData:
    """Represents the information related to a single server."""

    ip_address: str
    details: Dict[str, str]

    def __str__(self) -> str:
        """A useful string representation of this server."""
        return f"[{self.ip_address}] {dumps(self.details)}"

    @property
    def memory(self) -> int:
        """The pct of memory used in this server."""
        return int((self.details.get("memory", "") or "-1").replace("%", ""))

    @property
    def cpu(self) -> int:
        """The pct of user used in this server."""
        return int((self.details.get("cpu", "") or "-1").replace("%", ""))

    @property
    def service(self) -> str:
        """The name of the server hosted this server."""
        return self.details.get("service", "unknown") or "unknown"
