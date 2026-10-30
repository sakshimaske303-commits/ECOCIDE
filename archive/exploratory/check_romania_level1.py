import geopandas as gpd

romania_l1 = gpd.read_file("data/boundaries/gadm41_ROU.gpkg", layer="ADM_ADM_1")
print("Romania Level 1:")
print(romania_l1["NAME_1"].tolist())