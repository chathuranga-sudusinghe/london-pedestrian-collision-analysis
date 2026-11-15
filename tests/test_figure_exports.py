"""Check PNG export behaviour with mocked files; no data or images are written."""

import ast
from io import BytesIO
import json
from pathlib import Path
from types import SimpleNamespace
import unittest
from unittest.mock import MagicMock


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS = (
    "02_spatial_validation.ipynb",
    "03_croydon_grid_comparison.ipynb",
    "04_croydon_spatial_inference.ipynb",
)


def helper_definition(filename):
    """Extract the helper alone; never execute notebook input cells."""
    notebook = json.loads((ROOT / "notebooks" / filename).read_text(encoding="utf-8"))
    for cell in notebook["cells"]:
        if cell["cell_type"] == "code":
            for node in ast.parse("".join(cell["source"])).body:
                if isinstance(node, ast.FunctionDef) and node.name == "save_report_figure":
                    return node
    raise AssertionError(f"Missing figure helper: {filename}")


def fixture(filename):
    directory, destination, temporary_path = MagicMock(), MagicMock(), MagicMock()
    directory.__truediv__.return_value = destination
    destination.name = "figure.png"
    destination.exists.return_value = True
    destination.read_bytes.return_value = b"old PNG bytes"
    temporary_factory = MagicMock()
    handle = temporary_factory.return_value.__enter__.return_value
    handle.name = "temporary.png.tmp"
    replace = MagicMock()
    namespace = {
        "EXPORT_FIGURES": True, "FIGURE_DIR": directory, "BytesIO": BytesIO,
        "NamedTemporaryFile": temporary_factory,
        "Path": MagicMock(return_value=temporary_path),
        "os": SimpleNamespace(replace=replace), "print": MagicMock(),
    }
    definition = helper_definition(filename)
    exec(compile(ast.Module(body=[definition], type_ignores=[]), filename, "exec"), namespace)
    figure = MagicMock()
    figure.savefig.side_effect = lambda buffer, **kwargs: buffer.write(b"new PNG bytes")
    return SimpleNamespace(
        save=namespace["save_report_figure"], namespace=namespace, figure=figure,
        directory=directory, destination=destination, temporary_path=temporary_path,
        temporary_factory=temporary_factory, handle=handle, replace=replace,
    )


class FigureExportTests(unittest.TestCase):
    def test_all_notebooks_use_the_same_helper(self):
        definitions = [ast.dump(helper_definition(name)) for name in NOTEBOOKS]
        self.assertTrue(all(value == definitions[0] for value in definitions))

    def test_disabled_export_does_not_render_or_touch_files(self):
        for name in NOTEBOOKS:
            with self.subTest(notebook=name):
                case = fixture(name)
                case.namespace["EXPORT_FIGURES"] = False
                case.save(case.figure, "figure.png")
                case.figure.savefig.assert_not_called()
                case.directory.__truediv__.assert_not_called()
                case.temporary_factory.assert_not_called()

    def test_identical_png_is_not_rewritten(self):
        for name in NOTEBOOKS:
            with self.subTest(notebook=name):
                case = fixture(name)
                case.destination.read_bytes.return_value = b"new PNG bytes"
                case.save(case.figure, "figure.png")
                self.assertEqual(case.figure.savefig.call_args.kwargs,
                                 {"format": "png", "dpi": 300, "bbox_inches": "tight"})
                case.directory.mkdir.assert_not_called()
                case.temporary_factory.assert_not_called()
                case.replace.assert_not_called()

    def test_new_or_changed_png_is_closed_before_replacement(self):
        for name in NOTEBOOKS:
            for existed in (False, True):
                with self.subTest(notebook=name, existed=existed):
                    case = fixture(name)
                    case.destination.exists.return_value = existed
                    case.replace.side_effect = lambda *args: self.assertTrue(
                        case.temporary_factory.return_value.__exit__.called)
                    case.save(case.figure, "figure.png")
                    self.assertEqual(case.temporary_factory.call_args.kwargs["dir"],
                                     case.directory)
                    case.handle.write.assert_called_once_with(b"new PNG bytes")
                    case.replace.assert_called_once_with(case.temporary_path, case.destination)
                    case.destination.open.assert_not_called()
                    case.temporary_path.unlink.assert_called_once_with(missing_ok=True)

    def test_render_failure_does_not_touch_existing_file(self):
        for name in NOTEBOOKS:
            with self.subTest(notebook=name):
                case = fixture(name)
                case.figure.savefig.side_effect = RuntimeError("render failed")
                with self.assertRaisesRegex(RuntimeError, "render failed"):
                    case.save(case.figure, "figure.png")
                case.directory.mkdir.assert_not_called()
                case.destination.open.assert_not_called()
                case.temporary_factory.assert_not_called()
                case.replace.assert_not_called()

    def test_write_failure_keeps_destination_and_cleans_temporary_file(self):
        for name in NOTEBOOKS:
            with self.subTest(notebook=name):
                case = fixture(name)
                case.handle.write.side_effect = OSError("write failed")
                with self.assertRaisesRegex(OSError, "write failed"):
                    case.save(case.figure, "figure.png")
                case.replace.assert_not_called()
                case.destination.open.assert_not_called()
                case.destination.unlink.assert_not_called()
                case.temporary_path.unlink.assert_called_once_with(missing_ok=True)

    def test_replace_failure_is_reported_and_cleans_temporary_file(self):
        for name in NOTEBOOKS:
            with self.subTest(notebook=name):
                case = fixture(name)
                case.replace.side_effect = OSError("replace failed")
                with self.assertRaisesRegex(OSError, "replace failed"):
                    case.save(case.figure, "figure.png")
                case.destination.open.assert_not_called()
                case.destination.unlink.assert_not_called()
                case.temporary_path.unlink.assert_called_once_with(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
