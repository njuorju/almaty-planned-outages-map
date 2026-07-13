#!/usr/bin/env python3
"""Build the standalone map page from the published GeoJSON and CSV files.

This script does not recreate the upstream OSM matching and block reconstruction.
It rebuilds the static website from the final audited analytical layer included in
this repository.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
TEMPLATE_PATH = ROOT / "site" / "index.template.html"
OUTPUT_PATH = ROOT / "index.html"

COLORS = {
    "13.07.2026": "#e41a1c",
    "14.07.2026": "#377eb8",
    "15.07.2026": "#4daf4a",
    "16.07.2026": "#ff7f00",
    "17.07.2026": "#984ea3",
}

LABELS = {
    "13.07.2026": "Пн 13 июля",
    "14.07.2026": "Вт 14 июля",
    "15.07.2026": "Ср 15 июля",
    "16.07.2026": "Чт 16 июля",
    "17.07.2026": "Пт 17 июля",
}


def load_json(path: Path) -> object:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def build_schedule() -> list[dict[str, object]]:
    records = {int(row["outage_id"]): row for row in load_csv(DATA_DIR / "outage_records.csv")}
    audit = load_csv(DATA_DIR / "matching_audit.csv")

    schedule: list[dict[str, object]] = []
    for row in audit:
        outage_id = int(row["outage_id"])
        source = records[outage_id]
        schedule.append(
            {
                "outage_id": outage_id,
                "res": source["res"],
                "date": source["date"],
                "time": source["time"],
                "zone": source["zone_label"],
                "address": source["address"],
                "selected_blocks": int(row["selected_blocks"]),
                "method": row["method"],
                "confidence": row["confidence"],
            }
        )

    schedule.sort(key=lambda item: (str(item["date"])[6:10], str(item["date"])[3:5], str(item["date"])[0:2], str(item["time"]), int(item["outage_id"])))
    return schedule


def compact_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def main() -> None:
    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    geojson = load_json(DATA_DIR / "outage_city_blocks.geojson")
    schedule = build_schedule()

    replacements = {
        "__DATA_JSON__": compact_json(geojson),
        "__SCHEDULE_JSON__": compact_json(schedule),
        "__COLORS_JSON__": compact_json(COLORS),
        "__LABELS_JSON__": compact_json(LABELS),
    }

    output = template
    for token, value in replacements.items():
        if token not in output:
            raise RuntimeError(f"Template token not found: {token}")
        output = output.replace(token, value)

    OUTPUT_PATH.write_text(output, encoding="utf-8")
    print(f"Built {OUTPUT_PATH.relative_to(ROOT)} with {len(schedule)} schedule records and {len(geojson['features'])} polygons.")


if __name__ == "__main__":
    main()
