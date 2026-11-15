"""Synthetic-only checks for notebook 04; no input cells or real datasets execute."""

import ast
from decimal import Decimal, localcontext
import json
import math
from numbers import Integral
from pathlib import Path
import unittest

import geopandas as gpd
import numpy as np
import pandas as pd
from pyproj import CRS
from shapely import box


NOTEBOOK = Path(__file__).resolve().parents[1] / "notebooks/04_croydon_spatial_inference.ipynb"
notebook = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
namespace = {"math": math, "Integral": Integral, "np": np, "pd": pd,
             "gpd": gpd, "CRS": CRS, "box": box}
for cell in notebook["cells"]:
    if cell["id"] in {"grid-functions", "inference-functions"}:
        definitions = [node for node in ast.parse("".join(cell["source"])).body
                       if isinstance(node, ast.FunctionDef)]
        exec(compile(ast.Module(body=definitions, type_ignores=[]), str(NOTEBOOK), "exec"), namespace)

binomial_log_upper_tail = namespace["binomial_log_upper_tail"]
by_adjust_log = namespace["by_adjust_log"]
neighbourhood_membership = namespace["neighbourhood_membership"]
local_count_test = namespace["local_count_test"]
summarise_inference = namespace["summarise_inference"]
compare_flagged_areas = namespace["compare_flagged_areas"]


def decimal_log_tail(observed, total, probability):
    """Independent integer-combination, high-precision probability-space oracle."""
    with localcontext() as context:
        context.prec = 90
        p = Decimal(str(probability))
        tail = sum(Decimal(math.comb(total, k)) * p ** k * (1 - p) ** (total - k)
                   for k in range(observed, total + 1))
        return float(tail.ln())


def three_cells():
    """Three disconnected windows, with one clipped cell and an observed zero."""
    geometry = [box(0, 0, 1, 1), box(3, 0, 3.5, 1), box(6, 0, 7, 1)]
    return gpd.GeoDataFrame(
        {"cell_id": ["a", "b", "c"], "grid_col": [0, 3, 6], "grid_row": [0, 0, 0],
         "collision_count": [2, 0, 0], "area_m2": [1.0, 0.5, 1.0]},
        geometry=geometry, crs="EPSG:27700",
    )


class BinomialTailTests(unittest.TestCase):
    def test_hand_calculated_upper_tail_includes_observed(self):
        # P(Binomial(4, 1/2) >= 3) = (4 + 1) / 16, not P(X > 3).
        self.assertAlmostEqual(math.exp(binomial_log_upper_tail(3, 4, 0.5)), 5 / 16)
        self.assertEqual(binomial_log_upper_tail(0, 4, 0.5), 0)
        self.assertAlmostEqual(math.exp(binomial_log_upper_tail(4, 4, 0.5)), 1 / 16)

    def test_independent_high_precision_oracle_at_study_scale(self):
        for observed, total, probability in [
            (1, 792, 0.000001), (40, 792, 0.03), (100, 792, 0.01),
            (400, 792, 0.5), (790, 792, 0.99), (792, 792, 0.000001),
        ]:
            with self.subTest(observed=observed, total=total, probability=probability):
                actual = binomial_log_upper_tail(observed, total, probability)
                expected = decimal_log_tail(observed, total, probability)
                self.assertAlmostEqual(actual, expected, delta=2e-9)

    def test_degenerate_probabilities_and_empty_trial_count(self):
        self.assertEqual(binomial_log_upper_tail(0, 0, 0), 0)
        self.assertEqual(binomial_log_upper_tail(0, 2, 0), 0)
        self.assertEqual(binomial_log_upper_tail(1, 2, 0), -math.inf)
        self.assertEqual(binomial_log_upper_tail(2, 2, 1), 0)
        self.assertTrue(math.isfinite(binomial_log_upper_tail(792, 792, 1e-6)))

    def test_invalid_counts_and_probabilities_stop(self):
        for args in [(1, -1, 0.5), (-1, 2, 0.5), (3, 2, 0.5), (1.5, 2, 0.5),
                     (1, 2.5, 0.5), (True, 2, 0.5), (1, 2, -0.1),
                     (1, 2, 1.1), (1, 2, np.nan)]:
            with self.subTest(args=args), self.assertRaises(ValueError):
                binomial_log_upper_tail(*args)


class MultipleComparisonTests(unittest.TestCase):
    def test_hand_calculated_by_adjustment_and_original_order(self):
        # m=3, H_m=11/6. Ranked p=.01,.04,.20 -> .055,.11,11/30.
        p = np.array([0.20, 0.01, 0.04])
        np.testing.assert_allclose(np.exp(by_adjust_log(np.log(p))), [11 / 30, 0.055, 0.11])

    def test_step_up_monotonicity_ties_and_cap(self):
        p = np.array([0.01, 0.011, 0.9, 0.9])
        adjusted = np.exp(by_adjust_log(np.log(p)))
        # Reverse cumulative minimum propagates rank two's smaller value.
        self.assertAlmostEqual(adjusted[0], 0.011 * 4 * (25 / 12) / 2)
        self.assertAlmostEqual(adjusted[0], adjusted[1])
        np.testing.assert_allclose(adjusted[2:], [1, 1])
        self.assertTrue((adjusted >= p).all())

    def test_extreme_logs_and_single_family(self):
        adjusted = by_adjust_log([-2000.0, -1000.0, 0.0])
        self.assertTrue(np.isfinite(adjusted).all())
        self.assertLess(adjusted[0], -1900)
        np.testing.assert_array_equal(by_adjust_log([-4.0]), [-4.0])
        for values in [[], [[-1.0]], [np.nan], [0.1], [math.inf]]:
            with self.subTest(values=values), self.assertRaises(ValueError):
                by_adjust_log(values)


