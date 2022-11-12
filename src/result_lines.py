import csv
from dataclasses import asdict, dataclass
from io import StringIO
from json import dumps
from typing import Dict, List, Tuple


@dataclass
class SummaryResultLine:
    """Represents a line in a summary report."""

    service: str
    total_servers: int
    ips: List[str]
    ip_cpu_min: str
    ip_cpu_max: str
    ip_memory_min: str
    ip_memory_max: str
    cpu_min: int
    cpu_p25: int
    cpu_p50: int
    cpu_p75: int
    cpu_max: int
    memory_min: int
    memory_p25: int
    memory_p50: int
    memory_p75: int
    memory_max: int
    mode: str

    @property
    def status(self) -> str:
        """The status of the service."""
        if self.total_servers > 1:
            return "Healthy"
        return "Unhealthy"

    @property
    def columns(self) -> List[str]:
        """The columns to be displayed depending on mode (simple or complete)."""
        if self.mode == "simple":
            return [
                "service",
                "status",
                "total_servers",
                "ip_cpu_max",
                "ip_memory_max",
                "cpu_min",
                "cpu_max",
                "memory_min",
                "memory_max",
            ]
        return [
            "service",
            "status",
            "total_servers",
            "ips",
            "ip_cpu_min",
            "ip_cpu_max",
            "ip_memory_min",
            "ip_memory_max",
            "cpu_min",
            "cpu_p25",
            "cpu_p50",
            "cpu_p75",
            "cpu_max",
            "memory_min",
            "memory_p25",
            "memory_p50",
            "memory_p75",
            "memory_max",
        ]

    @property
    def csv_header_line(self) -> str:
        """The csv header dependng on the available columns."""
        return ",".join(self.columns)

    @property
    def csv_line(self) -> str:
        """The csv line dependng on the available columns."""
        values = {**asdict(self), "status": self.status}
        output = StringIO()
        spamwriter = csv.writer(
            output, delimiter=",", quotechar='"', quoting=csv.QUOTE_ALL
        )
        spamwriter.writerow([str(values[c]) for c in self.columns])
        return output.getvalue().replace("\n", "")

    @property
    def json_line(self) -> str:
        """The json dump of the line depending on available columns."""
        values = {**asdict(self), "status": self.status}
        return dumps({c: str(values[c]) for c in self.columns})

    @staticmethod
    def columns_formats(max_service_name_len: int) -> Dict[str, Tuple[str, int]]:
        """Sets length and formating for values displayed in each column."""
        return {
            # column: (title, length, value formatter)
            "service": ("Service", max(8, max_service_name_len + 1), lambda v: str(v)),
            "status": ("Status", 10, lambda v: str(v)),
            "total_servers": ("Servers (#)", 12, lambda v: str(v)),
            "ip_cpu_min": ("IP:min(cpu)", 16, lambda v: str(v)),
            "ip_cpu_max": ("IP:max(cpu)", 16, lambda v: str(v)),
            "ip_memory_min": ("IP:min(memory)", 16, lambda v: str(v)),
            "ip_memory_max": ("IP:max(memory)", 16, lambda v: str(v)),
            "cpu_min": ("CPU min", 8, lambda v: str(int(v)) + "%"),
            "cpu_p25": ("CPU Q1", 7, lambda v: str(int(v)) + "%"),
            "cpu_p50": ("CPU Q2", 7, lambda v: str(int(v)) + "%"),
            "cpu_p75": ("CPU Q3", 7, lambda v: str(int(v)) + "%"),
            "cpu_max": ("CPU max", 8, lambda v: str(int(v)) + "%"),
            "memory_min": ("Mem min", 8, lambda v: str(int(v)) + "%"),
            "memory_p25": ("Mem Q1", 7, lambda v: str(int(v)) + "%"),
            "memory_p50": ("Mem Q2", 7, lambda v: str(int(v)) + "%"),
            "memory_p75": ("Mem Q3", 7, lambda v: str(int(v)) + "%"),
            "memory_max": ("Mem max", 8, lambda v: str(int(v)) + "%"),
        }

    def table_header_line(self, max_service_name_len: int) -> str:
        """The formatted table header depending on available columns."""
        columns = [c for c in self.columns if c != "ips"]
        formats = self.columns_formats(max_service_name_len)
        header_line = ""
        for c in columns:
            header_line += formats[c][0].ljust(formats[c][1])
        return header_line

    def table_line(self, max_service_name_len: int) -> str:
        """The formatted table line depending on available columns."""
        values = {**asdict(self), "status": self.status}
        columns = [c for c in self.columns if c != "ips"]
        formats = self.columns_formats(max_service_name_len)
        line = ""
        for c in columns:
            line += formats[c][2](values[c]).ljust(formats[c][1])
        return line


