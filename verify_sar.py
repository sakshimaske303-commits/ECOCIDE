import json

for zone in ["kherson_upstream_reservoir", "kherson_downstream_floodplain"]:
    with open(f"data/ndwi/{zone}_sar_water.json") as f:
        data = json.load(f)
    print(f"\n{zone.upper()}:")
    for entry in data["data"]:
        date = entry["interval"]["from"][:10]
        water_pct = entry["outputs"]["water"]["bands"]["B0"]["stats"]["mean"] * 100
        print(f"  {date}: Water % = {water_pct:.2f}%")