# Report figure evidence

This folder is for selected report figures and their source information. Dataset exports and validation artifacts stay under `data/derived/`. No image exports have been generated or visually reviewed for this folder yet; the source notebooks retain their earlier saved inline figures.

## Available export code

Run from `notebooks/` using the documented environment and supplied inputs. In notebook 03 or 04's input cell, set `EXPORT_FIGURES = True` before an authorised manual run. `FIGURE_DIR` defaults to `../evidence`; `COMP1890_FIGURE_DIR` configures another location. Exports are 300 dpi PNGs with a tight bounding box, saved before inline display. With exports disabled, the helper creates no directories or files.

An existing target raises a clear error unless `OVERWRITE_FIGURES = True`. Inspect old exports before replacing them; a stopped run must not be interpreted as producing a new figure. Both notebook helpers use exclusive creation by default to protect existing images.

| Filename | Source notebook / cell | Caption guidance and interpretation |
| --- | --- | --- |
| `croydon_grid_comparison_100m_250m_500m.png` | [03](../notebooks/03_croydon_grid_comparison.ipynb), `grid-maps` | Reported pedestrian injury collision counts, 2022–2025, on 100/250/500 m clipped grids within Croydon's fixed ONS December 2024 footprint. Zero-count and partial cells remain included. Shared raw-count colours do not adjust for cell area or pedestrian exposure. EPSG:27700. |
| `croydon_inference_500m_250m.png` | [04](../notebooks/04_croydon_spatial_inference.ipynb), `maps` | Main 500 m and sensitivity 250 m maps under an 850 m centre-distance neighbourhood rule. Shading locates focal cells with BY-significant neighbourhood tests at 5% separately per grid, under an independent uniform-land-area null. Shading does not test a focal cell alone or measure pedestrian risk; the null ignores roads and exposure. EPSG:27700. |

Filenames do not assign final report figure numbers. Notebook 03's distribution chart is still displayed inline but is not exported by this setting. No new points map, workflow diagram or cartographic redesign is included.

## Before report reuse

- Inspect exported figures at the intended PDF size; export support alone does not establish report readiness.
- Verify product-specific ONS/OS attribution, including the applicable year, and include the required wording in the figure or final caption. Retain DfT source citations and period information; see [R01](../docs/references.md#r01) and [R05–R06](../docs/references.md#r05).
- Keep quantity, period, coordinate system and material limitations with each figure. Captions above are guidance, not completed source accreditation.
- Select only figures that support the report. Track the curated final PNGs after checking content and file sizes; do not stage unrelated datasets or temporary images.

## Validation status

The export code must be checked separately from real-data execution. No new notebook run, figure generation, visual acceptance or final attribution verification is claimed here. AI execution of a real-data run requires specific authorisation under the [project instructions](../AGENTS.md). See the [reproduction guide](../docs/reproduction.md#optional-report-figure-exports).
