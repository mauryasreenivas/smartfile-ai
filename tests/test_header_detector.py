import pytest

from app.services.header_detector import HeaderDetector


def test_detects_header_after_title_and_blank_rows() -> None:
    rows: list[list[object]] = [
        ["ABC Corporation"],
        [],
        ["Accounts Receivable Aging Report"],
        ["Customer ID", "Customer Name", "Invoice", "Amount"],
        ["1001", "John Doe", "INV001", 1200],
    ]

    result = HeaderDetector().detect(rows)

    assert result.row_index == 3
    assert result.header == [
        "Customer ID",
        "Customer Name",
        "Invoice",
        "Amount",
    ]
    assert result.score > 0


def test_detects_header_when_blank_rows_come_first() -> None:
    rows: list[list[object]] = [
        [],
        [],
        ["Customer", "Invoice", "Balance"],
        ["1001", "INV001", 500],
    ]

    result = HeaderDetector().detect(rows)

    assert result.row_index == 2
    assert result.header == ["Customer", "Invoice", "Balance"]


def test_single_title_row_is_not_selected_as_header() -> None:
    rows: list[list[object]] = [
        ["Accounts Receivable Aging Report"],
        ["Customer", "Invoice", "Balance"],
    ]

    result = HeaderDetector().detect(rows)

    assert result.row_index == 1


def test_returns_first_row_when_it_is_the_best_header() -> None:
    rows: list[list[object]] = [
        ["Customer ID", "Invoice", "Amount"],
        ["1001", "INV001", 200],
    ]

    result = HeaderDetector().detect(rows)

    assert result.row_index == 0


def test_normalizes_none_values_in_header() -> None:
    rows: list[list[object]] = [
        ["Customer ID", None, "Amount"],
        ["1001", "John Doe", 100],
    ]

    result = HeaderDetector().detect(rows)

    assert result.header == ["Customer ID", "", "Amount"]


def test_rejects_empty_input() -> None:
    detector = HeaderDetector()

    rows: list[list[object]] = []

    with pytest.raises(ValueError, match="No rows supplied"):
        detector.detect(rows)