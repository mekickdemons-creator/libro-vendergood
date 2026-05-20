#!/usr/bin/env python3
"""
query.py — run a SELECT query and retrieve features for matched objects.

Usage:
    python tools/query.py "root_2 <> \\"\\""
    python tools/query.py "mood_suffix = \\"alt\\""
    python tools/query.py "source = \\"temporpont\\""

The argument is a feature constraint expression (the body of the
[Word <constraint>] clause). Quotes inside must be escaped for shell.

Internally:
  1. Runs SELECT ALL OBJECTS WHERE [Word <constraint>] to get id_ds.
  2. Runs GET FEATURES surface, lemma, root_1, root_2, category, mood_suffix,
     source, gloss FROM OBJECTS WITH id_d IN (...) [Word]
  3. Prints a table.

Requires mql on PATH and db/vendergood in the cwd or DB_PATH env var.
"""

import json
import os
import subprocess
import sys
from pathlib import Path

DB_DIR = Path(os.environ.get("DB_PATH", Path(__file__).parent.parent / "db"))
DB_NAME = "vendergood"
FEATURES = ["surface", "lemma", "root_1", "root_2", "category", "mood_suffix",
            "source", "gloss"]


def run_mql(query: str) -> dict:
    result = subprocess.run(
        ["mql", "-b", "3", "--json"],
        input=query,
        capture_output=True,
        text=True,
        cwd=DB_DIR,
    )
    if result.returncode not in (0, 6):
        print(f"mql error:\n{result.stderr}", file=sys.stderr)
        sys.exit(1)
    return json.loads(result.stdout)


def select_ids(constraint: str) -> list[int]:
    query = f"USE DATABASE '{DB_NAME}' GO\nSELECT ALL OBJECTS WHERE\n[Word {constraint}]\nGO\n"
    data = run_mql(query)
    results = data.get("mql_results", [])
    if len(results) < 2:
        return []
    sheaf = results[1].get("sheaf", {})
    straws = sheaf.get("straws", [])
    ids = []
    for straw in straws:
        for obj in straw.get("matched_objects", []):
            ids.append(obj["id_d"])
    return ids


def get_features(id_ds: list[int]) -> list[dict]:
    id_list = ", ".join(str(i) for i in id_ds)
    feat_list = ", ".join(FEATURES)
    query = (
        f"USE DATABASE '{DB_NAME}' GO\n"
        f"GET FEATURES {feat_list}\n"
        f"FROM OBJECTS WITH ID_DS = {id_list}\n"
        f"[Word]\n"
        f"GO\n"
    )
    data = run_mql(query)
    results = data.get("mql_results", [])
    if len(results) < 2:
        return []

    table = results[1].get("table", {})
    trows = table.get("trows", [])
    rows = []
    for trow in trows:
        cols = trow.get("tcolumns", [])
        # cols[0] is id_d, cols[1:] are the features in order
        if len(cols) >= len(FEATURES) + 1:
            row = {feat: cols[i + 1] for i, feat in enumerate(FEATURES)}
            rows.append(row)
    return rows


def print_table(rows: list[dict]) -> None:
    if not rows:
        print("(no results)")
        return

    cols = ["surface", "lemma", "root_1", "root_2", "category", "mood_suffix",
            "source", "gloss"]
    widths = {c: max(len(c), max(len(str(r.get(c, ""))) for r in rows)) for c in cols}

    header = "  ".join(c.ljust(widths[c]) for c in cols)
    sep = "  ".join("-" * widths[c] for c in cols)
    print(header)
    print(sep)
    for row in rows:
        print("  ".join(str(row.get(c, "")).ljust(widths[c]) for c in cols))

    print(f"\n{len(rows)} result(s)")


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python tools/query.py \"<feature_constraint>\"")
        print("Example: python tools/query.py 'root_2 <> \"\"'")
        sys.exit(1)

    constraint = sys.argv[1]
    ids = select_ids(constraint)
    if not ids:
        print("(no matching objects)")
        return

    rows = get_features(ids)

    print_table(rows)


if __name__ == "__main__":
    main()
