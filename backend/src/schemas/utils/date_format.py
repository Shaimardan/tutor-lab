from datetime import datetime
from typing import Any


def parse_date(value: Any) -> datetime | None:
    if isinstance(value, datetime) or value is None:
        return value
    date_formats = [
        "%d-%m-%Y",
        "%d.%m.%Y",
        "%Y-%m-%dT%H:%M:%S.%fZ",
        "%Y-%m-%dT%H:%M:%S.%f",
        "%Y-%m-%d",
        "%Y/%m/%d",
        "%d/%m/%Y",
        "%m-%d-%Y",
    ]
    for fmt in date_formats:
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            continue
    raise ValueError(f"date format error. Acceptable forms {[f for f in date_formats ]}")
