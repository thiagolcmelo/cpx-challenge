#!/usr/bin/env python3
"""
The SerivesStatistics class is intended to compute statistics around the usage
of resource by CPX servers and services.
"""
from collections import defaultdict
from statistics import quantiles
from typing import List

from src.server_data import ServerData


def get_quantiles(numbers: List[int]) -> List[float]:
    """Returns [min, q1, q2, q3, max] for a list of numbers."""
    min_val = 0
    max_val = 0
    quantiles_values = [0.0, 0.0, 0.0]
    if len(numbers) >= 4:
        min_val = float(min(numbers))
        max_val = float(max(numbers))
        quantiles_values = quantiles(numbers, n=4)
    elif len(numbers) > 0:
        min_val = float(min(numbers))
        max_val = float(max(numbers))
    return [min_val] + quantiles_values + [max_val]


class SerivesStatistics:
    """Generates statistics about services given a list of servers."""

    def __init__(self, servers: List[ServerData]) -> None:
        self.memory_counts = defaultdict(list)
        self.cpu_counts = defaultdict(list)
        self.ips = defaultdict(list)
        self.ip_cpu_min = defaultdict(str)
        self.ip_cpu_max = defaultdict(str)
        self.ip_memory_min = defaultdict(str)
        self.ip_memory_max = defaultdict(str)
        self.memory_quantiles = defaultdict(list)
        self.cpu_quantiles = defaultdict(list)
        self.services = set()

        min_cpu = defaultdict(lambda: 100)
        max_cpu = defaultdict(int)
        min_memory = defaultdict(lambda: 100)
        max_memory = defaultdict(int)

        for server in servers:
            service = server.service
            self.services.add(service)
            memory = server.memory
            cpu = server.cpu
            if memory >= 0 and cpu >= 0:
                if memory <= min_memory[service]:
                    self.ip_memory_min[service] = server.ip_address
                    min_memory[service] = memory
                if memory >= max_memory[service]:
                    self.ip_memory_max[service] = server.ip_address
                    max_memory[service] = memory
                if cpu <= min_cpu[service]:
                    self.ip_cpu_min[service] = server.ip_address
                    min_cpu[service] = cpu
                if cpu >= max_cpu[service]:
                    self.ip_cpu_max[service] = server.ip_address
                    max_cpu[service] = cpu
                self.memory_counts[service].append(memory)
                self.cpu_counts[service].append(cpu)
                self.ips[service].append(server.ip_address)

        for service in self.services:
            self.memory_quantiles[service].extend(
                get_quantiles(self.memory_counts[service])
            )
            self.cpu_quantiles[service].extend(get_quantiles(self.cpu_counts[service]))
