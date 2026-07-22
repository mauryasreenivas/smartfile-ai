from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

COMMON_HEADER_WORDS = {
    "customer",
    "customer id",
    "cust",
    "invoice",
    "invoice no",
    "doc",
    "document",
    "balance",
    "amount",
    "date",
    "due",
    "name",
    "reference",
    "ref",
    "account",
    "ledger",
    "currency",
    "terms",
    "aging",
}


@dataclass(slots=True)
class HeaderDetectionResult:
    row_index: int
    score: int
    header: list[str]


class HeaderDetector:
    """
    Detects the most probable header row.
    """

    def detect(
        self,
        rows: Iterable[list[object]],
    ) -> HeaderDetectionResult:
        rows = list(rows)

        if not rows:
            raise ValueError("No rows supplied")

        best_score = -999
        best_index = 0

        for index, row in enumerate(rows):
            score = self._score_row(row)

            if score > best_score:
                best_score = score
                best_index = index

        header = [str(x).strip() if x is not None else "" for x in rows[best_index]]

        return HeaderDetectionResult(
            row_index=best_index,
            score=best_score,
            header=header,
        )

    def _score_row(
        self,
        row: list[object],
    ) -> int:
        score = 0

        values = [str(v).strip() for v in row if v is not None and str(v).strip()]

        populated = len(values)

        if populated == 0:
            return -100

        score += populated * 2
        score += len(set(values))

        if populated == 1:
            score -= 8

        lowered = [v.lower() for v in values]

        for value in lowered:
            for keyword in COMMON_HEADER_WORDS:
                if keyword in value:
                    score += 5

        long_cells = sum(len(v) > 40 for v in values)

        score -= long_cells * 5

        return score
