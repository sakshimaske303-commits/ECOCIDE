import os
import json
import requests
from auth_sentinelhub import get_sentinelhub_token

STATISTICAL_API_URL = "https://sh.dataspace.copernicus.eu/api/v1/statistics"
OUTPUT_DIR = "data/ndwi"

# Splitting the original bounding box at the dam's latitude (46.777°N) to
# separate the upstream reservoir (which drained after the breach) from the
# downstream floodplain (which flooded) — these two opposing water-level
# signals were canceling each other out in the combined bounding box.
ZONES = {
    "kherson_upstream_reservoir": (32.0, 46.777, 33.6, 46.9),
    "kherson_downstream_floodplain": (32.0, 46.3, 33.6, 46.777),
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


def request_ndwi_weekly(access_token, geometry, start, end):
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    evalscript = """
    //VERSION=3
    function setup() {
      return {
        input: [{ bands: ["B03", "B08", "dataMask"] }],
        output: [
          { id: "ndwi", bands: 1, sampleType: "FLOAT32" },
          { id: "dataMask", bands: 1 }
        ]
      };
    }
    function evaluatePixel(sample) {
      let ndwi = (sample.B03 - sample.B08) / (sample.B03 + sample.B08);
      return { ndwi: [ndwi], dataMask: [sample.dataMask] };
    }
    """
    payload = {
        "input": {
            "bounds": {"geometry": geometry, "properties": {"crs": "http://www.opengis.net/def/crs/EPSG/0/4326"}},
            "data": [{"type": "sentinel-2-l2a", "dataFilter": {"timeRange": {"from": f"{start}T00:00:00Z", "to": f"{end}T23:59:59Z"}, "maxCloudCoverage": 60}}],
        },
        "aggregation": {
            "timeRange": {"from": f"{start}T00:00:00Z", "to": f"{end}T23:59:59Z"},
            "aggregationInterval": {"of": "P7D"},
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

    for zone_name, bbox in ZONES.items():
        print(f"\nProcessing {zone_name}...")
        geometry = make_bbox_geometry(bbox)
        result = request_ndwi_weekly(access_token, geometry, "2023-04-01", "2023-08-31")

        if result:
            output_path = os.path.join(OUTPUT_DIR, f"{zone_name}_weekly.json")
            with open(output_path, "w") as f:
                json.dump(result, f, indent=2)
            print(f"  Saved: {len(result['data'])} weekly data points")


if __name__ == "__main__":
    main()