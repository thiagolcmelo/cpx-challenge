import pytest

from src.printer import Printer
from src.results_compiler import ResultsCompiler
from src.server_data import ServerData
from tests.utils import captured_output, servers


def test_print_summary(servers):
    simple_results = ResultsCompiler.summary(servers, "simple")
    complete_results = ResultsCompiler.summary(servers, "complete")

    with captured_output() as (out, _):
        Printer.print_summary(simple_results, "csv")
        output = out.getvalue()
        assert "something" in output
        assert "somethingElse" in output
        assert "192.168.1.105" in output
        assert "10.0.0.5" in output

    with captured_output() as (out, _):
        Printer.print_summary(simple_results, "json")
        output = out.getvalue()
        assert "something" in output
        assert "somethingElse" in output
        assert "192.168.1.105" in output
        assert "10.0.0.5" in output

    with captured_output() as (out, _):
        Printer.print_summary(simple_results, "table")
        output = out.getvalue()
        assert "something" in output
        assert "somethingElse" in output
        assert "192.168.1.105" in output
        assert "10.0.0.5" in output

    with captured_output() as (out, _):
        Printer.print_summary(complete_results, "csv")
        output = out.getvalue()
        assert "something" in output
        assert "somethingElse" in output
        assert "192.168.1.101" in output
        assert "192.168.1.105" in output
        assert "10.0.0.1" in output
        assert "10.0.0.5" in output

    with captured_output() as (out, _):
        Printer.print_summary(complete_results, "json")
        output = out.getvalue()
        assert "something" in output
        assert "somethingElse" in output
        assert "192.168.1.101" in output
        assert "192.168.1.105" in output
        assert "10.0.0.1" in output
        assert "10.0.0.5" in output

    with captured_output() as (out, _):
        Printer.print_summary(complete_results, "table")
        output = out.getvalue()
        assert "something" in output
        assert "somethingElse" in output
        assert "192.168.1.101" in output
        assert "192.168.1.105" in output
        assert "10.0.0.1" in output
        assert "10.0.0.5" in output


def test_print_full(servers):
    simple_results = ResultsCompiler.full(servers, "simple")

    with captured_output() as (out, _):
        Printer.print_full(simple_results, "csv")
        output = out.getvalue()
        assert "something" in output
        assert "somethingElse" in output
        assert "10.0.0.1" in output
        assert "10.0.0.2" in output
        assert "10.0.0.3" in output
        assert "10.0.0.4" in output
        assert "10.0.0.5" in output
        assert "192.168.1.101" in output
        assert "192.168.1.102" in output
        assert "192.168.1.103" in output
        assert "192.168.1.104" in output
        assert "192.168.1.105" in output

    with captured_output() as (out, _):
        Printer.print_full(simple_results, "json")
        output = out.getvalue()
        assert "something" in output
        assert "somethingElse" in output
        assert "10.0.0.1" in output
        assert "10.0.0.2" in output
        assert "10.0.0.3" in output
        assert "10.0.0.4" in output
        assert "10.0.0.5" in output
        assert "192.168.1.101" in output
        assert "192.168.1.102" in output
        assert "192.168.1.103" in output
        assert "192.168.1.104" in output
        assert "192.168.1.105" in output

    with captured_output() as (out, _):
        Printer.print_full(simple_results, "table")
        output = out.getvalue()
        assert "something" in output
        assert "somethingElse" in output
        assert "10.0.0.1" in output
        assert "10.0.0.2" in output
        assert "10.0.0.3" in output
        assert "10.0.0.4" in output
        assert "10.0.0.5" in output
        assert "192.168.1.101" in output
        assert "192.168.1.102" in output
        assert "192.168.1.103" in output
        assert "192.168.1.104" in output
        assert "192.168.1.105" in output
