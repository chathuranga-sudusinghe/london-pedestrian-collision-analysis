"""Synthetic tests for notebook 03's pure grid functions; no data loading or exports."""

import ast
import json
from pathlib import Path
import unittest

import geopandas as gpd
import numpy as np
import pandas as pd
from pyproj import CRS
from shapely import box
from shapely.geometry import MultiPolygon, Point, Polygon


# Extract only function definitions: never execute notebook input/processing cells.
NOTEBOOK = Path(__file__).resolve().parents[1] / "notebooks" / "03_croydon_grid_comparison.ipynb"
notebook = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
source = "".join(next(c for c in notebook["cells"] if c["id"] == "grid-functions")["source"])
functions = [node for node in ast.parse(source).body if isinstance(node, ast.FunctionDef)]
namespace = {"np": np, "pd": pd, "gpd": gpd, "box": box, "CRS": CRS}
exec(compile(ast.Module(body=functions, type_ignores=[]), str(NOTEBOOK), "exec"), namespace)
build_count_grid = namespace["build_count_grid"]
summarise_grid = namespace["summarise_grid"]


def points_at(coordinates):
    return gpd.GeoDataFrame(
        {"collision_index": [f"event-{i}" for i in range(len(coordinates))]},
        geometry=[Point(x, y) for x, y in coordinates], crs="EPSG:27700",
    )


