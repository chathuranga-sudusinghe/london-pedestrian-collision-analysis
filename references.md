# Reference register

This register records sources for the analysis and later PDF report; it is not a finished bibliography. **Used** means cited in the current project, **candidate** means inspected for a proposed method or input, and **background** means contextual reading. Convert used entries to the required report citation style once that style is confirmed.

Keep dataset provenance in [data/data.md](data/data.md) and completed download records in [data/download-manifest.json](data/download-manifest.json). Cite references beside the notebook method or claim they support. Do not interpret a candidate source as an implemented method or a validated result.

## Data, boundaries and coordinate systems

<a id="r01"></a>
### R01 — DfT road safety open data and supplied guide

- **Author:** Department for Transport (DfT).
- **Source:** [Road safety open data](https://www.gov.uk/government/statistical-data-sets/road-safety-open-data); annual 2022–2025 collision/casualty CSVs and the supplied 2025 Excel data guide, sheet `2024_code_list`.
- **Access:** source page checked 13 November 2026; preserved file URLs and download timestamps are in the manifest.
- **Use/status:** **used** for collision/casualty grain, eligibility and field definitions. Exact file links and cross-year comparability limitations are recorded in [data documentation](data/data.md).

<a id="r02"></a>
### R02 — STATS19 authoritative grid coordinates

- **Author/date:** Department for Transport, 24 September 2026.
- **Title:** [Matching STATS19 collisions to a road network: feasibility](https://www.gov.uk/government/statistics/matching-stats19-collision-data-to-a-road-network-feasibility/matching-stats19-collisions-to-a-road-network-feasibility).
- **Location/access:** section 3.1; accessed 14 November 2026.
- **Use/status:** **used** as documentary evidence that authoritative STATS19 coordinates use British National Grid. The report's conversion of a processing copy to WGS84 does not establish the datum of the longitude/latitude columns in the supplied CSVs or validate individual points.

<a id="r03"></a>
### R03 — British National Grid coordinate reference identifier

- **Author:** UK Government; publication date not recorded in this register.
- **Title:** [UK Geospatial Data Standards Register](https://www.gov.uk/government/publications/uk-geospatial-data-standards-register/national-geospatial-data-standards-register).
- **Location/access:** coordinate reference systems, OSGB36 / British National Grid; accessed 14 November 2026.
- **Use/status:** **used** with R02 to document EPSG:27700 for grid coordinates. This is documentary CRS evidence, not a point-accuracy check.

<a id="r04"></a>
### R04 — Boundary resolution and extent

- **Author:** Office for National Statistics (ONS); publication date not confirmed.
- **Title:** [Boundary Dataset Guidance: 2021 onwards](https://www.ons.gov.uk/file?uri=%2Faboutus%2Ftransparencyandgovernance%2Ffreedomofinformationfoi%2Fwestminsterconstituenciesforeachitl3%2Fboundarydatasetguidance2021onwards.pdf).
- **Location/access:** pages 1–4, resolution, point allocation and coastal extent; accessed 14 November 2026.
- **Use/status:** **used** to plan full-resolution point-in-polygon allocation and distinguish analysis boundaries from generalised display boundaries. Vintage compatibility, geometry validity and coverage must still be inspected for the chosen input.

<a id="r05"></a>
### R05 — Candidate December 2024 district boundaries

- **Author/vintage:** Office for National Statistics; boundaries as at December 2024.
- **Title:** [Local Authority Districts (December 2024) Boundaries UK BFE](https://www.data.gov.uk/dataset/5d392106-7cb3-4214-90ac-4b46f16f0db3/local-authority-districts-december-2024-boundaries-uk-bfe).
- **Metadata:** [official feature layer](https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Local_Authority_Districts_December_2024_Boundaries_UK_BFE/FeatureServer/0) and [ONS item](https://www.arcgis.com/home/item.html?id=a4d56f9755be48b0a78c120e499fa9df).
- **Access:** metadata and count-only query inspected, followed by local-file verification, on 14 November 2026; the preserved download timestamp and checksum are in the manifest.
- **Use/status:** **candidate** for membership validation. The preserved GeoPackage has EPSG:27700 metadata, fields `LAD24CD` and `LAD24NM`, and 33 unique London codes; notebook 02 records passing polygon-validity and guide-reconciliation checks, while suitability across 2022–2025 remains unresolved.

<a id="r06"></a>
### R06 — Boundary licensing and attribution

- **Author/date:** Office for National Statistics; page last updated 26 April 2022.
- **Title:** [Licences](https://www.ons.gov.uk/methodology/geography/licences).
- **Location/access:** digital boundaries and reference maps; accessed 14 November 2026.
- **Use/status:** **used** for planned boundary attribution. ONS specifies Open Government Licence v3.0 accreditation and an OS copyright/database-right statement; retain the applicable year from the selected product rather than guessing it.

## Spatial validation and implementation

<a id="r07"></a>
### R07 — Point interiors and boundary cases

- **Author:** Shapely contributors; rolling software documentation.
- **Title:** [shapely.within](https://shapely.readthedocs.io/en/stable/reference/shapely.within.html).
- **Location/access:** predicate definition and polygon-boundary example; accessed 14 November 2026.
- **Use/status:** **used** implementation reference for distinguishing strict interior membership from boundary intersections. A point on a polygon boundary is not within its interior; unmatched, boundary and multiple matches need separate audit categories.

<a id="r08"></a>
### R08 — Coordinate transformations and available operations

- **Author:** pyproj contributors; rolling software documentation.
- **Title:** [Transformer](https://pyproj4.github.io/pyproj/stable/api/transformer.html).
- **Location/access:** `Transformer`, `TransformerGroup`, unavailable operations and transformation-grid controls; accessed 14 November 2026.
- **Use/status:** **candidate** implementation reference for logging transformation choice and missing grids. Confirm the geographic source datum first, and justify any agreement tolerance using coordinate precision and transformation accuracy alongside observed offsets.

## Lecture alignment and spatial visualisation

The supplied slide text and hyperlinks were inspected on 14 November 2026; image-only content was not interpreted. Lecturer names and teaching dates are not confirmed, so verify them from the original material before constructing final citations. Local lecture files are reference material, are excluded from Git and are not runtime dependencies.

<a id="r09"></a>
### R09 — Spatial relationships and London geography lectures

- **Source/type:** COMP1890 lecture slides; author and teaching date to confirm.
- **Material:** `Spatial Data & Spatial Relationships.pptx`, slides 15–22; `UK Geography.pptx`, slides 9 and 19.
- **Use/status:** **used** for topological relationships, interior/boundary distinctions, 32 boroughs plus separate City of London, and the taught QGIS mapping context.
- **Availability:** supplied locally in `COMP1890_Spatial_Data_Science/COMP1890 Lecture notes/`; not supplied through this repository.

<a id="r10"></a>
### R10 — Spatial visualisation lecture

- **Source/type:** COMP1890 `Spatial Visualization.pptx`; author and teaching date to confirm.
- **Location:** slides 8–18, map design, visual variables, categorized/graduated symbols and classification; slide 20, linked traffic-collision exercise.
- **Use/status:** **used** to guide map design. Symbol size can communicate count magnitude, while categories can distinguish validation cases; classification and legends must match the mapped quantity.
- **Availability:** supplied locally alongside R09; the duplicate `(1)` deck is not a separate reference.

<a id="r11"></a>
### R11 — Lecture-linked QGIS collision exercise

- **Source:** Carleton University CUOSGwiki; page author and publication date not confirmed.
- **Title:** [Analysing Traffic Accidents Using QGIS — Heatmaps, Hotspot Analysis, and the Time Controller Panel](https://dges.carleton.ca/CUOSGwiki/index.php/Analysing_Traffic_Accidents_Using_QGIS_-_Heatmaps,_Hotspot_Analysis,_and_the_Time_Controller_Panel).
- **Access/connection:** accessed 14 November 2026; linked from R10 slide 20.
- **Use/status:** **background** for grid aggregation, mapping and sensitivity to settings. Its Ottawa settings and historical plugin installation instructions are not adopted for this project; a visual heatmap is not a statistical significance result.

<a id="r12"></a>
### R12 — Autocorrelation lectures and linked clustering exercise

- **Lecture material:** COMP1890 `Spatial Data Science - 2.pptx`, slides 21–24 and 29; `Spatial Data Science - 6.pptx`, slide 19; lecturer and teaching dates to confirm.
- **Linked title:** [Week 4 — Analysis of spatial clustering](https://hughst.github.io/week-4/), Spatial epidemiology in R; page author and publication date not confirmed.
- **Location/access:** global and local spatial autocorrelation, spatial weights and permutation examples; accessed 14 November 2026.
- **Use/status:** **candidate** for later analytical-method selection, with lecture concepts already used in framing the research. The linked exercise explicitly demonstrates global Moran's I and Local Moran's I; it does not establish Getis–Ord Gi* as a required taught method.

<a id="r13"></a>
### R13 — Candidate Gi* method and multiple comparisons

- **Author:** Esri; rolling ArcGIS Pro documentation.
- **Title:** [How Hot Spot Analysis (Getis–Ord Gi*) works](https://doc.esri.com/en/arcgis-pro/latest/tool-reference/spatial-statistics/h-how-hot-spot-analysis-getis-ord-gi-spatial-stati.html).
- **Location/access:** local neighbourhood sums, significance and false discovery rate correction; accessed 14 November 2026.
- **Use/status:** **candidate** methodological background, not evidence that Gi* has been selected or executed. Before local inference, specify the null hypothesis, weights, significance procedure and handling of multiple comparisons; add the original research reference if this method is selected.

<a id="r14"></a>
### R14 — GeoPandas installation, file reading and spatial joins

- **Author:** GeoPandas developers; rolling software documentation.
- **Sources:** [installation](https://geopandas.org/en/stable/getting_started/install.html), [read_file](https://geopandas.org/en/stable/docs/reference/api/geopandas.read_file.html) and [sjoin](https://geopandas.org/en/stable/docs/reference/api/geopandas.sjoin.html).
- **Access:** 14 November 2026; published package versions checked through the Python Package Index on the same date.
- **Use/status:** **used** for the validation notebook and dependency specification. Spatial packages are installed and recorded in the saved run; the saved nine-cell execution includes corrected highway-status summaries and a successful nine-file export with seven input hashes. The documentation is rolling, so retain the actual package versions with results.

<a id="r15"></a>
### R15 — Ward reviews and external council boundaries

- **Author:** Local Government Boundary Commission for England; rolling guidance.
- **Title:** [How reviews work](https://www.lgbce.org.uk/how-reviews-work).
- **Location/access:** electoral reviews and principal area boundary reviews; accessed 14 November 2026.
- **Use/status:** **used** to distinguish internal ward changes from changes to a council's external boundary. A ward review alone does not establish that a borough allocation polygon changed.

<a id="r16"></a>
### R16 — Official geography history and coverage limitations

- **Author:** Office for National Statistics.
- **Sources:** [Code History Database guidance](https://www.ons.gov.uk/methodology/geography/geographicalproducts/namescodesandlookups/codehistorydatabasechd), [December 2025 database metadata](https://www.data.gov.uk/dataset/4ec2169f-1a72-4c2d-be60-a74174902593/code-history-database-december-2025-for-the-uk) and [mid-2024 population estimates methods guide](https://www.ons.gov.uk/peoplepopulationandcommunity/populationandmigration/populationestimates/methodologies/populationestimatesforenglandandwalesmid2022methodsguide), section 13.
- **Access:** guidance and metadata inspected 14 November 2026; the history database itself was not downloaded or queried.
- **Use/status:** **used** to identify official history evidence and its limitations. The methods guide lists four 2023 reorganisations outside London, and the December 2025 metadata does not list London boroughs among that release's updated geography types; neither establishes that all London polygons were unchanged throughout 2022–2025. Complete a focused history check for the selected borough before final filtering; December 2024 remains a candidate fixed reference geography.
