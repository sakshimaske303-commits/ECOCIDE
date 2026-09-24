"""
NDVI extraction, version 3 — fixes three issues in download_ndvi_polygon.py
(the version that produced data/ndvi, a.k.a. data/ndvi_v2):

1. RESOLUTION. v2 sent no resx/resy, so Sentinel Hub sampled every zone on
   a default 256 x 256 grid (sampleCount = 65,536 for every zone). That is
   ~880 m pixels over Kherson but ~335 m over Brăila: a different effective
   resolution for treatment and controls. v3 sets the same pixel size for
   every zone (RES_DEG below, ~150-220 m).
2. WATER. v2 kept water pixels (SCL class 6, NDVI < 0) in the mean, so
   changes in water area (e.g. the drained Kakhovka reservoir inside the
   Kherson polygon, flooding, Danube Delta lakes) moved "vegetation" NDVI.
   v3 excludes SCL 6 as well.
3. MONTHLY AGGREGATION. v2 used the default single-scene mosaicking, so each
   pixel in a month came from one acquisition and a cloudy pixel in that
   scene was simply dropped. v3 uses ORBIT mosaicking and returns, per pixel,
   the median NDVI of all clear acquisitions in the month, then the API
   averages those pixels over the polygon.

Output goes to data/ndvi_v3/ — data/ndvi is NOT touched. After running:

    python download_ndvi_polygon_v3.py
    ECO_NDVI_DIR=data/ndvi_v3 python generate_model_results.py      (Linux/macOS)
    set ECO_NDVI_DIR=data\\ndvi_v3 && python generate_model_results.py   (Windows cmd)
    $env:ECO_NDVI_DIR="data/ndvi_v3"; python generate_model_results.py   (PowerShell)

Credentials come from .env via auth_sentinelhub.py, exactly as before.
Each zone takes a few minutes. If a request fails for size/timeout, raise
RES_DEG (e.g. 0.003) — but keep it the SAME for every zone.
maxCloudCoverage is relaxed to 80% because clouds are now removed per pixel.
"""
import json
import os
import time

import requests

from auth_sentinelhub import get_sentinelhub_token

STATISTICAL_API_URL = "https://sh.dataspace.copernicus.eu/api/v1/statistics"
GEOMETRY_DIR = "data/boundaries/geometries"
OUTPUT_DIR = "data/ndvi_v3"
ZONES = ["kherson", "tulcea", "galati", "constanta", "braila"]
RES_DEG = 0.002  # identical for all zones (~150 m E-W x ~220 m N-S at 45-47°N); Kherson grid ≈ 1800 x 840 px

# SCL classes excluded: 0 no data, 1 saturated/defective, 3 cloud shadow,
# 6 water, 8/9 cloud medium/high probability, 10 thin cirrus, 11 snow/ice.
EVALSCRIPT = """
//VERSION=3
function setup() {
  return {
    input: [{ bands: ["B04", "B08", "SCL", "dataMask"] }],
    output: [
      { id: "ndvi", bands: 1, sampleType: "FLOAT32" },
      { id: "dataMask", bands: 1 }
    ],
    mosaicking: "ORBIT"
  };
}
const INVALID = [0, 1, 3, 6, 8, 9, 10, 11];
function median(a) {
  a.sort(function (x, y) { return x - y; });
  const m = Math.floor(a.length / 2);
  return a.length % 2 ? a[m] : (a[m - 1] + a[m]) / 2;
}
function evaluatePixel(samples) {
  const vals = [];
  for (let i = 0; i < samples.length; i++) {
    const s = samples[i];
    if (s.dataMask === 1 && INVALID.indexOf(s.SCL) === -1 && (s.B08 + s.B04) > 0) {
      vals.push((s.B08 - s.B04) / (s.B08 + s.B04));
    }
  }
  if (vals.length === 0) { return { ndvi: [NaN], dataMask: [0] }; }
  return { ndvi: [median(vals)], dataMask: [1] };
}
"""


def load_geometry(zone):
    with open(f"{GEOMETRY_DIR}/{zone}_geometry.json") as f:
        return json.load(f)


def request_month_series(token, geometry, start, end):
    payload = {
        "input": {
            "bounds": {"geometry": geometry,
                       "properties": {"crs": "http://www.opengis.net/def/crs/EPSG/0/4326"}},
            "data": [{
                "type": "sentinel-2-l2a",
                "dataFilter": {"timeRange": {"from": f"{start}T00:00:00Z", "to": f"{end}T00:00:00Z"},
                               "maxCloudCoverage": 80},
            }],
        },
        "aggregation": {
            "timeRange": {"from": f"{start}T00:00:00Z", "to": f"{end}T00:00:00Z"},
            "aggregationInterval": {"of": "P1M"},
            "resx": RES_DEG,
            "resy": RES_DEG,
            "evalscript": EVALSCRIPT,
        },
    }
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    r = requests.post(STATISTICAL_API_URL, headers=headers, json=payload, timeout=600)
    if r.status_code != 200:
        print(f"  FAILED ({r.status_code}): {r.text[:500]}")
        return None
    return r.json()


def main():
    token = get_sentinelhub_token()
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for zone in ZONES:
        print(f"\n{zone}: polygon + SCL (incl. water) mask + per-pixel monthly median, res={RES_DEG}°")
        t0 = time.time()
        # one request per year keeps each call well inside API time limits
        parts = []
        # end dates are EXCLUSIVE and fall on a month boundary: Sentinel Hub drops a
        # monthly interval that is not complete inside timeRange (this is why an
        # earlier run lost Dec 2022, Dec 2023 and Nov 2024).
        for start, end in [("2022-01-01", "2023-01-01"), ("2023-01-01", "2024-01-01"), ("2024-01-01", "2024-12-01")]:
            res = request_month_series(token, load_geometry(zone), start, end)
            if res is None:
                parts = None
                break
            parts.extend(res.get("data", []))
        if parts is None:
            print(f"  Skipped {zone}.")
            continue
        parts.sort(key=lambda e: e["interval"]["from"])
        if len(parts) != 35:
            print(f"  WARNING: {zone} has {len(parts)} months, expected 35")
        out = {"data": parts, "status": "OK",
               "method": {"resx_deg": RES_DEG, "scl_excluded": [0, 1, 3, 6, 8, 9, 10, 11],
                          "mosaicking": "ORBIT, per-pixel monthly median", "maxCloudCoverage": 80}}
        path = os.path.join(OUTPUT_DIR, f"{zone}_ndvi_monthly.json")
        with open(path, "w") as f:
            json.dump(out, f, indent=2)
        print(f"  Saved {path}: {len(parts)} months in {time.time() - t0:.0f}s")


if __name__ == "__main__":
    main()
