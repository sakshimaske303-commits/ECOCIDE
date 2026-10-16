"""Step 9 (Registered Revision 2, R9) — irrigated-field maps of Baber et al. (2026b).

Source: Zenodo record 22036773, "Irrigation of Kherson and Zaporizhzhia 2019 - 2025", CC BY 4.0
(https://zenodo.org/records/22036773). Run ONLY after ANALYSIS_PLAN_v2_ADDENDUM_2.md is committed.

Downloads the 30 m GeoTIFFs for 2019–2022, 2024 and 2025 (≈ 58 MB). The 2023 file (≈ 461 MB,
probabilities) is used only to describe the decline and is skipped unless --with-2023 is given.
Each file is checked against the MD5 checksum published by Zenodo. Resumable.

    python v2/09_download_irrigation_maps.py
    python v2/09_download_irrigation_maps.py --with-2023
"""
import argparse
import hashlib
import json
import os
import re
import sys

import requests

RECORD = "https://zenodo.org/api/records/22036773"
OUT = "data/v2/irrigation_baber"


def md5(path):
    h = hashlib.md5()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--with-2023", action="store_true")
    args = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    rec = requests.get(RECORD, timeout=60).json()
    files = rec.get("files") or rec.get("entries") or []
    manifest = {"record": RECORD, "title": rec.get("metadata", {}).get("title"),
                "license": (rec.get("metadata", {}).get("license") or {}).get("id"), "files": {}}
    for f in files:
        name = f.get("key") or f.get("filename")
        year = re.search(r"(20\d\d)", name)
        year = int(year.group(1)) if year else None
        if year == 2023 and not args.with_2023:
            print("skip (use --with-2023):", name)
            continue
        url = f.get("links", {}).get("self") or f.get("links", {}).get("content")
        checksum = (f.get("checksum") or "").replace("md5:", "")
        path = os.path.join(OUT, name)
        if os.path.exists(path) and (not checksum or md5(path) == checksum):
            print("exists:", name)
        else:
            print(f"downloading {name} ({f.get('size', 0) / 1e6:.1f} MB)")
            with requests.get(url, stream=True, timeout=120) as r:
                r.raise_for_status()
                with open(path + ".part", "wb") as fh:
                    for chunk in r.iter_content(1 << 20):
                        fh.write(chunk)
            os.replace(path + ".part", path)
            if checksum and md5(path) != checksum:
                sys.exit(f"MD5 mismatch for {name}; delete it and re-run.")
        manifest["files"][name] = {"year": year, "md5": checksum, "bytes": os.path.getsize(path)}
    json.dump(manifest, open(os.path.join(OUT, "manifest.json"), "w"), indent=1)
    years = sorted(v["year"] for v in manifest["files"].values() if v["year"])
    missing = [y for y in (2019, 2020, 2021) if y not in years]
    if missing:
        sys.exit(f"Maps for {missing} are missing from the record; R9 cannot run as registered.")
    print("done:", years, "->", OUT)


if __name__ == "__main__":
    main()
