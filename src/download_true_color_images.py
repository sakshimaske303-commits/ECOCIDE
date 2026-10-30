import os
import requests
from auth_sentinelhub import get_sentinelhub_token

PROCESS_API_URL = "https://sh.dataspace.copernicus.eu/api/v1/process"
OUTPUT_DIR = "data/satellite_imagery"
BBOX = [32.0, 46.3, 33.6, 46.9]

EVALSCRIPT_TRUE_COLOR = """
//VERSION=3
function setup() {
  return {
    input: ["B02", "B03", "B04"],
    output: { bands: 3 }
  };
}
function evaluatePixel(sample) {
  return [sample.B04 * 2.5, sample.B03 * 2.5, sample.B02 * 2.5];
}
"""


def download_image(access_token, start_date, end_date, output_filename):
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}

    payload = {
        "input": {
            "bounds": {
                "bbox": BBOX,
                "properties": {"crs": "http://www.opengis.net/def/crs/EPSG/0/4326"},
            },
            "data": [{
                "type": "sentinel-2-l2a",
                "dataFilter": {
                    "timeRange": {"from": f"{start_date}T00:00:00Z", "to": f"{end_date}T23:59:59Z"},
                    "maxCloudCoverage": 20,
                    "mosaickingOrder": "leastCC"
                }
            }],
        },
        "output": {
            "width": 1600,
            "height": 1200,
            "responses": [{"identifier": "default", "format": {"type": "image/png"}}]
        },
        "evalscript": EVALSCRIPT_TRUE_COLOR,
    }

    response = requests.post(PROCESS_API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        output_path = os.path.join(OUTPUT_DIR, output_filename)
        with open(output_path, "wb") as f:
            f.write(response.content)
        print(f"Saved: {output_path}")
    else:
        print(f"FAILED ({response.status_code}): {response.text[:300]}")


def main():
    access_token = get_sentinelhub_token()

    print("Downloading BEFORE image (May 2023)...")
    download_image(access_token, "2023-05-01", "2023-05-31", "before_may2023.png")

    print("Downloading AFTER image (July 2023)...")
    download_image(access_token, "2023-07-01", "2023-07-31", "after_july2023.png")


if __name__ == "__main__":
    main()