# Reproduction guide

See the [project overview](../README.md), [data downloads and provenance](../data/data.md), [methods](methods-and-validation.md) and [references](references.md). Original data and derived inputs are ignored by Git, so a clone alone cannot rerun the analysis. No local lecture material is a runtime dependency.

## Environment

Use Python 3.12; local setup was checked with Python 3.12.3. [requirements.txt](../requirements.txt) pins direct dependencies; transitive dependencies are not locked. Reuse the root `.venv` if present. From the repository root on Ubuntu/WSL:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m ipykernel install --sys-prefix --name london-pedestrian-collision-analysis --display-name "Python (London pedestrian collisions)"
```

Create the environment only if absent. The kernel registration is local to the environment and is not a portable file to commit. On Windows or macOS, use Python 3.12 and the shell-appropriate environment activation command, then the same `python -m` installation and registration commands. No WSL-specific path or service is required.

Launch JupyterLab from the environment:

```bash
cd notebooks
python -m jupyterlab
```

Select **Python (London pedestrian collisions)**, or the repository's `.venv` interpreter if the editor discovers environments directly. Saved notebook kernel names may differ from the locally registered name; select the documented project environment. All notebooks expect `notebooks/` as their working directory and default to `../data`.

## Reproduce the ignored inputs

Preserve the supplied manifest and source files. For exact-input reproduction, use files matching its checksums. Published URLs can serve revised files; investigate mismatches rather than replacing recorded hashes. Final submission input-packaging arrangements remain to be confirmed.

1. Obtain the eight annual collision/casualty CSVs and the Excel guide using [data.md](../data/data.md#downloads), placing them alongside `download-manifest.json` in `data/`.
2. Obtain the [official boundary GeoPackage](https://open-geography-portalx-ons.hub.arcgis.com/api/download/v1/items/a4d56f9755be48b0a78c120e499fa9df/geoPackage?layers=0) as `data/ons-lad-december-2024-uk-bfe.gpkg`. Preserve the existing manifest entry.
3. Run notebook 01 to verify supplied inputs and generate `data/derived/pedestrian_collision_candidates.csv` and `data/derived/preparation_log.csv`.
4. Run notebook 02 to audit spatial membership and provide the nine validation exports. Choose an unused output directory if a separate export is needed.
5. Run notebook 03 for the descriptive grid comparison and notebook 04 for inference. Both use notebook 02's saved validation artifacts independently; notebook 04 does not need notebook 03's kernel or outputs.

These are manual execution instructions, not a record of a new run. Under project working instructions, AI execution of real-data processing requires specific authorisation; predictive training is neither part of this workflow nor authorised by these instructions.

### Boundary acquisition script

For initial acquisition only, from the repository root with the environment active:

```bash
python scripts/download_boundaries.py
```

The script downloads the official December 2024 BFE GeoPackage and checks supplied response size, the GeoPackage identifier, SQLite integrity and feature-layer metadata before preserving the file and adding provenance. It refuses an existing boundary file or manifest entry. Because the supplied manifest already has that entry, use the direct download above for a clone; do not reset the manifest to force acquisition. `--data-dir` supports an external folder containing the existing manifest. No extra dependency is required.

## Notebook inputs and output protection

| Notebook | Purpose | File writes |
| --- | --- | --- |
| [01](../notebooks/01_data_understanding_preparation.ipynb) | Inspection, EDA and candidate preparation | Replaces the two named derived CSVs; never overwrites raw inputs |
| [02](../notebooks/02_spatial_validation.ipynb) | London membership and diagnostics | Writes nine validation artifacts only if none of their names exists |
| [03](../notebooks/03_croydon_grid_comparison.ipynb) | Croydon selection and descriptive grids | In-memory tables and figures; optional PNG map export, disabled by default |
| [04](../notebooks/04_croydon_spatial_inference.ipynb) | Main inference and grid sensitivity | In-memory tables and figures; optional PNG map export, disabled by default |

For an authorised manual run, open the required notebook, check its parameters, restart the kernel, run cells in order and save. Notebook 01 reads selected fields one year or collision/casualty pair at a time; its shared selection supports both EDA and preparation. Original files remain unchanged.

Notebook 02 requires candidates, guide, manifest, boundary and four original annual collision CSVs. Its default `OUTPUT_DIR` is `DATA_DIR / "derived" / "spatial_validation_closure"`. If any named output exists, it skips all writes, lists existing/missing outputs and compares stored/current input hashes. Select a new project-relative directory before exporting separately; do not delete preserved results to force a rerun. Earlier exports remain in `data/derived/spatial_validation/`.

Notebooks 03/04 require the original boundary and guide, manifest, candidates, validation audit, borough evidence and `validation_run.json`. They verify source hashes and stop on mismatches rather than mixing candidate versions with older validation evidence. If candidates change after notebook 01 runs, validate those inputs in notebook 02 and use the corresponding new export directory. Matching hashes alone do not prove artifact contents or positional accuracy.

`COMP1890_DATA_DIR` supports external inputs. Notebooks 03/04 also accept `COMP1890_VALIDATION_DIR` and `COMP1890_BOUNDARY_PATH`; the default layout needs no environment-variable command. Keep paths relative to the documented working directory, or configure them explicitly for external inputs. Notebook 02's export location is configured through its Python `OUTPUT_DIR` parameter.

## Optional report figure exports

Notebooks 03/04 retain inline plots and can additionally save selected existing maps to `evidence/`. No new maps or statistical methods are introduced. Set `EXPORT_FIGURES = True` in the relevant input cell before an authorised manual run; the default `False` performs no image writes. `FIGURE_DIR` defaults to `../evidence` from `notebooks/` and can be configured through `COMP1890_FIGURE_DIR`.

Existing images raise `FileExistsError` unless `OVERWRITE_FIGURES = True`; inspect files before explicitly replacing them. Output uses 300 dpi PNG with a tight bounding box. See [export filenames, source cells and caption guidance](../evidence/README.md). Saved inline outputs predate the export-code update; no new run or exported-image review is implied. Final attribution and report-layout checks remain pending.

## Synthetic checks

From the repository root with the environment active:

```bash
python -m unittest discover -s tests -v
```

The 7 grid and 14 inference tests extract only pure function definitions. They use synthetic geometry/counts, including a high-precision Decimal binomial oracle and hand-calculated BY cases, and do not read real datasets or train models. They do not verify provenance, the spatial null or final figure readability. Execution counts and saved notebook outputs alone do not establish a fresh-kernel run.
