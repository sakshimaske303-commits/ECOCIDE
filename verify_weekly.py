import json

with open("data/ndwi/kherson_flood_weekly.json") as f:
    data = json.load(f)

for entry in data["data"]:
    date = entry["interval"]["from"][:10]
    ndwi = entry["outputs"]["ndwi"]["bands"]["B0"]["stats"]["mean"]
    print(f"{date}: NDWI = {ndwi:.4f}")