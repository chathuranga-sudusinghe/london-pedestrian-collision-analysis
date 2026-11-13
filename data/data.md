# Data sources and provenance

## Study scope

The proposed study examines the spatial concentration of reported pedestrian injury collisions in one London borough. The borough and final study period remain undecided; 2022–2025 is the candidate period. Count each collision once when it involves at least one pedestrian casualty, including fatal, serious and slight injuries. Without pedestrian exposure or footfall data, the study describes collision concentrations rather than pedestrian risk.

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

The inspected guide defines pedestrian `casualty_class` as `3`, pedestrian `casualty_type` as `0`, and casualty severity `1`, `2` and `3` as fatal, serious and slight respectively. The notebook uses class `3` with those severity codes for inclusion and checks agreement with type `0`.

Use `collision_index` to associate casualties with collisions. Reduce qualifying casualty records to distinct collision keys before selecting collision records; multiple pedestrian casualties must not multiply the collision count. Validate key uniqueness and unmatched records before accepting the selection. Vehicle files are not part of the preserved input set.

## Input location and preservation

The original inputs are in the repository-root `data/` directory. The notebook is in `notebooks/` and uses `Path("../data")` relative to its documented working directory, `notebooks/`.

Keep the `data/` and `notebooks/` folders together when packaging the project. Alternatively, configure an external input directory using `COMP1890_DATA_DIR` or the notebook’s `DATA_DIR` setting. Do not require a particular username, repository name or absolute filesystem location.

Keep originals unchanged. Future derived datasets must be written separately, with transformations and exclusions documented. Borough boundary data have not yet been obtained or selected.

## Verification status

**Completed:** file-presence checks, initial download-size and CSV-header checks, Excel archive-integrity checks, and copy verification. The nine downloaded files matched their manifest checksums during preservation; all ten copied files matched their source copies. These checks do not validate the records.

**Pending:** execution of the prepared inspection notebook; record counts and actual date coverage; duplicate and missing keys; casualty-to-collision join coverage; coordinate completeness and validity; borough counts and geographic validation. The notebook has only received static syntax and structure checks.

**Before analysis:** confirm relevant year-to-year reporting/specification changes, select an authoritative borough boundary and coordinate reference system, agree the borough and period, and check the proposed spatial method against lecture material. Do not infer completeness from the year in a filename or from the final-release label alone.

## Attribution and reuse

Cite the DfT source page, the relevant files, the data guide and the access date in the report. The source page links to the [Open Government Licence v3.0](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/); check applicable dataset terms and attribution before redistributing inputs. Boundary data will need their own source and licence record.
