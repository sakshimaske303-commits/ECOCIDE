"""Step 4 — irrigation canals from OpenStreetMap (waterway=canal) in the study area.

Used to identify the irrigation network fed by the Kakhovka reservoir
(pre-registered rule in ANALYSIS_PLAN_v2.md, section 4.3).

Output: data/v2/osm_canals.geojson

    python v2/04_download_osm_canals.py   (fixed copy: python v2/04b_osm_canals.py)
"""
import json
import os
import sys
import time

import requests

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import grid  # noqa: E402

OUT = "data/v2/osm_canals.geojson"
SERVERS = ["https://overpass-api.de/api/interpreter",
           "https://overpass.private.coffee/api/interpreter",
           "https://maps.mail.ru/osm/tools/overpass/api/interpreter",
           "https://overpass.kumi.systems/api/interpreter"]
# overpass-api.de rejects requests without an identifying User-Agent (HTTP 406)
HEADERS = {"User-Agent": "ECOCIDE-research/2.0 (academic study; python-requests)",
           "Accept": "*/*"}


def main():
    if os.path.exists(OUT):
        print(f"{OUT} already exists.")
        return
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    w, s, e, n = grid.BBOX_LONLAT
    q = f'[out:json][timeout:900];way["waterway"="canal"]({s},{w},{n},{e});out geom;'
    data = None
    for url in SERVERS:
        for attempt in range(3):
            try:
                r = requests.post(url, data={"data": q}, headers=HEADERS, timeout=1000)
                r.raise_for_status()
                data = r.json()
                break
            except Exception as ex:  # noqa: BLE001
                print(f"{url} attempt {attempt + 1}: {ex}")
                time.sleep(60 * (attempt + 1))  # 429 = rate limit: wait longer each time
        if data:
            break
    if not data:
        sys.exit("Could not reach any Overpass server; try again later.")
    feats = []
    for el in data.get("elements", []):
        if el.get("type") != "way" or "geometry" not in el:
            continue
        coords = [[p["lon"], p["lat"]] for p in el["geometry"]]
        if len(coords) < 2:
            continue
        feats.append({"type": "Feature", "geometry": {"type": "LineString", "coordinates": coords},
                      "properties": {"osm_id": el["id"], **{k: v for k, v in el.get("tags", {}).items()
                                                            if k in ("name", "name:uk", "name:en", "name:ru", "waterway", "usage")}}})
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump({"type": "FeatureCollection", "features": feats,
                   "source": "OpenStreetMap contributors (ODbL), Overpass API",
                   "query": q, "downloaded": time.strftime("%Y-%m-%d")}, fh, ensure_ascii=False)
    print(f"Saved {OUT}: {len(feats)} canal segments")


if __name__ == "__main__":
    main()
