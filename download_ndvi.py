import os
import json
import requests
from auth_sentinelhub import get_sentinelhub_token

STATISTICAL_API_URL = "https://sh.dataspace.copernicus.eu/api/v1/statistics"
OUTPUT_DIR = "data/ndvi"

ZONES = {
    "kherson": (31.51, 45.90, 35.10, 47.58),
    "tulcea": (27.99, 44.61, 29.72, 45.46),
}


def make_bbox_geometry(bbox):
    min_lon, min_lat, max_lon, max_lat = bbox
    return {
        "type": "Polygon",
        "coordinates": [[
            [min_lon, min_lat], [max_lon, min_lat],
            [max_lon, max_lat], [min_lon, max_lat], [min_lon, min_lat]
        ]]
    }


def request_ndvi(access_token, geometry, start, end):
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}

    evalscript = """
    //VERSION=3
    function setup() {
      return {
        input: [{ bands: ["B04", "B08", "dataMask"] }],
        output: [
          { id: "ndvi", bands: 1, sampleType: "FLOAT32" },
          { id: "dataMask", bands: 1 }
        ]
      };
    }
    function evaluatePixel(sample) {
      let ndvi = (sample.B08 - sample.B04) / (sample.B08 + sample.B04);
      return { ndvi: [ndvi], dataMask: [sample.dataMask] };
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
                    "maxCloudCoverage": 40
                }
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
        print(f"  FAILED ({response.status_code}): {response.text[:300]}")
        return None


def main():
    access_token = get_sentinelhub_token()
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Monthly NDVI, spanning well before and after the 6 June 2023 dam destruction
    for zone_name, bbox in ZONES.items():
        print(f"\nProcessing {zone_name}...")
        geometry = make_bbox_geometry(bbox)

        result = request_ndvi(access_token, geometry, "2022-01-01", "2024-12-31")

        if result:
            output_path = os.path.join(OUTPUT_DIR, f"{zone_name}_ndvi_monthly.json")
            with open(output_path, "w") as f:
                json.dump(result, f, indent=2)
            data_count = len(result.get("data", []))
            print(f"  Saved: {output_path} ({data_count} monthly data points)")


if __name__ == "__main__":
    main()