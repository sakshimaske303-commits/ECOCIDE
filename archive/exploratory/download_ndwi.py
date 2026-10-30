import os
import json
import requests
from auth_sentinelhub import get_sentinelhub_token

STATISTICAL_API_URL = "https://sh.dataspace.copernicus.eu/api/v1/statistics"
OUTPUT_DIR = "data/ndwi"

# Narrowed to the actual flood-affected river corridor, not the entire
# Kherson Oblast, since the flood signal was being diluted to statistical
# invisibility when averaged across the full ~28,000 km2 oblast
ZONES = {
    "kherson_flood_corridor": (32.0, 46.3, 33.6, 46.9),
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


def request_ndwi(access_token, geometry, start, end):
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

    for zone_name, bbox in ZONES.items():
        print(f"\nProcessing {zone_name}...")
        geometry = make_bbox_geometry(bbox)

        result = request_ndwi(access_token, geometry, "2022-01-01", "2024-12-31")

        if result:
            output_path = os.path.join(OUTPUT_DIR, f"{zone_name}_ndwi_monthly.json")
            with open(output_path, "w") as f:
                json.dump(result, f, indent=2)
            data_count = len(result.get("data", []))
            print(f"  Saved: {output_path} ({data_count} monthly data points)")


if __name__ == "__main__":
    main()