@dataclass
class FullResultLine:
    """Represents a line in a full report."""

    service: str
    ip: str
    memory: int
    cpu: int
    mode: str
    service_summary: SummaryResultLine

    @property
    def status(self) -> str:
        """The status of the service hosted in this server."""
        if self.service_summary.total_servers > 1:
            return "Healthy"
        return "Unhealthy"

    @property
    def columns(self) -> List[str]:
        """The columns to be displayed depending on mode (simple or complete)."""
        if self.mode == "simple":
            return [
                "ip",
                "service",
                "memory",
                "cpu",
            ]
        return [
            "ip",
            "service",
            "memory",
            "cpu",
            "status",
            "total_servers",
            "ip_cpu_min",
            "ip_cpu_max",
            "ip_memory_min",
            "ip_memory_max",
            "cpu_min",
            "cpu_max",
            "memory_min",
            "memory_max",
        ]

    @property
    def csv_header_line(self) -> str:
        """The csv header dependng on the available columns."""
        return ",".join(self.columns)

    @property
    def csv_line(self) -> str:
        """The csv line dependng on the available columns."""
        values = {**asdict(self), "status": self.status}
        values.update(**asdict(self.service_summary))
        output = StringIO()
        spamwriter = csv.writer(
            output, delimiter=",", quotechar='"', quoting=csv.QUOTE_ALL
        )
        spamwriter.writerow([str(values[c]) for c in self.columns])
        return output.getvalue().replace("\n", "")

    @property
    def json_line(self) -> str:
        """The json dump of the line depending on available columns."""
        values = {**asdict(self), "status": self.status}
        values.update(**asdict(self.service_summary))
        return dumps({c: str(values[c]) for c in self.columns})

    @staticmethod
    def columns_formats(max_service_name_len: int) -> Dict[str, Tuple[str, int]]:
        """Sets length and formating for values displayed in each column."""
        return {
            # column: (title, length, value formatter)
            "ip": ("IP", 16, lambda v: str(v)),
            "service": ("Service", max(8, max_service_name_len + 1), lambda v: str(v)),
            "memory": ("Mem", 7, lambda v: str(int(v)) + "%"),
            "cpu": ("CPU", 7, lambda v: str(int(v)) + "%"),
            "status": ("Status", 10, lambda v: str(v)),
            "total_servers": ("Servers (#)", 12, lambda v: str(v)),
            "ip_cpu_min": ("IP:min(cpu)", 16, lambda v: str(v)),
            "ip_cpu_max": ("IP:max(cpu)", 16, lambda v: str(v)),
            "ip_memory_min": ("IP:min(memory)", 16, lambda v: str(v)),
            "ip_memory_max": ("IP:max(memory)", 16, lambda v: str(v)),
            "cpu_min": ("CPU min", 8, lambda v: str(int(v)) + "%"),
            "cpu_max": ("CPU max", 8, lambda v: str(int(v)) + "%"),
            "memory_min": ("Mem max", 8, lambda v: str(int(v)) + "%"),
            "memory_max": ("Mem min", 8, lambda v: str(int(v)) + "%"),
        }

    def table_header_line(self, max_service_name_len: int) -> str:
        """The formatted table header depending on available columns."""
        formats = self.columns_formats(max_service_name_len)
        header_line = ""
        for c in self.columns:
            header_line += formats[c][0].ljust(formats[c][1])
        return header_line

    def table_line(self, max_service_name_len: int) -> str:
        """The formatted table line depending on available columns."""
        values = {**asdict(self), "status": self.status}
        values.update(**asdict(self.service_summary))
        formats = self.columns_formats(max_service_name_len)
        line = ""
        for c in self.columns:
            line += formats[c][2](values[c]).ljust(formats[c][1])
        return line
