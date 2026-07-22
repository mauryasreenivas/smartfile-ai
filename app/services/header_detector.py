from __future__ import annotations

from collections.abc import Iterable, Sequence
from dataclasses import dataclass


COMMON_HEADER_WORDS = {
    "account",
    "aging",
    "amount",
    "balance",
    "currency",
    "cust",
    "customer",
    "customer id",
    "date",
    "doc",
    "document",
    "due",
    "invoice",
    "invoice no",
    "ledger",
    "name",
    "ref",
    "reference",
    "terms",
}


@dataclass(slots=True)
class HeaderDetectionResult:
    row_index: int
    score: int
    header: list[str]


class HeaderDetector:
    """Detect the most likely header row from a collection of rows."""

    def detect(
        self,
        rows: Iterable[Sequence[object]],
    ) -> HeaderDetectionResult:
        candidate_rows = list(rows)

        if not candidate_rows:
            raise ValueError("No rows supplied")

        best_index = 0
        best_score = float("-inf")

        for row_index, row in enumerate(candidate_rows):
            score = self._score_row(row)

            if score > best_score:
                best_index = row_index
                best_score = score

        header = [
            str(value).strip() if value is not None else ""
            for value in candidate_rows[best_index]
        ]

        return HeaderDetectionResult(
            row_index=best_index,
            score=int(best_score),
            header=header,
        )

    def _score_row(self, row: Sequence[object]) -> int:
        values = [
            str(value).strip()
            for value in row
            if value is not None and str(value).strip()
        ]

        populated_cells = len(values)

        if populated_cells == 0:
            return -100

        score = 0

        # Rows with several populated cells are more likely to be headers.
        score += populated_cells * 2

        # Header values are generally unique.
        score += len(set(values))

        # A single populated cell is often a title or report name.
        if populated_cells == 1:
            score -= 8

        # Reward common financial and reporting column words.
        for value in values:
            lowered_value = value.lower()

            for keyword in COMMON_HEADER_WORDS:
                if keyword in lowered_value:
                    score += 5

        # Long text is more likely to be report metadata than a column name.
        long_cell_count = sum(len(value) > 40 for value in values)
        score -= long_cell_count * 5

        return score