# Methodology and uncertainty

## Purpose

The source publication is an address-based schedule of planned electricity interruptions. It does not provide official network polygons, feeder service areas, transformer catchments, or machine-readable spatial data. The map therefore translates textual address information into an approximate, navigable spatial representation.

## Processing logic

1. Consolidate the published schedule into one record per outage entry.
2. Normalize street names, address ranges, neighbourhood names, and common Russian/Kazakh spelling variants.
3. Search an OpenStreetMap-derived address and building cache across Almaty rather than relying on manually assigned neighbourhood centres.
4. Use matched address buildings as location evidence only.
5. Group nearby evidence and derive morphological urban-block envelopes from the surrounding built form.
6. Store the resulting block polygons with the original outage record and a confidence classification.
7. Publish the layer as GeoJSON and embed it in a standalone Leaflet interface with chronological filtering.

## Confidence classes

- **High:** the address evidence and selected block geometry are strongly supported.
- **Medium:** the general location is supported, but the exact set of affected blocks remains interpretive.
- **Low:** the source address is vague, incomplete, unmatched, or requires a neighbourhood-centre fallback. These polygons are displayed with dashed boundaries and reduced opacity.

## Important limitation

The polygons are analytical approximations. They are not official outage boundaries and do not represent the topology of the electricity distribution network. A single listed address range may be served by multiple network elements, while a network interruption may affect only part of a mapped block.

Users should verify the listed address and time against the original AЖК publication before relying on the map.
