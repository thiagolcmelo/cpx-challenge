from curses import A_STANDOUT
from typing import List

from src.result_lines import FullResultLine, SummaryResultLine


class Printer:
    """Provides utilities for printing summary or full results for snapshot or watch modes."""

    @staticmethod
    def print_summary(lines: List[SummaryResultLine], format: str, window=None) -> None:
        """Prints the summary in csv, json, or table formats."""
        if format == "csv":
            Printer.print_csv_summary(lines)
        elif format == "json":
            Printer.print_json_summary(lines)
        else:
            Printer.print_table_summary(lines, window)

    @staticmethod
    def print_csv_summary(lines: List[SummaryResultLine]) -> None:
        """Prints the summary in csv format."""
        print(lines[0].csv_header_line)
        for line in lines:
            print(line.csv_line)

    @staticmethod
    def print_json_summary(lines: List[SummaryResultLine]) -> None:
        """Prints the summary in json format."""
        print("[" + ",".join([line.json_line for line in lines]) + "]")

    @staticmethod
    def print_table_summary(lines: List[SummaryResultLine], window=None) -> None:
        """Prints the summary in table format."""
        max_name_len = max(map(lambda l: len(l.service), lines))
        header = lines[0].table_header_line(max_name_len)
        header_sub_line = "-" * len(header)
        text_lines = [
            line.table_line(max_name_len)
            for line in sorted(lines, key=lambda l: l.service)
        ]
        if window is None:
            print(header)
            print(header_sub_line)
            for line in text_lines:
                print(line)
        else:
            window.clear()
            window.addstr(1, 2, header)
            window.addstr(2, 2, header_sub_line)
            for idx, line in enumerate(text_lines):
                if "Unhealthy" in line:
                    window.addstr(idx + 3, 2, line, A_STANDOUT)
                else:
                    window.addstr(idx + 3, 2, line)
            window.refresh()

    @staticmethod
    def print_full(lines: List[FullResultLine], format: str) -> None:
        """Prints the full results in csv, json, or table formats."""
        if format == "csv":
            Printer.print_csv_full(lines)
        elif format == "json":
            Printer.print_json_full(lines)
        else:
            Printer.print_table_full(lines)

    @staticmethod
    def print_csv_full(lines: List[FullResultLine]) -> None:
        """Prints the full results in csv format."""
        print(lines[0].csv_header_line)
        for line in lines:
            print(line.csv_line)

    @staticmethod
    def print_json_full(lines: List[FullResultLine]) -> None:
        """Prints the full results in json format."""
        print("[" + ",".join([line.json_line for line in lines]) + "]")

    @staticmethod
    def print_table_full(lines: List[FullResultLine]) -> None:
        """Prints the full results in table format."""
        max_name_len = max(map(lambda l: len(l.service_summary.service), lines))
        print(lines[0].table_header_line(max_name_len))
        for line in sorted(lines, key=lambda l: l.service):
            print(line.table_line(max_name_len))
