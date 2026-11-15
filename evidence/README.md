# Report figure evidence

This folder holds selected figure exports and source information; dataset and validation artifacts stay under `data/derived/`. The original three-panel grid and inference PNGs were exported in a manual run and visually inspected. All four report/appendix exports are now present and have been visually inspected against the saved outputs. Final PDF-size readability and complete attribution remain unverified.

## Export settings and protection

Run notebooks from `notebooks/` with the documented environment and supplied inputs. Notebooks 02–04 currently set `EXPORT_FIGURES = True` in their input cell; set it to `False` for inline-only use. `FIGURE_DIR` defaults to `../evidence`; `COMP1890_FIGURE_DIR` supports another location. Exports are 300 dpi PNGs with a tight bounding box, saved before inline display. With exports disabled, the helper creates no directories or files.

The helper renders a PNG in memory and compares its bytes with the existing file. Identical PNGs are retained without rewriting; new or changed PNGs are saved through a temporary file in the same directory and then installed with `os.replace`. This avoids the previous existing-file error and preserves the old PNG if rendering, writing or replacement fails. Temporary files are cleaned up; no overwrite flag is required. Byte comparison is exact, so rendering or metadata changes can cause replacement even when a figure looks similar.

Notebook 03 additionally sets `EXPORT_LEGACY_FIGURES = False`: its original three-panel map still displays inline but its existing PNG is not rewritten. Its new report figures use new filenames. Notebook 04's revised map also uses a new `_report.png` filename, preserving the original inference PNG.

## Figure register

| Filename | Source notebook / cell | Status and caption guidance |
| --- | --- | --- |
| `croydon_grid_comparison_100m_250m_500m.png` | [03](../notebooks/03_croydon_grid_comparison.ipynb), `grid-maps` | Existing exploratory export: 100/250/500 m raw-count grids, including zeros and partial cells. Shared colours do not adjust for cell area or pedestrian exposure. The 100 m panel has low contrast; retain as supporting evidence rather than assuming report readiness. |
| `croydon_inference_500m_250m.png` | [04](../notebooks/04_croydon_spatial_inference.ipynb), earlier `maps` source | **Superseded historical export:** 74/276 flagged focal cells in the earlier layout. The current notebook no longer regenerates this layout; use `croydon_inference_500m_250m_report.png` for report preparation. This file is retained locally for comparison, with no decision to include it in the commit or submission. |
| `croydon_collision_locations_context.png` | [03](../notebooks/03_croydon_grid_comparison.ipynb), `report-points-map` | Generated and visually inspected: selected recorded collision centres in Croydon, plus its London location using the same boundary input. The point count comes from the selected records; symbols may overlap. Coordinates are not independently accuracy-validated, and the map alone does not establish road alignment, causes or individual risk. |
| `croydon_grid_comparison_250m_500m.png` | [03](../notebooks/03_croydon_grid_comparison.ipynb), `report-grid-map` | Generated and visually inspected: shared raw-count classes for the existing 250/500 m grids, including zeros. Blue dashed outlines identify partial cells; unequal clipped support is not exposure. This is not a significance map. |
| `croydon_inference_500m_250m_report.png` | [04](../notebooks/04_croydon_spatial_inference.ipynb), revised `maps` | Generated and visually inspected: main 500 m and sensitivity 250 m maps with external shared legend, scale bars and grid-north arrows. Shading locates focal cells with BY-significant neighbourhood tests at 5% separately per grid under independent uniform-land-area placement. It does not test a focal cell alone or estimate risk; the null ignores roads and exposure. |
| `membership_boundary_examples.png` | [02](../notebooks/02_spatial_validation.ipynb), `python-inspection-maps` | Generated and visually inspected appendix export of the existing two examples, not a redesigned map. Recorded/geometric membership and point-to-recorded-polygon distances illustrate validation; two examples do not verify all records or positional accuracy. Existing axes indicate metres and the title indicates grid north. |

