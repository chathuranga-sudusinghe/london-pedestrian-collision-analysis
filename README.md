# London pedestrian collision analysis

COMP1890 Spatial Data Science project investigating the spatial concentration of reported pedestrian injury collisions in one London borough.

## Research framework

Investigate the spatial concentration of reported pedestrian injury collisions within one London borough. Count each collision involving at least one pedestrian casualty once, including fatal, serious and slight injuries. Without pedestrian exposure data, the findings describe reported collision concentrations rather than pedestrian risk or causal effects.

| ID | Research question |
| --- | --- |
| Main | Where are reported pedestrian injury collisions spatially concentrated within the selected London borough during the study period? |
| SQ1 | How does the spatial distribution of qualifying collision counts vary across the borough? |
| SQ2 | Which local concentrations, if any, are statistically significant under the selected spatial test? |
| SQ3 | How sensitive are the identified concentrations to one alternative spatial-analysis setting? |

SQ1 provides the descriptive component of the main question. Grid-based counts and Getis–Ord Gi* are provisional approaches, with one alternative grid size or neighbourhood setting proposed for SQ3. Final method selection requires justification against the teaching material; any significance result must be interpreted under the selected test's null hypothesis and assumptions.

### Scope and status

The borough and final study period remain undecided; 2022–2025 is the candidate period. No predictive model training is planned. The questions remain unanswered for the final study area until geographic validation and spatial analysis are completed.

The merged notebook has saved execution results for all 14 code cells, including four EDA figures, with no saved errors. Preparation reports 74,682 national candidates, including 17,596 recorded-London and 17 Heathrow-coded collisions, without imputing values or deleting repeated locations. Notebook 02 records resolved London membership under the candidate December 2024 boundaries; the final borough/period, temporal suitability, coordinate agreement and hotspot method remain unresolved.

## Planned QGIS work before submission

**Decision:** use QGIS later in the project, before the final PDF submission. This work is planned and has not yet been completed. Schedule it after the study borough and period are agreed and suitable spatial layers and analysis outputs are available.

- Inspect the selected borough boundary, coordinate reference systems and alignment of collision and analysis layers.
- Prepare final map layouts from verified analysis outputs.
- Capture selected screenshots of the actual QGIS workflow and results for the report's Implementation and Results and Discussions sections, with concise captions explaining their relevance.

Record the QGIS version and the steps actually performed. Use project-relative layer paths when saving the QGIS project. Decide the exact screenshots once the relevant work is complete, keeping the report focused and within its submission limits.

## Project structure

```text
.
├── AGENTS.md                         # Project working instructions
├── README.md                         # Project overview and execution instructions
├── references.md                     # Sources, relevance and adoption status
├── requirements.txt                  # Pinned direct dependencies
├── data/                             # Original CSVs and Excel guide (ignored)
│   ├── data.md                       # Sources, download links and verification status
│   ├── download-manifest.json        # Download provenance and checksums
│   └── derived/                      # Generated candidates and log (ignored)
├── scripts/
│   └── download_boundaries.py        # Candidate ONS boundary acquisition
├── notebooks/
│   ├── 01_data_understanding_preparation.ipynb  # Executed inspection, EDA and preparation
│   └── 02_spatial_validation.ipynb              # Executed validation, diagnostics and exports
└── COMP1890_Spatial_Data_Science/     # Local coursework reference material
```

Add scripts, derived outputs, figures and report folders only when needed. The local reference folder is not a runtime dependency.

## Data

See [data.md](data/data.md) for download links, definitions, provenance and outstanding checks. Keep the eight annual collision/casualty CSVs, Excel guide and `download-manifest.json` in `data/`. Preserve originals and write any future derived data separately.

The notebook expects its working directory to be `notebooks/` and defaults to `../data`. Set `DATA_DIR` or `COMP1890_DATA_DIR` to use another input location. Paths do not depend on a particular repository name or absolute location.

## Data preparation

[01_data_understanding_preparation.ipynb](notebooks/01_data_understanding_preparation.ipynb) verifies inputs, identifiers, joins and pedestrian eligibility once for the shared selection step. Task 1 covers inspection and EDA; Task 2 reuses the selected candidates for field-specific quality flags, an audit and exports. Source values remain unchanged, and the saved run includes the candidate and audit exports.

The export retains national candidates with recorded-London and Heathrow flags so incorrect district codes can be investigated later. It is a candidate dataset, not a final cleaned borough analysis file. Final membership and spatial exclusions require documented boundary checks.

