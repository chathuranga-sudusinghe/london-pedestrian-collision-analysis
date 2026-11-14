# Data sources and provenance

## Study scope

See the [README research framework](../README.md#research-framework) for the research questions, collision-counting definition, study scope and provisional decisions.

## Official source and coverage

[Department for Transport (DfT): Road safety open data](https://www.gov.uk/government/statistical-data-sets/road-safety-open-data). Source page checked on 13 November 2026.

The source covers police-reported personal injury collisions on public roads in Great Britain. It does not represent every collision or every pedestrian injury. The DfT page identifies 2025 as the latest full year of final validated data; the candidate period still requires record-level completeness and comparability checks.

## Downloads

These links reproduce the URLs recorded in the preserved download manifest. Filenames are shown as link labels. The original download timestamps are 13 November 2026 (UTC). Download URLs may later serve revised files; retain the manifest and verify checksums when reproducing this input version.

| Year | Collision records | Casualty records |
| --- | --- | --- |
| 2022 | [dft-road-casualty-statistics-collision-2022.csv](https://data.dft.gov.uk/road-accidents-safety-data/dft-road-casualty-statistics-collision-2022.csv) | [dft-road-casualty-statistics-casualty-2022.csv](https://data.dft.gov.uk/road-accidents-safety-data/dft-road-casualty-statistics-casualty-2022.csv) |
| 2023 | [dft-road-casualty-statistics-collision-2023.csv](https://data.dft.gov.uk/road-accidents-safety-data/dft-road-casualty-statistics-collision-2023.csv) | [dft-road-casualty-statistics-casualty-2023.csv](https://data.dft.gov.uk/road-accidents-safety-data/dft-road-casualty-statistics-casualty-2023.csv) |
| 2024 | [dft-road-casualty-statistics-collision-2024.csv](https://data.dft.gov.uk/road-accidents-safety-data/dft-road-casualty-statistics-collision-2024.csv) | [dft-road-casualty-statistics-casualty-2024.csv](https://data.dft.gov.uk/road-accidents-safety-data/dft-road-casualty-statistics-casualty-2024.csv) |
| 2025 | [dft-road-casualty-statistics-collision-2025.csv](https://data.dft.gov.uk/road-accidents-safety-data/dft-road-casualty-statistics-collision-2025.csv) | [dft-road-casualty-statistics-casualty-2025.csv](https://data.dft.gov.uk/road-accidents-safety-data/dft-road-casualty-statistics-casualty-2025.csv) |

Data dictionary: [dft-road-casualty-statistics-road-safety-open-dataset-data-guide-2025.xlsx](https://assets.publishing.service.gov.uk/media/6ab2a71d997a4b2950cced58/dft-road-casualty-statistics-road-safety-open-dataset-data-guide-2025.xlsx).

Preserve the eight CSVs, the Excel guide and `download-manifest.json` together. The manifest records each downloaded file’s source URL, byte size, SHA-256 checksum, download timestamp and initial format checks. It is locally created provenance metadata, not a DfT download.

## File purpose and record selection

- **Collision files:** collision-level identifiers, dates, reported geography and coordinates.
- **Casualty files:** individual casualty records used to identify pedestrian involvement.
- **Excel guide:** coded-field meanings and notes. Its code-list sheet is named `2024_code_list`, despite the workbook’s 2025 filename; check applicability across the study years.

The inspected guide defines pedestrian `casualty_class` as `3`, pedestrian `casualty_type` as `0`, and casualty severity `1`, `2` and `3` as fatal, serious and slight respectively. The selection rule uses class `3` with those severity codes and checks agreement with type `0`. The latest saved run reports no class/type disagreements or unknown pedestrian severities for 2022–2025.

Use `collision_index` to associate casualties with collisions. Reduce qualifying casualty records to distinct collision keys before selecting collision records; multiple pedestrian casualties must not multiply the collision count. Validate key uniqueness and unmatched records before accepting the selection. Vehicle files are not part of the preserved input set.

## Input location and preservation

The original inputs are in the repository-root `data/` directory. The notebook is in `notebooks/` and uses `Path("../data")` relative to its documented working directory, `notebooks/`.

Keep the `data/` and `notebooks/` folders together when packaging the project. Alternatively, configure an external input directory using `COMP1890_DATA_DIR` or the notebook’s `DATA_DIR` setting. Do not require a particular username, repository name or absolute filesystem location.

Originals remain unchanged and derived outputs are stored separately with preparation flags and a log. Borough boundary data have not yet been obtained or selected.

## Verification status

**Completed:** file-presence checks, initial download-size and CSV-header checks, Excel archive-integrity checks, and copy verification. The nine downloaded files matched their manifest checksums during preservation; all ten copied files matched their source copies. These checks do not validate the records.

**Saved inspection results:** the merged notebook reports stable within-type schemas and no blank candidate-key components, within-file duplicate keys or record-year mismatches. Each year spans 1 January–31 December with all 12 months represented and no invalid collision dates. These checks describe the supplied records, not complete reporting or verified geographic accuracy.

**Saved selection and export results:** the merged notebook reports 74,682 national candidates, including 17,596 recorded-London and 17 separately flagged Heathrow-coded events. London annual counts are 4,383 / 4,392 / 4,299 / 4,522 for 2022–2025. Key, pooled-uniqueness, year, join and pedestrian-code safeguards pass without reported discrepancies.

**Saved London quality results:** the evaluated date, ID-composition, district and grid/longitude-latitude range flags are zero for the recorded-London subset. Its repeated-grid flags affect 16 records within years and 66 in the pooled-national comparison, with all events retained. These counts describe flagged records rather than distinct location pairs and do not establish positional accuracy.

**Remaining spatial checks:** London extents, coordinate-representation agreement and borough membership remain `not_checked`. The final borough, period and boundary vintage must be agreed before final spatial filtering. The final hotspot method must align with lecture material.

## Preparation rules and derived candidates

The cleaning rules and audit are now in Task 2 of [01_data_understanding_preparation.ipynb](../notebooks/01_data_understanding_preparation.ipynb). All 14 code cells have saved execution counts in sequence with no saved errors, and the export cell reports completion.

Raw fields are retained alongside numeric/date representations and quality flags, without filling missing values or deleting repeated locations. Optional attributes never determine collision eligibility.

Recorded London codes, Heathrow, blanks, the predates-code category and unrecognised codes are distinguished explicitly. National candidates remain available to investigate code/geometry disagreement. `local_authority_district = -1` means Code deprecated, not ordinary missingness.

[DfT methodology](https://www.gov.uk/government/statistics/matching-stats19-collision-data-to-a-road-network-feasibility/matching-stats19-collisions-to-a-road-network-feasibility) and the [government CRS register](https://www.gov.uk/government/publications/uk-geospatial-data-standards-register/national-geospatial-data-standards-register) support British National Grid / EPSG:27700 for grid coordinates, with sources checked on 14 November 2026. This documentary reference does not validate individual points. The supplied guide does not specify the longitude/latitude datum, so cross-representation checks remain pending.

The saved merged-notebook export reports 74,682 rows and the candidate CSV has 38 columns. Both `data/derived/pedestrian_collision_candidates.csv` and `data/derived/preparation_log.csv` exist and remain ignored by Git. QGIS and authoritative boundaries will support final geographic validation before submission.

## Attribution and reuse

Cite the DfT source page, the relevant files, the data guide and the access date in the report. The source page links to the [Open Government Licence v3.0](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/); check applicable dataset terms and attribution before redistributing inputs. Boundary data will need their own source and licence record.
