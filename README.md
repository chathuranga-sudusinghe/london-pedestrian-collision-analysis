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

The merged notebook has saved execution results for all 14 code cells, including four EDA figures, with no saved errors. Preparation reports 74,682 national candidates, including 17,596 recorded-London and 17 Heathrow-coded collisions, without imputing values or deleting repeated locations. The final borough and period, coordinate consistency, boundary membership and hotspot method remain unresolved.

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
├── requirements.txt                  # Pinned direct dependencies
├── data/                             # Original CSVs and Excel guide (ignored)
│   ├── data.md                       # Sources, download links and verification status
│   ├── download-manifest.json        # Download provenance and checksums
│   └── derived/                      # Generated candidates and log (ignored)
├── notebooks/
│   └── 01_data_understanding_preparation.ipynb  # Inspection, EDA and preparation
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

The saved London audit reports no evaluated date, ID-composition, district-code or coordinate-range problems. It flags 16 records for within-year repeats and 66 for pooled-national repeats, retaining those events. London extent screens, grid/longitude-latitude agreement and borough membership remain `not_checked`.

Grid CRS evidence for EPSG:27700 is recorded in the merged notebook. The longitude/latitude datum and spatial consistency still need verification before final analysis.

## Environment and execution

Use Python 3.12; local setup was checked with Python 3.12.3. `requirements.txt` pins the installed direct dependencies. Transitive dependencies are not locked. The existing repository-root `.venv` contains the required packages and the project kernel.

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

Open `01_data_understanding_preparation.ipynb`, restart the kernel and run all cells in order after checking the input/output parameters. Task 2 replaces only the two named derived CSVs; raw inputs remain unchanged. The same project files work on Windows, macOS and Linux with an appropriate Python environment; no WSL-specific paths are required.

The notebook reads selected fields one annual file or collision/casualty pair at a time. Task 1 profiles the inputs and performs a shared pedestrian selection for EDA and preparation; Task 2 adds quality flags and writes the two derived exports. All 14 code cells now have saved execution counts in sequence, and the findings reflect their outputs; a fresh-kernel run is not established by execution counts alone.

## Version control

The current ignore rules exclude raw downloads in `data/`, `.venv/`, personal student files and local coursework reference material. `data/data.md` and `data/download-manifest.json` are explicitly available for version control. Root documentation, dependency configuration and `notebooks/` are available for version control. Review the intended file list before staging or publishing.
