import os
import json
import requests
from auth_sentinelhub import get_sentinelhub_token

STATISTICAL_API_URL = "https://sh.dataspace.copernicus.eu/api/v1/statistics"
OUTPUT_DIR = "data/ndwi"

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


def request_sar_water(access_token, geometry, start, end):
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}

    # Sentinel-1 SAR (radar) can see through clouds, unlike Sentinel-2
    # optical imagery. Water surfaces appear as smooth, low-backscatter
    # (dark) areas in VV polarization radar images, providing a
    # cloud-independent water detection method.
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
      // VV backscatter below -17 dB is a standard threshold for
      // identifying smooth open-water surfaces in Sentinel-1 SAR
      let vv_db = 10 * Math.log(sample.VV) / Math.LN10;
      let isWater = vv_db < -17 ? 1 : 0;
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
        result = request_sar_water(access_token, geometry, "2023-04-01", "2023-08-31")

        if result:
            output_path = os.path.join(OUTPUT_DIR, f"{zone_name}_sar_water.json")
            with open(output_path, "w") as f:
                json.dump(result, f, indent=2)
            print(f"  Saved: {len(result['data'])} weekly data points")


if __name__ == "__main__":
    main()