"""Download the GADM v4.1 boundaries used by Study 1 and Study 2.

GADM data may be used for academic and non-commercial work, but may not be
redistributed (https://gadm.org/license.html), so the files are not kept in
this repository. Run once after cloning:

    python download_gadm.py                    # -> data/boundaries/gadm41_UKR.gpkg, gadm41_ROU.gpkg
    python extract_boundaries.py               # -> kherson_oblast.gpkg, tulcea_county.gpkg
    python extract_control_zone_boundaries.py  # -> galati, constanta, braila county files
    python export_zone_geometries.py           # -> data/boundaries/geometries/*.json (Study 1 downloads)

If the download fails, get the GeoPackage files for Ukraine and Romania by hand
from https://gadm.org/download_country.html and save them under the same names.
"""
import os
import urllib.request

URL = "https://geodata.ucdavis.edu/gadm/gadm4.1/gpkg/gadm41_{iso}.gpkg"
OUT_DIR = "data/boundaries"


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    for iso in ("UKR", "ROU"):
        out = os.path.join(OUT_DIR, f"gadm41_{iso}.gpkg")
        if os.path.exists(out):
            print(f"exists: {out}")
            continue
        print(f"downloading {URL.format(iso=iso)}")
        urllib.request.urlretrieve(URL.format(iso=iso), out + ".part")
        os.replace(out + ".part", out)
        print(f"saved: {out} ({os.path.getsize(out) / 1e6:.1f} MB)")


if __name__ == "__main__":
    main()
