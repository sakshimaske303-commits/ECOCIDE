import os
import json
import requests
from auth_sentinelhub import get_sentinelhub_token

STATISTICAL_API_URL = "https://sh.dataspace.copernicus.eu/api/v1/statistics"
GEOMETRY_DIR = "data/boundaries/geometries"
OUTPUT_DIR = "data/ndvi_v2"

# All 5 zones, same acquisition window as the original bbox-based pull, but
# now using the actual GADM administrative-boundary geometry (exported by
# export_zone_geometries.py) instead of each zone's bounding box, plus
# pixel-level SCL-based cloud/shadow/snow masking instead of relying on the
# scene-level maxCloudCoverage filter alone. Output goes to data/ndvi_v2/,
# NOT data/ndvi/ -- the original bbox-based files are kept as the Phase-1
# baseline for comparison (see ECO_RESULTS_RECONCILIATION.md).
ZONES = ["kherson", "tulcea", "galati", "constanta", "braila"]


def load_geometry(zone_name):
    with open(f"{GEOMETRY_DIR}/{zone_name}_geometry.json") as f:
        return json.load(f)


def request_ndvi(access_token, geometry, start, end):
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}

    # Same NDVI formula as the original evalscript, but now also requests
    # the Scene Classification (SCL) band and uses it to zero out the
    # dataMask for cloud / cloud-shadow / cirrus / snow / no-data / saturated
    # pixels, so the Statistics API's mean/sampleCount/noDataCount reflect
    # genuinely clean vegetation-and-bare-ground pixels only.
    #
    # SCL codes excluded: 0 no data, 1 saturated/defective, 3 cloud shadow,
    # 8 cloud medium probability, 9 cloud high probability, 10 thin cirrus,
    # 11 snow/ice. (2 "dark area pixels" and 7 "unclassified" are kept in,
    # since those are not reliably cloud/shadow artifacts on their own.)
    evalscript = """
    //VERSION=3
    function setup() {
      return {
        input: [{ bands: ["B04", "B08", "SCL", "dataMask"] }],
        output: [
          { id: "ndvi", bands: 1, sampleType: "FLOAT32" },
          { id: "dataMask", bands: 1 }
        ]
      };
    }
    function evaluatePixel(sample) {
      let ndvi = (sample.B08 - sample.B04) / (sample.B08 + sample.B04);
      let invalidSCL = [0, 1, 3, 8, 9, 10, 11];
      let validScene = invalidSCL.indexOf(sample.SCL) === -1;
      let valid = sample.dataMask * (validScene ? 1 : 0);
      return { ndvi: [ndvi], dataMask: [valid] };
    }
    """

    payload = {
        "input": {
            "bounds": {
                "geometry": geometry,
                "properties": {"crs": "http://www.opengis.net/def/crs/EPSG/0/4326"},
            },
            "data": [{
                "type": "sentinel-2-l2a",
                "dataFilter": {
                    "timeRange": {"from": f"{start}T00:00:00Z", "to": f"{end}T23:59:59Z"},
                    "maxCloudCoverage": 40,
                },
            }],
        },
        "aggregation": {
            "timeRange": {"from": f"{start}T00:00:00Z", "to": f"{end}T23:59:59Z"},
            "aggregationInterval": {"of": "P1M"},
            "evalscript": evalscript,
        },
    }

    response = requests.post(STATISTICAL_API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"  FAILED ({response.status_code}): {response.text[:500]}")
        return None


def main():
    access_token = get_sentinelhub_token()
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for zone_name in ZONES:
        print(f"\nProcessing {zone_name} (polygon geometry + SCL masking)...")
        geometry = load_geometry(zone_name)

        result = request_ndvi(access_token, geometry, "2022-01-01", "2024-12-31")

        if result:
            output_path = os.path.join(OUTPUT_DIR, f"{zone_name}_ndvi_monthly.json")
            with open(output_path, "w") as f:
                json.dump(result, f, indent=2)
            data_count = len(result.get("data", []))
            print(f"  Saved: {output_path} ({data_count} monthly data points)")
        else:
            print(f"  Skipped {zone_name} -- see error above. If it's a geometry-complexity "
                  f"error (400 / timeout), raise this zone's SIMPLIFY_TOLERANCE_DEG in "
                  f"export_zone_geometries.py, re-run that script, then re-run this zone.")


if __name__ == "__main__":
    main()
