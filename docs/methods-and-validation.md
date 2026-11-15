# Methods and validation

This document explains the analysis and its saved evidence. See the [project overview](../README.md#research-framework), [reproduction guide](reproduction.md), [data provenance](../data/data.md) and [reference register](references.md). Saved outputs are not an independent real-data rerun; execution counts alone do not establish a fresh-kernel run.

## Study frame and rationale

The study includes qualifying 2022–2025 collisions strictly inside Croydon's ONS December 2024 footprint (E09000008), using British National Grid coordinates, EPSG:27700. This is a fixed-footprint study, without a claim of identical historical boundaries.

Croydon was selected purposively for research relevance and feasibility, before local significance calculation. Its Local Plan recognises varied local character ([R18](references.md#r18)); this qualitative context does not measure land use or establish a cause of collisions. Westminster and Lambeth remain defensible alternatives. Croydon is not claimed to represent London, and the supplied records do not capture every injury collision.

The four supplied annual input pairs support a pooled spatial study. Annual totals are retained rather than interpreted as causal trends. The gradual transition to the 2024 STATS19 specification remains a reporting-comparability limitation ([R19](references.md#r19)); serious/slight reclassification alone does not change eligibility when all injury severities are included.

## Preparation and selection

[Notebook 01](../notebooks/01_data_understanding_preparation.ipynb) inspects source schemas, identifiers, dates, joins and pedestrian eligibility, then adds quality flags and exports national candidates. Distinct collision keys prevent multiple pedestrian casualties from multiplying event counts. No missing-value imputation or deletion of repeated locations is performed; optional attributes do not determine eligibility. See [selection rules and checks](../data/data.md#file-purpose-and-record-selection).

The saved export contains 74,682 national candidates, including 17,596 recorded-London and 17 separately flagged Heathrow-coded events. These are candidates for spatial validation, not a final borough dataset. Preparation-stage spatial flags remain historical `not_checked` values; later validation supplies the geographic evidence without rewriting that history.

## Spatial membership validation

[Notebook 02](../notebooks/02_spatial_validation.ipynb) checks all 33 London district codes against the guide, polygon validity and positive-area overlaps. It separates strict interior membership (`within`) from boundary intersections, multiple matches and unmatched cases. Ambiguous records are retained for audit rather than assigned to a nearest polygon. Full-resolution allocation and predicate references are [R04](references.md#r04), [R07](references.md#r07) and [R09](references.md#r09).

Saved outputs report passing polygon-validity and district-reconciliation checks, no positive-area overlaps and 17,613 unique London interior memberships. The 199 recorded/geometric differences comprise 182 London district differences and 17 Heathrow-coded events inside Hillingdon.

The 182 London differences occur between shared-edge borough pairs, approximately 0.015–42.66 m from their recorded polygons. All current highway codes agree with geometric membership and all original highway codes differ. The current field is location-derived, so this is consistency evidence, not independent positional validation. Diagnostics use hash-verified annual source fields and validated joins; no distance cutoff, correction or exclusion is applied.

Nine validation outputs are documented in `data/derived/spatial_validation_closure/`, including the audit, borough evidence, district-difference diagnostics and `validation_run.json`. The metadata records seven input hashes: boundary, guide, candidates and four annual collision files. Earlier six-file exports in `data/derived/spatial_validation/` remain protected. Matching input hashes do not independently verify unchanged code, settings or artifact contents.

### Supplementary map inspection

Notebook 02 contains London context/diagnostic maps and fixed 50 m-wide views of two examples. Circle areas represent counts, while B-prefixed identifiers locate boroughs using a separate key. Callouts may obscure individual points; the audit and example views retain inspectable detail.

Mapshaper inspection of 33 boundary polygons and 17,613 validation points checked rendering and attributes for two records: `2022010376283` (matching Lambeth) and `2022010354125` (recorded Westminster, geometric Brent). Their distances to the recorded polygon are 0 m and approximately 2.16 m; zero denotes an interior point's polygon distance, not boundary distance. These examples do not establish ground-truth accuracy or validate every disagreement.

The previously documented eight browser screenshots are unavailable in this working copy; their location remains unverified. They are not notebook dependencies. Verify and package any genuine screenshots used in the submission. No QGIS inspection was performed or is required by the chosen Python workflow ([R17](references.md#r17)).

## Croydon selection and descriptive grids

[Notebook 03](../notebooks/03_croydon_grid_comparison.ipynb) independently reconciles source fields against candidates and saved validation evidence, verifies interior membership and retains recorded-code differences. Saved selection gives 792 unique collisions: 190 / 200 / 180 / 222 in 2022–2025. One event recorded elsewhere is inside the footprint in 2022; two recorded-Croydon events are outside in 2025. Recorded-Croydon totals therefore differ from fixed-footprint totals.

All grids use the British National Grid origin (0, 0), floor-based half-open assignment and every positive-area footprint intersection, including zero-count cells. Each event is assigned exactly once, and clipped areas reconcile with the footprint. The 100 m and 250 m grids each nest within 500 m, but not within one another.

| Cell size | Retained cells | Zero-count share | Partial-cell share | Events in partial cells |
| --- | ---: | ---: | ---: | ---: |
| 100 m | 9,006 | 94.1% | 7.9% | 20 |
| 250 m | 1,520 | 76.9% | 18.0% | 41 |
| 500 m | 415 | 55.4% | 30.8% | 74 |

Each grid counts all 792 events. Coarser aggregation reduces sparsity and spatial detail while increasing boundary-cell involvement. Shared raw-count map scales make fine-grid variation less visible; counts in unequal cells do not estimate exposure-adjusted risk. Clipped area is geometric support, not pedestrian exposure. Notebook 03 is descriptive; notebook 04 implements the subsequent approved design.

## Croydon spatial inference

[Notebook 04](../notebooks/04_croydon_spatial_inference.ipynb) uses a 500 m main grid and one 250 m sensitivity grid. Binary neighbourhood membership includes retained full-square centres within 850 m of a focal centre, including itself. Interior windows contain nine cells (2.25 km²) at 500 m and 37 cells (2.3125 km²) at 250 m. The common exploratory distance does not imply identical window shapes, centres or multiplicity.

Conditional on the selected total N, the null places events independently and uniformly within the fixed footprint. A specified neighbourhood's clipped area share a gives S ~ Binomial(N, a). Direct one-sided tails P(S ≥ observed) are calculated in log space. Benjamini–Yekutieli (BY) correction controls the false discovery rate at 5% separately across every retained cell of each grid, including zeros ([R20](references.md#r20), [R21](references.md#r21)). Decisions use unfloored log probabilities; probability display columns have a labelled floor. No Monte Carlo simulation, shuffled-count permutation or predictive fitting is used.

This is a custom area-based neighbourhood count test, not standard Getis–Ord Gi*. A shaded focal cell locates a neighbourhood test rather than testing that cell alone. Zero-count focal cells can legitimately be flagged. Event and area summaries use flagged focal cells, not sums or unions of overlapping test neighbourhoods.

| Saved result | 500 m main | 250 m sensitivity |
| --- | ---: | ---: |
| Flagged focal cells | 74 / 415 | 276 / 1,520 |
| Flagged focal area (km²) | 17.39 | 16.69 |
| Events in flagged focal cells | 495 | 459 |
| Top neighbourhood observed / expected | 110 / 20.60923 | 122 / 21.181709 |
| Top observed/expected ratio | 5.34 | 5.76 |

Flagged focal areas overlap by 14.93 km², with a 19.16 km² union, 77.9% intersection-over-union and 85.8% of main flagged area reproduced at 250 m. No pass/fail overlap threshold is imposed; zero-denominator ratios remain missing. Maps show broadly consistent northern concentration and a larger southern outlying patch at 500 m. Sensitivity is not independent replication; separate BY families do not establish joint control across grids.

## Validation scope and outstanding limitations

The existing 21 synthetic tests extract pure notebook function definitions without running input cells. They check grid assignment, clipping, zeros, neighbourhood geometry, binomial tails against hand calculations and a high-precision oracle, BY adjustment, numerical underflow and focal-area overlap. They do not verify source provenance, calibrate the entire pipeline under simulation, validate the spatial null or establish map readability. See [test instructions](reproduction.md#synthetic-checks).

- Uniform land area does not model roads, junctions, pedestrian exposure, reporting differences or event dependence. BY cannot repair invalid null assumptions. Results are concentration relative to that benchmark, not risk, safety or causality.
- Boundary windows exclude events outside the footprint. Grid sensitivity changes window geometry, test locations and multiplicity; more flagged cells do not establish a better grid.
- Longitude/latitude agreement remains unperformed because the supplied geographic datum is unresolved. Authoritative grid coordinates are used; documentary CRS evidence does not validate individual point locations ([R02–R03](references.md#r02)).
- Historical polygon identity is not claimed. Ward changes do not establish external borough changes ([R15–R16](references.md#r15)).
- Reporting comparability, the custom extension's acceptance under the taught-method requirement, final product-specific map attribution and final input packaging remain outstanding. Lecture links teach relevant spatial concepts and Moran methods, not this exact test; adding a statistic does not itself resolve alignment.
- Final figures and captions must identify the source, quantity, period, coordinate reference system and interpretation limits. Product-specific ONS/OS attribution must be verified before report reuse ([R06](references.md#r06)).
