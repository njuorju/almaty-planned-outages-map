#!/usr/bin/env python3
"""Run lightweight consistency checks for the published map data."""
from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"


def read_csv(name: str) -> list[dict[str, str]]:
    with (DATA_DIR / name).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    with (DATA_DIR / "outage_city_blocks.geojson").open("r", encoding="utf-8") as handle:
        geojson = json.load(handle)

    records = read_csv("outage_records.csv")
    audit = read_csv("matching_audit.csv")
    features = geojson.get("features", [])

    assert geojson.get("type") == "FeatureCollection"
    assert len(records) == 61, len(records)
    assert len(audit) == 61, len(audit)
    assert len(features) == 447, len(features)
    assert all(feature.get("geometry", {}).get("type") == "Polygon" for feature in features)

    record_ids = {int(row["outage_id"]) for row in records}
    audit_ids = {int(row["outage_id"]) for row in audit}
    feature_ids = {int(feature["properties"]["outage_id"]) for feature in features}
    assert record_ids == audit_ids == feature_ids

    polygon_counts = Counter(int(feature["properties"]["outage_id"]) for feature in features)
    for row in audit:
        assert polygon_counts[int(row["outage_id"])] == int(row["selected_blocks"])

    print("Validation passed")
    print(f"  outage records: {len(records)}")
    print(f"  block polygons: {len(features)}")
    print(f"  confidence: {Counter(row['confidence'] for row in audit)}")


if __name__ == "__main__":
    main()
