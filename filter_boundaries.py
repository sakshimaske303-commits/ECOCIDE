import geopandas as gpd

# Load Ukraine boundary (Level 1 = Oblasts)
ukraine = gpd.read_file("data/boundaries/gadm41_UKR.gpkg", layer="ADM_ADM_1")
print("Ukraine oblasts:")
print(ukraine["NAME_1"].tolist())

# Load Romania boundary (Level 2 = Counties)
romania = gpd.read_file("data/boundaries/gadm41_ROU.gpkg", layer="ADM_ADM_2")
print("\nRomania counties:")
print(romania["NAME_2"].tolist())