# London pedestrian collision analysis

COMP1890 Spatial Data Science project investigating the spatial concentration of reported pedestrian injury collisions in one London borough.

## Scope and status

The borough and final study period remain undecided; 2022–2025 is the candidate period. Count each collision involving at least one pedestrian casualty once, including fatal, serious and slight injuries. Without pedestrian exposure data, counts describe reported collision concentrations rather than pedestrian risk.

Grid-based Getis–Ord Gi* analysis with a small sensitivity check remains provisional, pending lecture alignment and data inspection. No predictive model training is planned.

The initial inspection notebook is prepared but unexecuted. Record counts, joins, coordinate quality and borough comparisons have not been validated. Confirm module-specific AI guidance before further implementation.

## Project structure

```text
.
├── AGENTS.md                         # Project working instructions
├── README.md                         # Project overview and execution instructions
├── requirements.txt                  # Pinned direct dependencies
├── data/                             # Original CSVs and Excel guide (ignored)
│   ├── data.md                       # Sources, download links and verification status
│   └── download-manifest.json        # Download provenance and checksums
├── notebooks/
│   └── 01_data_inspection.ipynb       # Initial quality and study-scope checks
└── COMP1890_Spatial_Data_Science/     # Local coursework reference material
```

Add scripts, derived outputs, figures and report folders only when needed. The local reference folder is not a runtime dependency.

## Data

See [data.md](data/data.md) for download links, definitions, provenance and outstanding checks. Keep the eight annual collision/casualty CSVs, Excel guide and `download-manifest.json` in `data/`. Preserve originals and write any future derived data separately.

The notebook expects its working directory to be `notebooks/` and defaults to `../data`. Set `DATA_DIR` or `COMP1890_DATA_DIR` to use another input location. Paths do not depend on a particular repository name or absolute location.

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

Open `01_data_inspection.ipynb`, check the input directory, and run cells in order. The same project files work on Windows, macOS and Linux with an appropriate Python environment; no WSL-specific paths are required.

Loading all eight CSVs into memory uses more RAM than their approximately 116 MiB disk size. The notebook displays tables without modifying original files or writing derived datasets. Save the notebook after reviewing actual outputs. Execution remains pending; only static notebook checks have passed.

## Version control

The current ignore rules exclude raw downloads in `data/`, `.venv/`, personal student files and local coursework reference material. `data/data.md` and `data/download-manifest.json` are explicitly available for version control. Root documentation, dependency configuration and `notebooks/` are available for version control. Review the intended file list before staging or publishing.
