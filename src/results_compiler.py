from typing import List
from src.result_lines import FullResultLine, SummaryResultLine

from src.server_data import ServerData
from src.services_statistics import SerivesStatistics


class ResultsCompiler:
    """Compiles and augment information about a list of servers."""

    @staticmethod
    def full(servers: List[ServerData], mode: str) -> List[FullResultLine]:
        """Creates a report per server augmenting with some information about the hosted service."""
        services_summaries = {
            summary.service: summary
            for summary in ResultsCompiler.summary(servers, mode)
        }
        return [
            FullResultLine(
                server.service,
                server.ip,
                server.memory,
                server.cpu,
                mode,
                services_summaries[server.service],
            )
            for server in servers
        ]

    @staticmethod
    def summary(servers: List[ServerData], mode: str) -> List[SummaryResultLine]:
        """Creates a summary of each service given information about all servers."""
        assert mode in ("simple", "complete")

        services_statistics = SerivesStatistics(servers)

        results = []
        for service in services_statistics.services:
            results.append(
                SummaryResultLine(
                    service=service,
                    total_servers=len(services_statistics.ips[service]),
                    ips=services_statistics.ips[service],
                    ip_cpu_min=services_statistics.ip_cpu_min[service],
                    ip_cpu_max=services_statistics.ip_cpu_max[service],
                    ip_memory_min=services_statistics.ip_memory_min[service],
                    ip_memory_max=services_statistics.ip_memory_max[service],
                    cpu_min=services_statistics.cpu_quantiles[service][0],
                    cpu_p25=services_statistics.cpu_quantiles[service][1],
                    cpu_p50=services_statistics.cpu_quantiles[service][2],
                    cpu_p75=services_statistics.cpu_quantiles[service][3],
                    cpu_max=services_statistics.cpu_quantiles[service][4],
                    memory_min=services_statistics.memory_quantiles[service][0],
                    memory_p25=services_statistics.memory_quantiles[service][1],
                    memory_p50=services_statistics.memory_quantiles[service][2],
                    memory_p75=services_statistics.memory_quantiles[service][3],
                    memory_max=services_statistics.memory_quantiles[service][4],
                    mode=mode,
                )
            )
        return results
