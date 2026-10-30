import geopandas as gpd
import os

os.makedirs("data/boundaries", exist_ok=True)

# Extract Kherson Oblast from Ukraine (Level 1)
ukraine = gpd.read_file("data/boundaries/gadm41_UKR.gpkg", layer="ADM_ADM_1")
kherson = ukraine[ukraine["NAME_1"] == "Kherson"]
kherson.to_file("data/boundaries/kherson_oblast.gpkg", driver="GPKG")
print(f"Kherson saved: {len(kherson)} feature(s)")

# Extract Tulcea County from Romania (Level 1)
romania = gpd.read_file("data/boundaries/gadm41_ROU.gpkg", layer="ADM_ADM_1")
tulcea = romania[romania["NAME_1"] == "Tulcea"]
tulcea.to_file("data/boundaries/tulcea_county.gpkg", driver="GPKG")
print(f"Tulcea saved: {len(tulcea)} feature(s)")

# Print bounds for both, useful for later data acquisition
print("\nKherson bounds:", kherson.total_bounds)
print("Tulcea bounds:", tulcea.total_bounds)