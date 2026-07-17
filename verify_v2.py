import json

with open("data/ndwi/kherson_downstream_relaxed_3day.json") as f:
    data = json.load(f)

for entry in data["data"]:
    date = entry["interval"]["from"][:10]
    water_pct = entry["outputs"]["water"]["bands"]["B0"]["stats"]["mean"] * 100
    print(f"{date}: Water % = {water_pct:.2f}%")