# London pedestrian collision analysis

COMP1890 Spatial Data Science project examining reported pedestrian injury collision concentrations in Croydon, 2022–2025.

## Research framework

**Main question:** Where are reported pedestrian injury collisions spatially concentrated within Croydon's fixed December 2024 footprint during 2022–2025?

| ID | Supporting question |
| --- | --- |
| SQ1 | How does the spatial distribution of qualifying collision counts vary across the borough? |
| SQ2 | Which local concentrations, if any, are statistically significant under the selected spatial test? |
| SQ3 | How sensitive are the identified concentrations to one alternative spatial-analysis setting? |

### Scope and status

Count each collision involving at least one injured pedestrian once, across fatal, serious and slight injuries. Membership uses the Office for National Statistics (ONS) December 2024 Croydon footprint as fixed geography; historically identical boundaries are not assumed.

The analysis compares descriptive grids, then uses a 500 m main grid and 250 m sensitivity grid with an area-based binomial neighbourhood test and Benjamini–Yekutieli correction. This is a custom inferential extension, not standard Getis–Ord Gi*. Findings describe concentration, not exposure-adjusted pedestrian risk or causality. See [methods and limitations](docs/methods-and-validation.md).

## Key saved results

- [Notebook 03](notebooks/03_croydon_grid_comparison.ipynb): 792 unique collisions; annual counts 190 / 200 / 180 / 222.
- [Notebook 04](notebooks/04_croydon_spatial_inference.ipynb): 74/415 flagged focal cells at 500 m and 276/1,520 at 250 m; flagged-area intersection-over-union is 77.9%.

Shading locates a significant neighbourhood test, rather than testing the focal cell alone. These are saved-output results under a uniform-land-area baseline; sensitivity is not independent replication.

## Quick start

Use Python 3.12 and the root `.venv`. On Ubuntu/WSL, from the repository root, create the environment only if absent:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cd notebooks
python -m jupyterlab
```

Select the project `.venv` interpreter. Original data and derived inputs are ignored by Git and must be supplied before execution. Follow [reproduction instructions](docs/reproduction.md) for downloads, notebook order, output protection and Windows/macOS environment guidance. Notebook working directory: `notebooks/`; default inputs: `../data`.

## Project structure

```text
.
├── README.md
├── AGENTS.md
├── requirements.txt
├── docs/
│   ├── methods-and-validation.md
│   ├── reproduction.md
│   └── references.md
├── evidence/                   # Selected report figure exports and source notes
├── data/
│   ├── data.md
│   ├── download-manifest.json
│   └── derived/                 # Local generated inputs and validation exports
├── notebooks/                  # Four numbered analysis notebooks
├── scripts/                    # Boundary acquisition
└── tests/                      # Synthetic grid and inference checks
```

## Documentation and checks

- [Methods and validation](docs/methods-and-validation.md): study rationale, selection, grids, inference, saved evidence and limitations.
- [Reproduction](docs/reproduction.md): environment, input acquisition, execution and synthetic tests.
- [Data sources and provenance](data/data.md): download links, definitions, checksums, preservation and reuse.
- [Reference register](docs/references.md): source details, lecture connections and adoption status.
- [Report figure evidence](evidence/README.md): opt-in map exports, source cells, caption guidance and pending checks.

From the repository root with the environment active:

```bash
python -m unittest discover -s tests -v
```

These synthetic tests do not load real datasets, execute notebook input cells or validate the spatial null. Original inputs, `.venv/`, personal files and local coursework references remain excluded from Git. Final report-map attribution, teaching alignment, reporting comparability and submission input packaging remain outstanding.
