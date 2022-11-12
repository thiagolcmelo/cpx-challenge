from dataclasses import dataclass
from json import dumps
from typing import Dict


@dataclass
class ServerData:
    ip: str
    details: Dict[str, str]

    def __str__(self) -> str:
        return f"[{self.ip}] {dumps(self.details)}"

    @property
    def memory(self) -> int:
        return int((self.details.get("memory", "") or "-1").replace("%", ""))

    @property
    def cpu(self) -> int:
        return int((self.details.get("cpu", "") or "-1").replace("%", ""))

    @property
    def service(self) -> str:
        return self.details.get("service", "unknown")