The saved merged-notebook export reports 74,682 candidate rows, and both generated files exist:

- `data/derived/pedestrian_collision_candidates.csv`
- `data/derived/preparation_log.csv`

The saved London audit reports no evaluated date, ID-composition, district-code or coordinate-range problems. It flags 16 records for within-year repeats and 66 for pooled-national repeats, retaining those events. Spatial checks retain their preparation-stage `not_checked` status; notebook 02 supplies the later London membership evidence. Grid/longitude-latitude agreement remains unperformed.

Grid CRS evidence for EPSG:27700 is recorded in the merged notebook. Use the documented grid coordinates for analysis; the supplementary longitude/latitude agreement check remains unperformed because its source datum is unresolved.

## References and spatial validation

The [reference register](references.md) records methodological sources, lecture connections, access dates and whether each source is used, a candidate or background. Dataset provenance remains in [data/data.md](data/data.md), with completed download records in the manifest. Notebook citations should sit beside the claims or methods they support.

The saved validation run checks London boundaries and point membership and includes context and diagnostic maps. All 33 district codes and names reconcile with the guide, polygon-validity safeguards pass and no positive-area district overlaps are reported. The [December 2024 ONS BFE product](references.md#r05) remains subject to temporal-suitability review for the final period.

Use full-resolution boundaries for membership and distinguish interior, boundary, multiple-match and unmatched cases. Keep ambiguous cases auditable rather than automatically assigning the nearest borough, and document the datum and transformation before evaluating coordinate agreement. Grid settings, the final local statistic and multiple-testing treatment remain later decisions; see [validation references](references.md#r07) and [lecture alignment](references.md#r12).

### Acquire the candidate boundary input

From the repository root with the documented environment active, run:

```bash
python scripts/download_boundaries.py
```

The script downloads the official December 2024 UK BFE GeoPackage to `data/ons-lad-december-2024-uk-bfe.gpkg`. It checks the response size when supplied, the GeoPackage identifier, SQLite integrity and feature-layer metadata before preserving the file and appending provenance to the existing manifest. It refuses to replace an existing boundary input and leaves the DfT files and their manifest entries unchanged.

The download completed: 163,885,056 bytes, SHA-256 recorded in the manifest, with layer `LAD_DEC_24_UK_BFE` in EPSG:27700. The source contains 361 UK features, including 33 unique London district codes; the original GeoPackage remains unchanged. If the service returns an incomplete export or a different format, the script stops without registering a completed download.

An external input folder can be supplied with `--data-dir`, provided it contains the existing manifest. No new Python dependency is required for acquisition. The saved spatial-validation run evaluates polygon geometry and membership; acquisition-time manifest checks remain a historical record of the download stage.

### Run spatial validation

[02_spatial_validation.ipynb](notebooks/02_spatial_validation.ipynb) has nine saved code-cell execution counts in sequence, 1–9, with no saved errors, including the corrected highway-status summaries and successful export. All nine output files exist in `data/derived/spatial_validation_closure/`, and the run metadata records seven input hashes. Execution counts alone do not independently establish a fresh-kernel run.

For reproduction, use the documented environment and run from `notebooks/` with the candidate CSV, guide, boundary file, manifest and four original annual collision CSVs available. Notebook 02 works independently of notebook 01's kernel state, using its exported candidates.

The notebook checks polygon validity, reconciles London codes, classifies membership, compares recorded codes and prepares a London context/diagnostic figure. Geographic-coordinate agreement remains `not_checked` by default until the datum evidence is configured; a decision tolerance also needs a rationale. No borough is automatically selected, and no hotspot statistic is calculated.

Validation outputs use the notebook's `OUTPUT_DIR`, currently `DATA_DIR / "derived" / "spatial_validation_closure"`. If any named output exists, the export cell skips all writes, lists existing/missing files and compares stored/current input hashes; choose another new `OUTPUT_DIR` before a future export. Matching input hashes do not establish unchanged code, settings or artifact contents, and the earlier six-file result set remains preserved in `data/derived/spatial_validation/`.

The diagnostics retrieve both highway fields from the original annual collision files with manifest verification and one-to-one joins. They measure distance to the recorded district polygon, classify district pairs by shared edge, point contact or disjointness, and summarise by year and directed borough pair. No threshold, correction or exclusion is applied; the current highway field is location-derived consistency evidence, not independent positional validation.

In VS Code, select the existing project `.venv` kernel, open notebook 02, restart the kernel, run all cells in order and save. The notebook expects its working directory to be `notebooks/`. Its output path is already configured in the first code cell; no terminal environment-variable command is required.

For a future export, select an unused `OUTPUT_DIR` in the notebook's parameter cell before execution. This project-relative Python setting works across Windows, macOS and Linux. Existing results are retained when the configured directory already contains a named output.

The run reads and hashes four original collision CSVs in addition to the boundary, guide and candidate inputs. It performs spatial diagnostics and writes nine outputs only when none of their names already exists in the selected directory. Do not remove preserved exports to force a rerun.

Inspect real outputs in QGIS before selecting screenshots or freezing the final borough dataset. In the exported `london_validation.gpkg`, use `london_boundaries` and `collision_validation` with EPSG:27700; join `district_difference_diagnostics.csv` by `collision_index` when inspecting diagnostic attributes. Review the largest distances and each observed pair-relation category, record the QGIS version and steps performed, and capture genuine screenshots only after inspection.

British National Grid remains the analysis coordinate representation; the longitude/latitude cross-check remains explicitly unperformed. December 2024 is a candidate fixed reference geography, not a verified year-specific boundary for every event; complete a focused external-boundary history check for the selected borough before freezing its dataset. Ward reviews alone do not establish a change to the borough's external boundary; see [R15–R16](references.md#r15).

### Reproduce the ignored inputs

Original data and derived exports are excluded from Git, so cloning the repository does not supply them. Use preserved inputs matching the manifest checksums for exact-input reproduction; the manifest records completed acquisitions, not instructions to overwrite their metadata. Published URLs can serve revised files, so investigate checksum differences rather than replacing the recorded hashes.

1. Set up the environment below, then obtain the eight annual CSVs and Excel guide using [data.md](data/data.md) and place them in `data/`.
2. Obtain the GeoPackage through the [official boundary download](https://open-geography-portalx-ons.hub.arcgis.com/api/download/v1/items/a4d56f9755be48b0a78c120e499fa9df/geoPackage?layers=0), preserving it as `data/ons-lad-december-2024-uk-bfe.gpkg` alongside the supplied manifest.
3. Run notebook 01 from `notebooks/` to verify its source inputs and generate collision candidates and the preparation log.
4. Run notebook 02 to verify the boundary/guide and audit spatial membership, using a new validation-output directory if current results need exporting separately.

The acquisition script is for initial acquisition and refuses an existing boundary manifest entry, including the one supplied in this repository. For a clone with that entry, download the boundary file directly as above; no manifest reset is required. The final submission's input-packaging arrangements remain to be confirmed.

## Environment and execution

Use Python 3.12; local setup was checked with Python 3.12.3. `requirements.txt` pins the direct dependencies used by the two notebooks. Transitive dependencies are not locked. The repository-root `.venv` contains the installed spatial packages, whose versions match the saved validation run; the installed NumPy version is also pinned.

To reproduce the setup on Ubuntu/WSL, start from the repository root. Create the environment only if it does not already exist:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m ipykernel install --sys-prefix --name london-pedestrian-collision-analysis --display-name "Python (London pedestrian collisions)"
```

The kernel is registered inside the selected environment, so launch JupyterLab using that environment. Its generated local kernel configuration is ignored with `.venv/`; it is not a portable file to commit. On Windows or macOS, use Python 3.12 and the activation command appropriate to that environment, then run the same `python -m` installation and registration commands.

With the environment active, launch JupyterLab:

```bash
cd notebooks
python -m jupyterlab
```

Select **Python (London pedestrian collisions)** as the notebook kernel. In a notebook editor that discovers Python environments directly, select the repository’s `.venv` interpreter if the display name is unavailable.

Open the required notebook, restart the kernel and run its cells in order after checking the input/output parameters. Notebook 01 replaces its two named derived CSVs, while notebook 02 protects existing validation exports; raw inputs remain unchanged. The same project files work on Windows, macOS and Linux with an appropriate Python environment; no WSL-specific paths are required.

Notebook 01 reads selected fields one annual file or collision/casualty pair at a time. Task 1 profiles the inputs and performs a shared pedestrian selection for EDA and preparation; Task 2 adds quality flags and writes the two derived exports. All 14 code cells now have saved execution counts in sequence, and the findings reflect their outputs; a fresh-kernel run is not established by execution counts alone.

## Version control

The current ignore rules exclude raw downloads in `data/`, `.venv/`, personal student files and local coursework reference material. `data/data.md` and `data/download-manifest.json` are explicitly available for version control. Root documentation, dependency configuration and `notebooks/` are available for version control. Review the intended file list before staging or publishing.