class NeighbourhoodTests(unittest.TestCase):
    def test_radius_has_nine_or_thirty_seven_cells_including_self(self):
        lattice = pd.DataFrame([(i, j) for i in range(-4, 5) for j in range(-4, 5)],
                               columns=["grid_col", "grid_row"])
        centre = lattice.index[(lattice["grid_col"] == 0) & (lattice["grid_row"] == 0)][0]
        for size, expected in [(500, 9), (250, 37)]:
            with self.subTest(size=size):
                weights = neighbourhood_membership(lattice, size, 850)
                self.assertEqual(int(weights[centre].sum()), expected)
                self.assertTrue(weights.diagonal().all())
                np.testing.assert_array_equal(weights, weights.T)

    def test_exact_distance_boundary_and_no_centroid_shift(self):
        grid = three_cells()
        # First and second full-square centres are 3 units apart despite clipping.
        self.assertTrue(neighbourhood_membership(grid, 1, 3)[0, 1])
        self.assertFalse(neighbourhood_membership(grid, 1, 2.99)[0, 1])
        np.testing.assert_array_equal(neighbourhood_membership(grid, 1, 0), np.eye(3, dtype=bool))
        duplicate = pd.concat([grid, grid.iloc[[0]]], ignore_index=True)
        for frame, size, radius in [(duplicate, 1, 1), (grid, 0, 1), (grid, 1, -1),
                                    (grid, np.nan, 1), (grid.iloc[:0], 1, 1)]:
            with self.subTest(size=size, radius=radius), self.assertRaises(ValueError):
                neighbourhood_membership(frame, size, radius)


class InferenceIntegrationTests(unittest.TestCase):
    def test_unequal_area_expectations_and_zero_cells_in_family(self):
        grid = three_cells()
        original = grid.copy(deep=True)
        result = local_count_test(grid, 1, 0, 2.5)
        np.testing.assert_allclose(result["expected_neighbourhood_count"], [0.8, 0.4, 0.8])
        # First count has tail .4**2=.16; all three tests -> BY p=.88.
        self.assertAlmostEqual(result.iloc[0]["p_upper_display_floor"], 0.16)
        self.assertAlmostEqual(result.iloc[0]["p_by_display_floor"], 0.88)
        self.assertEqual(len(result), 3)
        self.assertFalse(result["by_significant"].any())
        self.assertTrue(grid.equals(original))

    def test_full_footprint_window_has_probability_one(self):
        result = local_count_test(three_cells(), 1, 100, 2.5)
        np.testing.assert_allclose(result["observed_neighbourhood_count"], [2, 2, 2])
        np.testing.assert_allclose(result["expected_neighbourhood_count"], [2, 2, 2])
        np.testing.assert_allclose(result["log_p_upper"], [0, 0, 0])
        self.assertFalse(result["by_significant"].any())

    def test_log_decision_survives_display_underflow(self):
        grid = three_cells()
        grid["collision_count"] = [792, 0, 0]
        grid.loc[0, "area_m2"] = 1e-6
        result = local_count_test(grid, 1, 0, 1.500001)
        self.assertLess(result.iloc[0]["log_p_upper"], -7000)
        self.assertTrue(result.iloc[0]["by_significant"])
        self.assertGreater(result.iloc[0]["p_upper_display_floor"], 0)

    def test_invalid_area_count_and_fdr_inputs_stop(self):
        for column, value in [("area_m2", 0), ("area_m2", -1), ("area_m2", np.nan),
                              ("collision_count", -1), ("collision_count", 0.5)]:
            grid = three_cells()
            grid[column] = grid[column].astype(float)
            grid.loc[0, column] = value
            with self.subTest(column=column, value=value), self.assertRaises(ValueError):
                local_count_test(grid, 1, 0, 2.5)
        grid = three_cells()
        for footprint, level in [(99, 0.05), (0, 0.05), (2.5, 0), (2.5, 1)]:
            with self.subTest(footprint=footprint, level=level), self.assertRaises(ValueError):
                local_count_test(grid, 1, 0, footprint, level)
        grid["collision_count"] = 0
        with self.assertRaises(ValueError):
            local_count_test(grid, 1, 0, 2.5)

    def test_area_overlap_and_events_use_focal_cells(self):
        main = three_cells()
        main["by_significant"] = [True, False, True]
        main["neighbour_count_excluding_self"] = [2, 2, 2]
        alternative = main.copy()
        alternative["by_significant"] = [True, False, False]
        overlap = compare_flagged_areas(main, alternative)
        self.assertAlmostEqual(overlap["intersection_over_union"], 0.5)
        self.assertAlmostEqual(overlap["share_main_flagged_area_reproduced"], 0.5)
        summary = summarise_inference(main, 1)
        self.assertEqual(summary["events_in_flagged_focal_cells"], 2)
        self.assertEqual(summary["flagged_focal_cells"], 2)
        main["by_significant"] = False
        alternative["by_significant"] = False
        empty = compare_flagged_areas(main, alternative)
        self.assertEqual(empty["union_km2"], 0)
        self.assertTrue(math.isnan(empty["intersection_over_union"]))
        self.assertTrue(math.isnan(empty["share_main_flagged_area_reproduced"]))
        with self.assertRaises(ValueError):
            compare_flagged_areas(main, alternative.to_crs("EPSG:4326"))


if __name__ == "__main__":
    unittest.main()
