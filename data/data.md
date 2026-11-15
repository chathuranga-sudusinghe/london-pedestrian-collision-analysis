# Data sources and provenance

## Study scope

See the [README research framework](../README.md#research-framework) for the research questions, collision-counting definition, study scope and links to the adopted methods.

## Official source and coverage

[Department for Transport (DfT): Road safety open data](https://www.gov.uk/government/statistical-data-sets/road-safety-open-data). Source page checked on 11 November 2026.

The source covers police-reported personal injury collisions on public roads in Great Britain. It does not represent every collision or every pedestrian injury. The DfT page identifies 2025 as the latest full year of final validated data; the approved 2022–2025 period still requires explicit reporting-comparability limitations alongside record-level completeness checks.

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

Originals remain unchanged and derived outputs are stored separately with preparation flags and a log. The original December 2024 ONS UK BFE boundary GeoPackage is preserved; notebook 02 records geometry validation, without establishing historically identical boundaries.

## Verification status

**Completed:** file-presence checks, initial download-size and CSV-header checks, Excel archive-integrity checks, and copy verification. The nine downloaded files matched their manifest checksums during preservation; all ten copied files matched their source copies. These checks do not validate the records.

**Saved inspection results:** the merged notebook reports stable within-type schemas and no blank candidate-key components, within-file duplicate keys or record-year mismatches. Each year spans 1 January–31 December with all 12 months represented and no invalid collision dates. These checks describe the supplied records, not complete reporting or verified geographic accuracy.

**Saved selection and export results:** the merged notebook reports 74,682 national candidates, including 17,596 recorded-London and 17 separately flagged Heathrow-coded events. London annual counts are 4,383 / 4,392 / 4,299 / 4,522 for 2022–2025. Key, pooled-uniqueness, year, join and pedestrian-code safeguards pass without reported discrepancies.

**Saved London quality results:** the evaluated date, ID-composition, district and grid/longitude-latitude range flags are zero for the recorded-London subset. Its repeated-grid flags affect 16 records within years and 66 in the pooled-national comparison, with all events retained. These counts describe flagged records rather than distinct location pairs and do not establish positional accuracy.

**Remaining spatial checks:** preparation-stage spatial flags remain `not_checked`; notebook 02 supplies later London membership evidence. Coordinate-representation agreement remains unperformed because the geographic datum is unresolved. See [methods and limitations](../docs/methods-and-validation.md#validation-scope-and-outstanding-limitations) for subsequent analytical decisions and outstanding issues.

## Preparation rules and derived candidates

The cleaning rules and audit are in Task 2 of [01_data_understanding_preparation.ipynb](../notebooks/01_data_understanding_preparation.ipynb); the saved export reports completion.

Raw fields are retained alongside numeric/date representations and quality flags, without filling missing values or deleting repeated locations. Optional attributes never determine collision eligibility.

Recorded London codes, Heathrow, blanks, the predates-code category and unrecognised codes are distinguished explicitly. National candidates remain available to investigate code/geometry disagreement. `local_authority_district = -1` means Code deprecated, not ordinary missingness.

[DfT methodology](https://www.gov.uk/government/statistics/matching-stats19-collision-data-to-a-road-network-feasibility/matching-stats19-collisions-to-a-road-network-feasibility) and the [government CRS register](https://www.gov.uk/government/publications/uk-geospatial-data-standards-register/national-geospatial-data-standards-register) support British National Grid / EPSG:27700 for grid coordinates, with the DfT methodology page checked on 14 November 2026 and the CRS register on 13 November 2026. This documentary reference does not validate individual points. The supplied guide does not specify the longitude/latitude datum, so cross-representation checks remain pending.

The saved merged-notebook export reports 74,682 rows and the candidate CSV has 38 columns. Both `data/derived/pedestrian_collision_candidates.csv` and `data/derived/preparation_log.csv` exist and remain ignored by Git. The documented boundary checks and Python maps support geographic validation; browser inspection provides supplementary evidence.

## Boundary input

The [ONS December 2024 UK BFE district boundaries](../docs/references.md#r05) are used for spatial membership checks and the fixed Croydon footprint. The preserved file contains layer `LAD_DEC_24_UK_BFE`, a MULTIPOLYGON geometry column, EPSG:27700 metadata and 361 UK features, including 33 unique London district codes. The saved spatial-validation run passes polygon-validity and guide-code reconciliation checks; historically identical boundaries are not established or assumed.

Full-resolution allocation and licensing guidance are recorded in the [reference register](../docs/references.md#r04).

The prepared [boundary acquisition script](../scripts/download_boundaries.py) downloads the original GeoPackage and appends its retrieval metadata, SHA-256 and initial format checks to the manifest. Its completed download is 163,885,056 bytes, and a read-only local check confirms the manifest size and SHA-256. The script records the ONS licence reference; confirm the product-specific attribution and applicable copyright year before reproducing maps.

The manifest now records the stable download URL and resolved host/path without signed query parameters, timestamp, size, checksum, publisher, boundary vintage, licence reference and initial format checks. The boundary SHA-256 is `a421a026170391ade115e7424b8c4e06e682e0290978b827e03941b38b8e9475`. The analysis uses this vintage as fixed reference geography, without assuming identical year-specific boundaries.

## Spatial analysis and validation evidence

See [methods and validation](../docs/methods-and-validation.md#spatial-membership-validation) for the London membership audit, Croydon study frame, grid comparison, inference results and limitations. The December 2024 footprint is fixed reference geography; historically identical boundaries are not claimed. Coordinate-representation agreement remains unperformed.

## Attribution and reuse

Cite the DfT source page, the relevant files, the data guide and the access date in the report. The source page links to the [Open Government Licence v3.0](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/); check applicable dataset terms and attribution before redistributing inputs. Boundary data will need their own source and licence record.

Acquisition-time `not_checked` fields in the manifest describe the download stage; notebook 02 provides the later geometry and code-reconciliation evidence. Reproduction of ignored inputs is described in the [reproduction guide](../docs/reproduction.md#reproduce-the-ignored-inputs).

## Supplementary browser inspection

The [methods document](../docs/methods-and-validation.md#supplementary-map-inspection) records browser inspection and notebook 02's saved example maps. The previously documented eight screenshots are unavailable in this working copy; their location remains unverified. They are not notebook inputs. Verify and package any genuine screenshots used in the submission.
