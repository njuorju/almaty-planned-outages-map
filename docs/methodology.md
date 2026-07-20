# Methodology and uncertainty

## Purpose

The project is a common map for planned interruptions of electricity, water, gas and district heating in Almaty. Each provider-specific notice is normalized into the same spatial-temporal event model. The current release populates only the electricity layer using the АЖК schedule for 20–27 July 2026.

## Source processing

1. Extract one record for each published interruption entry.
2. Normalize dates, times, provider divisions, equipment, work type and raw location text.
3. Normalize street names, address ranges, neighbourhood names and common Russian/Kazakh spelling variants.
4. Match address evidence against an OpenStreetMap-derived Almaty address and building cache.
5. Use matched buildings only as location seeds.
6. Derive approximate morphological urban-block envelopes from the surrounding built form.
7. Store each source entry as one event feature, using `Polygon` or `MultiPolygon` geometry and a component-polygon count.
8. Simplify and coordinate-round the geometry for lightweight browser delivery.

The interface assigns a permanent colour to each utility type. The selected date controls visibility rather than colour. Water, gas and heating already exist as empty interface layers and can later be populated through additional source adapters.

## Confidence classes

- **High:** address evidence and the selected block geometry are strongly supported.
- **Medium:** the general location is supported, but the precise set of affected blocks remains interpretive.
- **Low:** the source description is vague, incomplete, unmatched or requires a neighbourhood-level fallback. Low-confidence geometry is displayed with a dashed boundary and reduced opacity.

## Important limitations

The source schedule does not contain official network polygons, feeder service areas, transformer catchments or machine-readable spatial boundaries. The displayed geometry is therefore an analytical interpretation of address text.

A listed address range may span several service areas, while an interruption may affect only part of a mapped block. Users should verify the exact address and time against the original provider publication before relying on the map.

Future roadworks can use the same event model, but they should normally be represented as street-line geometry rather than artificial block polygons.
