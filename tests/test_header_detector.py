from app.services.header_detector import HeaderDetector


def test_detect_simple_header():

    rows = [
        ["ABC Corporation"],
        [],
        ["Generated on 22 Jul"],
        [
            "Customer ID",
            "Customer Name",
            "Invoice",
            "Amount",
        ],
        [
            1001,
            "John",
            "INV001",
            120,
        ],
    ]

    detector = HeaderDetector()

    result = detector.detect(rows)

    assert result.row_index == 3


def test_blank_rows():

    rows = [
        [],
        [],
        [],
        ["Customer", "Invoice", "Balance"],
    ]

    detector = HeaderDetector()

    result = detector.detect(rows)

    assert result.row_index == 3


def test_single_title_not_header():

    rows = [
        ["Accounts Receivable Aging Report"],
        ["Customer", "Invoice", "Balance"],
    ]

    detector = HeaderDetector()

    result = detector.detect(rows)

    assert result.row_index == 1
