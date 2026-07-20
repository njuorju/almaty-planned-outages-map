#!/usr/bin/env python3
"""Validate the compressed static GeoJSON payload used by the map."""
from __future__ import annotations

import base64
import gzip
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"


def fail(message: str) -> None:
    raise SystemExit(f"VALIDATION FAILED: {message}")


def main() -> None:
    parts = sorted(DATA_DIR.glob("utility_events.part*"))
    if not parts:
        fail("compressed data chunks are missing")

    encoded = "".join(part.read_text(encoding="ascii").strip() for part in parts)
    try:
        raw = gzip.decompress(base64.b64decode(encoded)).decode("utf-8")
        geojson = json.loads(raw)
    except Exception as exc:
        fail(f"cannot decode utility payload: {exc}")

    if geojson.get("type") != "FeatureCollection":
        fail("payload is not a FeatureCollection")

    features = geojson.get("features", [])
    if len(features) != 86:
        fail(f"expected 86 event features, found {len(features)}")

    required = {
        "event_id",
        "utility_type",
        "provider",
        "date",
        "time",
        "address",
        "confidence",
        "polygon_count",
    }

    for index, feature in enumerate(features, start=1):
        geometry_type = feature.get("geometry", {}).get("type")
        if geometry_type not in {"Polygon", "MultiPolygon"}:
            fail(f"feature {index} has unsupported geometry: {geometry_type}")

        properties = feature.get("properties", {})
        missing = required.difference(properties)
        if missing:
            fail(f"feature {index} is missing properties: {sorted(missing)}")

        if properties["utility_type"] != "electricity":
            fail(f"feature {index} has unexpected populated utility layer")

    dates = Counter(feature["properties"]["date"] for feature in features)
    confidence = Counter(feature["properties"]["confidence"] for feature in features)
    polygons = sum(int(feature["properties"]["polygon_count"]) for feature in features)

    expected_dates = {
        "20.07.2026": 20,
        "21.07.2026": 4,
        "22.07.2026": 23,
        "23.07.2026": 22,
        "24.07.2026": 17,
    }
    if dict(dates) != expected_dates:
        fail(f"unexpected records by date: {dict(dates)}")
    if polygons != 626:
        fail(f"expected 626 component polygons, found {polygons}")

    print("Validation passed")
    print(f"  data chunks: {len(parts)}")
    print(f"  utility events: {len(features)}")
    print(f"  component polygons: {polygons}")
    print(f"  dates: {dict(dates)}")
    print(f"  confidence: {dict(confidence)}")


if __name__ == "__main__":
    main()
