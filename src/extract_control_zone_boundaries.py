import geopandas as gpd
import os

os.makedirs("data/boundaries", exist_ok=True)

# Extracts the Romanian county boundaries used as control zones — Galați,
# Constanța, Brăila — from the same GADM Level 1 source as Tulcea, so all
# control-zone boundaries come from one consistent data source.
CANDIDATES = {
    "Galați": "galati_county",
    "Constanța": "constanta_county",
    "Brăila": "braila_county",
}

romania = gpd.read_file("data/boundaries/gadm41_ROU.gpkg", layer="ADM_ADM_1")

for name, fname in CANDIDATES.items():
    county = romania[romania["NAME_1"] == name]
    county.to_file(f"data/boundaries/{fname}.gpkg", driver="GPKG")
    bounds = county.total_bounds
    print(f"{name} saved: {len(county)} feature(s), bounds={tuple(round(b, 4) for b in bounds)}")
