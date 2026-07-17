import json

for zone in ["kherson_upstream_reservoir", "kherson_downstream_floodplain"]:
    with open(f"data/ndwi/{zone}_weekly.json") as f:
        data = json.load(f)
    print(f"\n{zone.upper()}:")
    for entry in data["data"]:
        date = entry["interval"]["from"][:10]
        ndwi = entry["outputs"]["ndwi"]["bands"]["B0"]["stats"]["mean"]
        print(f"  {date}: NDWI = {ndwi:.4f}")