All maps concern 2022–2025 reported pedestrian injury collisions and use EPSG:27700. The Croydon analysis uses a fixed December 2024 footprint. These filenames do not assign final report figure numbers. No workflow diagram, distribution-chart export or new inferential method is included.

## Tables and report narrative

- **Data preparation and validation table:** reuse saved evidence from notebooks 01/02 and the final selection in notebook 03. Label national candidates, recorded-London and geometric memberships explicitly; recorded/geometric classifications must not be presented as an unexplained filtering chain. Record-selection checks and spatial validation serve different purposes.
- **Compact results table:** use notebook 03's grid properties and notebook 04's original comparison and new `report-area-summary` display. The saved display gives an actual footprint area of 86.466113 km², focal-area shares of 20.115% / 19.308%, and event shares of 62.500% / 57.955% at 500 m / 250 m. Keep overlap and reproduced share labelled separately, and do not imply joint BY control or independent replication.
- **Practical implications:** connect limitations to further investigation using pedestrian/vehicle flows, crossings, junctions, speed, lighting and collision circumstances. See [future work](../docs/methods-and-validation.md#practical-implications-and-future-work). Unflagged areas are not established as safe.

These are evidence-selection notes based on saved outputs, not a completed report. Select three complementary main figures and compact tables according to the final layout; the membership examples are appendix candidates. A workflow diagram remains optional.

## Attribution and final reuse

The [ONS licence guidance](https://www.ons.gov.uk/methodology/geography/licences) was rechecked on 15 November 2026. It requires ONS source accreditation and an OS copyright/database-right statement. The [official product item](https://www.arcgis.com/home/item.html?id=a4d56f9755be48b0a78c120e499fa9df) and linked service identify ONS/OS rights but did not provide an explicit copyright year in the inspected metadata. The map footers therefore use 2025, the year the December 2024 boundary product was published (the ArcGIS item was created on 8 January 2025). This is an inference from the publication year, not a year stated by ONS; confirm it with ONS or the Open Geography Portal download page if certainty is required.

Retain DfT source citations and the original data access date in final captions; see [R01](../docs/references.md#r01) and [R05–R06](../docs/references.md#r05). Notebook 02's exported example figure keeps its existing content; its final caption must supply the relevant attribution. Keep quantity, period, coordinate system and interpretation limits beside every figure, applying the uniform-area-null description specifically to inference figures.

Inspect new images at the intended PDF width, including point visibility, class/partial-cell distinctions, legends, scale bars and footer legibility. The new main figures are designed at 6.3 inches wide, but source dimensions alone do not prove readability. Track only selected, reviewed PNGs after checking file sizes; staging and commits require explicit instructions.

## Execution status

Manual reruns were reported for notebooks 01–04, and their saved outputs contain no errors. See [saved execution evidence](../docs/methods-and-validation.md#saved-execution-and-figure-evidence) for the inspected metadata and remaining gap; the saved files do not independently demonstrate complete fresh-kernel execution.

The saved report-figure messages in notebooks 02–04 say `Figure unchanged; kept existing PNG`, confirming the revised helper reached its identical-byte branch for the four current report/appendix exports. New-file creation, changed-image replacement and failure handling remain covered by mock tests, not an additional real-data run of every branch. Notebook 02's saved final export message reports all nine existing validation artifacts retained with matching input hashes; they were not regenerated.

The location map shows a denser northern pattern and Croydon's London context; the count-map legend and dashed partial cells are visible; the inference map's external legend leaves the footprint unobscured. Its 74/276 cell titles and northern/southern patterns agree with saved summaries. The two membership examples remain consistent with the recorded/geometric table. This inspection does not establish final acceptance in a composed PDF or resolve attribution.

No further rerun is required solely for these wording edits: code, outputs and PNGs are unchanged. If a future run changes a figure, the helper compares PNG bytes and replaces the image only after a complete save. AI execution of real-data processing still requires specific authorisation under [AGENTS.md](../AGENTS.md); staging and commits also require explicit instructions. See the [reproduction guide](../docs/reproduction.md#optional-report-figure-exports).
