import pytest

from src.result_lines import FullResultLine, SummaryResultLine


@pytest.fixture
def summary_result_lines():
    return [
        SummaryResultLine(
            service="something",
            total_servers=1,
            ips=["10.0.0.1"],
            ip_cpu_min="10.0.0.1",
            ip_cpu_max="10.0.0.1",
            ip_memory_min="10.0.0.1",
            ip_memory_max="10.0.0.1",
            cpu_min=10,
            cpu_p25=0,
            cpu_p50=0,
            cpu_p75=0,
            cpu_max=10,
            memory_min=25,
            memory_p25=0,
            memory_p50=0,
            memory_p75=0,
            memory_max=25,
            mode="simple",
        ),
        SummaryResultLine(
            service="something",
            total_servers=2,
            ips=["10.0.0.1", "10.0.0.2"],
            ip_cpu_min="10.0.0.1",
            ip_cpu_max="10.0.0.2",
            ip_memory_min="10.0.0.1",
            ip_memory_max="10.0.0.2",
            cpu_min=10,
            cpu_p25=0,
            cpu_p50=0,
            cpu_p75=0,
            cpu_max=100,
            memory_min=25,
            memory_p25=0,
            memory_p50=0,
            memory_p75=0,
            memory_max=50,
            mode="complete",
        ),
    ]


@pytest.fixture
def full_result_lines():
    return [
        FullResultLine(
            "something",
            "10.0.0.1",
            25,
            10,
            "simple",
            SummaryResultLine(
                service="something",
                total_servers=1,
                ips=["10.0.0.1"],
                ip_cpu_min="10.0.0.1",
                ip_cpu_max="10.0.0.1",
                ip_memory_min="10.0.0.1",
                ip_memory_max="10.0.0.1",
                cpu_min=10,
                cpu_p25=0,
                cpu_p50=0,
                cpu_p75=0,
                cpu_max=10,
                memory_min=25,
                memory_p25=0,
                memory_p50=0,
                memory_p75=0,
                memory_max=25,
                mode="simple",
            ),
        ),
        FullResultLine(
            "something",
            "10.0.0.1",
            25,
            10,
            "complete",
            SummaryResultLine(
                service="something",
                total_servers=2,
                ips=["10.0.0.1", "10.0.0.2"],
                ip_cpu_min="10.0.0.1",
                ip_cpu_max="10.0.0.2",
                ip_memory_min="10.0.0.1",
                ip_memory_max="10.0.0.2",
                cpu_min=10,
                cpu_p25=0,
                cpu_p50=0,
                cpu_p75=0,
                cpu_max=100,
                memory_min=25,
                memory_p25=0,
                memory_p50=0,
                memory_p75=0,
                memory_max=50,
                mode="complete",
            ),
        ),
        FullResultLine(
            "something",
            "10.0.0.2",
            50,
            100,
            "complete",
            SummaryResultLine(
                service="something",
                total_servers=2,
                ips=["10.0.0.1", "10.0.0.2"],
                ip_cpu_min="10.0.0.1",
                ip_cpu_max="10.0.0.2",
                ip_memory_min="10.0.0.1",
                ip_memory_max="10.0.0.2",
                cpu_min=10,
                cpu_p25=0,
                cpu_p50=0,
                cpu_p75=0,
                cpu_max=100,
                memory_min=25,
                memory_p25=0,
                memory_p50=0,
                memory_p75=0,
                memory_max=50,
                mode="complete",
            ),
        ),
    ]


def test_summary_service_health(summary_result_lines):
    assert summary_result_lines[0].status == "Unhealthy"
    assert summary_result_lines[1].status == "Healthy"


def test_full_service_health(full_result_lines):
    assert full_result_lines[0].status == "Unhealthy"
    assert full_result_lines[1].status == "Healthy"


def test_summary_columns(summary_result_lines):
    srl1 = summary_result_lines[0]
    srl2 = summary_result_lines[1]
    assert len(srl1.columns) < len(srl2.columns)


def test_summary_csv_header_line(summary_result_lines):
    srl1 = summary_result_lines[0]
    srl2 = summary_result_lines[1]
    srl1_columns = srl1.columns
    srl1_header = srl1.csv_header_line
    srl2_columns = srl2.columns
    srl2_header = srl2.csv_header_line

    for col in srl1_columns:
        assert col in srl1_header

    for col in srl2_columns:
        assert col in srl2_header


def test_full_csv_header_line(full_result_lines):
    frl1 = full_result_lines[0]
    frl2 = full_result_lines[1]
    frl1_columns = frl1.columns
    frl1_header = frl1.csv_header_line
    frl2_columns = frl2.columns
    frl2_header = frl2.csv_header_line

    for col in frl1_columns:
        assert col in frl1_header

    for col in frl2_columns:
        assert col in frl2_header
