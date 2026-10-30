import os
import json
import requests
from auth_sentinelhub import get_sentinelhub_token

STATISTICAL_API_URL = "https://sh.dataspace.copernicus.eu/api/v1/statistics"
OUTPUT_DIR = "data/ndwi"

BBOX_DOWNSTREAM = (32.0, 46.3, 33.6, 46.777)


def make_bbox_geometry(bbox):
    min_lon, min_lat, max_lon, max_lat = bbox
    return {
        "type": "Polygon",
        "coordinates": [[
            [min_lon, min_lat], [max_lon, min_lat],
            [max_lon, max_lat], [min_lon, max_lat], [min_lon, min_lat]
        ]]
    }


def request_sar_water_relaxed(access_token, geometry, start, end):
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}

    # Relaxed threshold (-14 dB instead of -17 dB) to capture flooded
    # vegetation and wet agricultural land, which produces a less
    # smooth (higher backscatter) signature than pure open water but
    # is still substantially wetter than dry cropland
    evalscript = """
    //VERSION=3
    function setup() {
      return {
        input: [{ bands: ["VV", "dataMask"] }],
        output: [
          { id: "water", bands: 1, sampleType: "UINT8" },
          { id: "dataMask", bands: 1 }
        ]
      };
    }
    function evaluatePixel(sample) {
      let vv_db = 10 * Math.log(sample.VV) / Math.LN10;
      let isWater = vv_db < -14 ? 1 : 0;
      return { water: [isWater], dataMask: [sample.dataMask] };
    }
    """

    payload = {
        "input": {
            "bounds": {"geometry": geometry, "properties": {"crs": "http://www.opengis.net/def/crs/EPSG/0/4326"}},
            "data": [{
                "type": "sentinel-1-grd",
                "dataFilter": {
                    "timeRange": {"from": f"{start}T00:00:00Z", "to": f"{end}T23:59:59Z"},
                    "acquisitionMode": "IW",
                    "polarization": "DV"
                }
            }],
        },
        "aggregation": {
            "timeRange": {"from": f"{start}T00:00:00Z", "to": f"{end}T23:59:59Z"},
            "aggregationInterval": {"of": "P3D"},
            "evalscript": evalscript,
        },
    }

    response = requests.post(STATISTICAL_API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()
    print(f"FAILED: {response.text[:300]}")
    return None


def main():
    access_token = get_sentinelhub_token()
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    geometry = make_bbox_geometry(BBOX_DOWNSTREAM)
    # Narrower window focused tightly on the flood event itself
    result = request_sar_water_relaxed(access_token, geometry, "2023-05-15", "2023-07-15")

    if result:
        output_path = os.path.join(OUTPUT_DIR, "kherson_downstream_relaxed_3day.json")
        with open(output_path, "w") as f:
            json.dump(result, f, indent=2)
        print(f"Saved: {len(result['data'])} data points")


if __name__ == "__main__":
    main()