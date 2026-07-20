# Almaty Planned Utility Outages Map

An unofficial interactive map of planned urban-service interruptions in Almaty. The interface now uses one common spatial-temporal model for **electricity, water, gas and district heating**. The current dataset contains electricity interruptions published by АО «АЖК» for **20–27 July 2026**; the other service layers are present in the interface but have not yet been populated.

**Live map:** [power-outage-plan.fdas201290.workers.dev](https://power-outage-plan.fdas201290.workers.dev/)

## Current release

- **86** normalized electricity-interruption records;
- **86** event geometries containing **626** approximate urban-block polygons;
- one stable colour per utility type rather than per day;
- a date slider covering 20–27 July 2026;
- service filters for electricity, water, gas and heating;
- no permanent address list obscuring the map;
- popups with provider, time, equipment, source address and spatial confidence;
- visible dashed styling for low-confidence spatial matches.

The source page covers 20–27 July, but the published schedule contains records only for 20–24 July. The slider retains the full advertised period and shows an empty-state message on dates with no published records.

## Common event model

Every source adapter is expected to produce the same core fields:

```text
event_id
utility_type
provider
event_type
status
date
time
address
geometry
geometry_method
spatial_confidence
source_url
```

This allows later water, gas and heating records to enter the same interface without redesigning the map. Roadworks can later use the same event model with line geometry rather than block polygons.

## Method

АЖК publishes an address-based schedule without official outage-area geometry. Street names, address ranges and neighbourhood names were normalized and matched against OpenStreetMap-derived address evidence. Address-tagged buildings were used only as location seeds; the displayed features are approximate morphological block envelopes, not building footprints or electrical-network service areas.

The full methodology and confidence rules are documented in [`docs/methodology.md`](docs/methodology.md). Record-level matching evidence is available in [`data/matching_audit.csv`](data/matching_audit.csv).

## Repository contents

```text
.
├── index.html                    # standalone deployable map
├── data/
│   ├── utility_events.geojson.gz.b64 # compressed static GeoJSON payload
│   ├── utility_events.csv        # one row per source event
│   └── matching_audit.csv        # record-level spatial audit
├── docs/
│   ├── methodology.md
│   └── qa-report.md
├── scripts/
│   ├── build_site.py
│   └── validate_data.py
├── site/index.template.html
├── ATTRIBUTION.md
├── DATA_LICENSE.md
└── LICENSE
```

## Rebuild and validate

Python 3.10 or newer is sufficient for the published static-site build:

```bash
python scripts/validate_data.py
python scripts/build_site.py
python -m http.server 8000
```

Then open `http://localhost:8000/`. An internet connection is required for Leaflet and OpenStreetMap background tiles.

## Disclaimer

**This is an unofficial analytical visualization.** It is not affiliated with АО «АЖК», the Almaty akimat or any utility organization.

The polygons are approximate interpretations of published addresses. They are not official electricity-network, transformer, feeder or service-area boundaries. Check the original provider notice before relying on an address or interruption time.

## Author

**Nikolay Nikolaev**

- [LinkedIn](https://www.linkedin.com/in/ninikolaev/)
- [GitHub](https://github.com/njuorju)

## Sources and licensing

Electricity schedule: [АО «Алатау Жарық Компаниясы», 20–27 July 2026](https://www.azhk.kz/ru/spetsialnye-razdely/graphics/101-grafik-otklyuchenij/2020-god/5229-gorod-almaty-s-20-07-2026-goda-po-27-07-2026-goda)

Geographic data and derived geometry use OpenStreetMap data and retain attribution to OpenStreetMap contributors. Original project code and documentation are released under the MIT License. Third-party and geographic-data terms are described separately in [`ATTRIBUTION.md`](ATTRIBUTION.md) and [`DATA_LICENSE.md`](DATA_LICENSE.md).

---

## Кратко по-русски

Неофициальная карта плановых отключений городских услуг в Алматы. Интерфейс поддерживает электричество, воду, газ и теплоснабжение; сейчас заполнен слой электричества по графику АЖК на 20–27 июля 2026 года. Цвет показывает вид услуги, дата выбирается ползунком, а пунктир обозначает низкую точность пространственной привязки. Полигоны являются аналитической интерпретацией адресов, а не официальными границами сетей.
