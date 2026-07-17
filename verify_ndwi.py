import json

for zone in ["kherson", "tulcea"]:
    with open(f"data/ndwi/{zone}_ndwi_monthly.json") as f:
        data = json.load(f)
    entries = data["data"]
    print(f"\n{zone.upper()}:")
    for entry in entries:
        date = entry["interval"]["from"][:7]
        ndwi = entry["outputs"]["ndwi"]["bands"]["B0"]["stats"]["mean"]
        print(f"  {date}: NDWI = {ndwi:.4f}")