import json

for zone in ["kherson", "tulcea"]:
    with open(f"data/ndvi/{zone}_ndvi_monthly.json") as f:
        data = json.load(f)
    entries = data["data"]
    print(f"\n{zone.upper()}: {len(entries)} data points")
    for entry in entries[:3]:
        date = entry["interval"]["from"]
        ndvi = entry["outputs"]["ndvi"]["bands"]["B0"]["stats"]["mean"]
        print(f"  {date[:7]}: NDVI = {ndvi:.4f}")