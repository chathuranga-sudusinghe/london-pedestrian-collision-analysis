"""Preserve the candidate ONS boundary GeoPackage and append its provenance.

Run from the repository root: python scripts/download_boundaries.py
Uses only the Python standard library; no spatial analysis is performed.
"""

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
import sqlite3
import tempfile
from urllib.parse import urlsplit
from urllib.request import Request, urlopen


FILENAME = "ons-lad-december-2024-uk-bfe.gpkg"
SOURCE_PAGE = (
    "https://www.data.gov.uk/dataset/5d392106-7cb3-4214-90ac-4b46f16f0db3/"
    "local-authority-districts-december-2024-boundaries-uk-bfe"
)
DOWNLOAD_URL = (
    "https://open-geography-portalx-ons.hub.arcgis.com/api/download/v1/items/"
    "a4d56f9755be48b0a78c120e499fa9df/geoPackage?layers=0"
)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--data-dir", type=Path,
        default=Path(__file__).resolve().parents[1] / "data",
        help="Directory containing the existing download-manifest.json.",
    )
    args = parser.parse_args()
    data_dir = args.data_dir.expanduser().resolve()
    manifest_path = data_dir / "download-manifest.json"
    if not manifest_path.is_file():
        raise FileNotFoundError("Supply a data directory containing download-manifest.json.")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    entries = manifest.get("files")
    if not isinstance(entries, list):
        raise ValueError("The manifest must contain a files list.")
    output = data_dir / FILENAME
    if output.exists() or any(entry.get("file") == FILENAME for entry in entries):
        raise FileExistsError("Boundary file or manifest entry already exists; inspect it before rerunning.")

    temporary_path = None
    manifest_temp = None
    published = False
    try:
        request = Request(DOWNLOAD_URL, headers={"User-Agent": "COMP1890-boundary-download/1.0"})
        digest = hashlib.sha256()
        size = 0
        with urlopen(request, timeout=120) as response:
            if response.status != 200:
                raise RuntimeError(
                    "ONS has not returned a completed download. Retry later or inspect the source page."
                )
            # Redirect URLs can contain temporary signed credentials; retain host/path only.
            resolved_url = urlsplit(response.geturl())._replace(query="", fragment="").geturl()
            expected_size = response.headers.get("Content-Length")
            with tempfile.NamedTemporaryFile(dir=data_dir, suffix=".gpkg", delete=False) as handle:
                temporary_path = Path(handle.name)
                for chunk in iter(lambda: response.read(1024 * 1024), b""):
                    handle.write(chunk)
                    digest.update(chunk)
                    size += len(chunk)
        if expected_size is not None and size != int(expected_size):
            raise ValueError("Download size differs from the HTTP Content-Length.")
        with temporary_path.open("rb") as handle:
            if handle.read(16) != b"SQLite format 3\x00":
                raise ValueError("Response is not a GeoPackage; the service may have returned HTML, JSON or an archive.")
        with sqlite3.connect(temporary_path.as_uri() + "?mode=ro", uri=True) as connection:
            if connection.execute("PRAGMA application_id").fetchone()[0] != 0x47504B47:
                raise ValueError("SQLite file does not have the GeoPackage application identifier.")
            if connection.execute("PRAGMA quick_check").fetchone()[0] != "ok":
                raise ValueError("GeoPackage SQLite integrity check failed.")
            layers = connection.execute(
                "SELECT table_name, srs_id FROM gpkg_contents WHERE data_type = 'features'"
            ).fetchall()
            if not layers:
                raise ValueError("GeoPackage contains no feature layers.")

        entries.append({
            "file": FILENAME,
            "url": DOWNLOAD_URL,
            "resolved_url": resolved_url,
            "source_page": SOURCE_PAGE,
            "publisher": "Office for National Statistics",
            "boundary_vintage": "December 2024",
            "boundary_type": "BFE: full resolution, extent of the realm",
            "licence_source": "https://www.ons.gov.uk/methodology/geography/licences",
            "bytes": size,
            "sha256": digest.hexdigest(),
            "downloaded_utc": datetime.now(timezone.utc).isoformat(),
            "checks": {
                "sqlite_integrity": "ok",
                "feature_layers": [{"name": name, "srs_id": crs} for name, crs in layers],
                "geometry_validity": "not_checked",
                "london_code_reconciliation": "not_checked",
                "temporal_suitability": "not_checked",
            },
        })
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=data_dir, suffix=".json", delete=False,
        ) as handle:
            manifest_temp = Path(handle.name)
            json.dump(manifest, handle, indent=2, ensure_ascii=False)
            handle.write("\n")
        # Exclusive creation prevents replacement of an existing source file.
        with output.open("xb") as destination, temporary_path.open("rb") as source:
            published = True
            for chunk in iter(lambda: source.read(1024 * 1024), b""):
                destination.write(chunk)
        manifest_temp.replace(manifest_path)
    except BaseException:
        if published:
            output.unlink(missing_ok=True)
        raise
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)
        if manifest_temp is not None:
            manifest_temp.unlink(missing_ok=True)

    print(f"Preserved {FILENAME}: {size:,} bytes")
    print(f"SHA-256: {digest.hexdigest()}")
    print(f"Feature layers and CRS identifiers: {layers}")
    print("Manifest updated. Geometry, London codes and temporal suitability still require validation.")


if __name__ == "__main__":
    main()
