import json

with open("data/ndwi/kherson_flood_corridor_ndwi_monthly.json") as f:
    data = json.load(f)

for entry in data["data"]:
    date = entry["interval"]["from"][:7]
    ndwi = entry["outputs"]["ndwi"]["bands"]["B0"]["stats"]["mean"]
    print(f"{date}: NDWI = {ndwi:.4f}")