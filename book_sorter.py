#!/usr/bin/env python3
import csv
import sys
from pathlib import Path


def read_csv(csv_path: Path) -> list[dict]:
    with csv_path.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


def sort_key(row: dict) -> str:
    title = row.get("title", "")
    if title is None:
        title = ""
    return str(title).lower()


def write_sorted_csv(input_csv: Path, rows: list[dict]) -> Path:
    out_path = input_csv.with_name(f"{input_csv.stem}_sorted.csv")

    # Use the same header fields/order as the input CSV
    fieldnames = list(rows[0].keys()) if rows else []

    # Drop any "None" key (happens when a row has extra commas/fields)
    fieldnames = [f for f in fieldnames if f is not None]

    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for row in rows:
            # Keep only keys that exist in the header
            clean_row = {k: v for k, v in row.items() if k in fieldnames}
            writer.writerow(clean_row)

    return out_path



def main() -> int:
    FALLBACK_PATH = "book_list.csv"

    if len(sys.argv) > 2:
        print(f"Usage: {sys.argv[0]} [path/to/file.csv]")
        return 2

    if len(sys.argv) == 2:
        csv_file = Path(sys.argv[1])
        if not csv_file.exists() or not csv_file.is_file():
            print(f"Usage: {sys.argv[0]} [path/to/file.csv]")
            return 2
        if csv_file.suffix.lower() != ".csv":
            print(f"Usage: {sys.argv[0]} [path/to/file.csv]")
            return 2
    else:
        csv_file = Path(FALLBACK_PATH)

    rows = read_csv(csv_file)
    rows.sort(key=sort_key)

    # Optional: print full titles without truncation
    for row in rows:
        print(row.get("title", ""))

    out_path = write_sorted_csv(csv_file, rows)
    print(f"Count: {len(rows)}")
    print(f"Wrote: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