class GridComparisonTests(unittest.TestCase):
    def test_internal_edges_count_once_and_zero_cells_remain(self):
        points = points_at([(0.25, 0.25), (1, 0.25), (1, 1), (1.75, 1.75)])
        original = points.copy(deep=True)
        grid, assigned = build_count_grid(points, box(0, 0, 2, 2), 1)
        counts = grid.set_index(["grid_col", "grid_row"])["collision_count"].to_dict()
        self.assertEqual(counts, {(0, 0): 1, (0, 1): 0, (1, 0): 1, (1, 1): 2})
        self.assertEqual(assigned.set_index("collision_index").loc["event-2", ["grid_col", "grid_row"]].tolist(), [1, 1])
        self.assertEqual(len(assigned), 4)
        self.assertTrue(assigned["collision_index"].is_unique)
        self.assertFalse(grid["partial_cell"].any())
        self.assertTrue(grid["cell_id"].is_unique)
        self.assertTrue(points.equals(original))

    def test_partial_cells_preserve_events_centroid_rule_would_lose(self):
        triangle = Polygon([(0, 0), (2, 0), (0, 2)])
        grid, _ = build_count_grid(points_at([(0.25, 0.25), (1.1, 0.25)]), triangle, 1)
        indexed = grid.set_index(["grid_col", "grid_row"])
        self.assertEqual(len(grid), 3)  # The fourth square touches only at a point.
        self.assertAlmostEqual(grid["area_m2"].sum(), 2)
        self.assertAlmostEqual(indexed.loc[(1, 0), "area_fraction"], 0.5)
        self.assertEqual(indexed.loc[(1, 0), "collision_count"], 1)
        self.assertFalse(Point(1.5, 0.5).within(triangle))
        self.assertEqual(indexed.loc[(0, 1), "collision_count"], 0)
        self.assertEqual(int(grid["collision_count"].sum()), 2)

    def test_holes_and_disconnected_small_parts_are_retained_correctly(self):
        with_hole = box(0, 0, 3, 3).difference(box(1, 1, 2, 2))
        grid, _ = build_count_grid(points_at([(0.5, 0.5), (2.5, 2.5)]), with_hole, 1)
        self.assertEqual(len(grid), 8)
        self.assertAlmostEqual(grid["area_m2"].sum(), 8)
        self.assertEqual(int(grid["collision_count"].eq(0).sum()), 6)
        islands = MultiPolygon([box(0.1, 0.1, 0.2, 0.2), box(2.1, 0.1, 2.2, 0.2)])
        grid, _ = build_count_grid(points_at([(0.15, 0.15), (2.15, 0.15)]), islands, 1)
        self.assertEqual(set(grid["grid_col"]), {0, 2})
        self.assertTrue(grid["partial_cell"].all())
        self.assertAlmostEqual(grid["area_m2"].sum(), 0.02)
        self.assertEqual(int(grid["collision_count"].sum()), 2)

    def test_origin_and_negative_coordinate_floor_assignment(self):
        points = points_at([(-0.75, -0.75), (0, 0), (0.75, 0.75)])
        grid, assigned = build_count_grid(points, box(-1, -1, 1, 1), 1)
        self.assertEqual(assigned.iloc[0][["grid_col", "grid_row"]].tolist(), [-1, -1])
        self.assertEqual(assigned.iloc[1][["grid_col", "grid_row"]].tolist(), [0, 0])
        self.assertEqual(int(grid["collision_count"].sum()), 3)
        grid, assigned = build_count_grid(points, box(-1, -1, 1, 1), 1, origin=(0.5, 0.5))
        self.assertEqual(assigned.iloc[1][["grid_col", "grid_row"]].tolist(), [-1, -1])
        self.assertEqual(int(grid["collision_count"].sum()), 3)

    def test_candidate_sizes_count_identical_event_population(self):
        points = points_at([(100, 100), (250, 250), (500, 500), (999, 999)])
        for size in (100, 250, 500):
            with self.subTest(size=size):
                grid, assigned = build_count_grid(points, box(0, 0, 1000, 1000), size)
                self.assertEqual(int(grid["collision_count"].sum()), 4)
                self.assertEqual(set(assigned["collision_index"]), set(points["collision_index"]))
                self.assertAlmostEqual(grid["area_m2"].sum(), 1_000_000)

    def test_summary_uses_explicit_all_and_occupied_denominators(self):
        grid, _ = build_count_grid(points_at([(0.25, 0.25), (1, 0.25), (1, 1), (1.75, 1.75)]), box(0, 0, 2, 2), 1)
        summary = summarise_grid(grid, 1)
        self.assertEqual(summary["retained_cells"], 4)
        self.assertEqual(summary["zero_count_pct"], 25)
        self.assertEqual(summary["occupied_cells"], 3)
        self.assertEqual(summary["mean_count_all_cells"], 1)
        self.assertEqual(summary["total_collisions"], 4)
        self.assertEqual(summary["events_in_partial_cells"], 0)
        empty, _ = build_count_grid(points_at([]), box(0, 0, 2, 2), 1)
        summary = summarise_grid(empty, 1)
        self.assertEqual(summary["zero_count_pct"], 100)
        self.assertTrue(np.isnan(summary["median_count_occupied_cells"]))

    def test_invalid_points_parameters_and_oversized_grids_stop(self):
        footprint = box(0, 0, 2, 2)
        points = points_at([(0.5, 0.5)])
        for size in (0, -1, np.nan):
            with self.subTest(size=size), self.assertRaises(ValueError):
                build_count_grid(points, footprint, size)
        for origin in ((0,), (0, np.nan)):
            with self.subTest(origin=origin), self.assertRaises(ValueError):
                build_count_grid(points, footprint, 1, origin=origin)
        for coordinates in ([(0, 0.5)], [(3, 3)], [(np.nan, 1)]):
            with self.subTest(coordinates=coordinates), self.assertRaises(ValueError):
                build_count_grid(points_at(coordinates), footprint, 1)
        duplicate = points_at([(0.5, 0.5), (1.5, 1.5)])
        duplicate["collision_index"] = "same-id"
        with self.assertRaises(ValueError):
            build_count_grid(duplicate, footprint, 1)
        with self.assertRaises(ValueError):
            build_count_grid(points.to_crs("EPSG:4326"), footprint, 1)
        with self.assertRaises(ValueError):
            build_count_grid(points, footprint, 1, max_cells=1)


if __name__ == "__main__":
    unittest.main()
