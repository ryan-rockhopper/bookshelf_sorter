#!/usr/bin/env python3
import csv
import sys
from pathlib import Path


def read_csv(csv_path: Path) -> list[dict]:
    with csv_path.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)

def title_key(row: dict) -> str:
    title = row.get("title", "")
    if title is None:
        return ''
    else:
        return str(title).lower()


def main() -> int:
    # 1) Determine CSV path
    FALLBACK_PATH = 'book_list.csv'

    if len(sys.argv) > 2:
        print(f"Usage: {sys.argv[0]} [path/to/file.csv]")
        return 2

    if len(sys.argv) == 2:
        candidate = Path(sys.argv[1])

        if not candidate.exists() or not candidate.is_file():
            print(f"Usage: {sys.argv[0]} [path/to/file.csv]")
            return 2

        if candidate.suffix.lower() != ".csv":
            print(f"Usage: {sys.argv[0]} [path/to/file.csv]")
            return 2

        csv_file = candidate
    else:
        csv_file = Path(FALLBACK_PATH)

    # 2) Read CSV into a data structure
    rows = read_csv(csv_file)

    rows.sort(key=title_key)

    # 4) Print titles + count
    for row in rows:
        print(title_key(row))

    print(f"Count: {len(rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
