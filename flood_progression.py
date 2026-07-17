import geopandas as gpd

DATES = {
    "2023-06-06": "ST3_20230606_FloodExtent_KhersonskaOblast_UKR.shp",
    "2023-06-08": "ST2_20230608_FloodExtent_KhersonskarOblast_UKR.shp",
    "2023-06-09": "ST3_20230609_FloodExtent_KhersonskaOblast_UKR.shp",
    "2023-06-13": "ST2_20230613_FloodExtent_KhersonskaOblast_UKR.shp",
    "2023-06-21": "ST1_20230621_FloodExtent_KhersonskarOblast_UKR.shp",
}

print("Kakhovka Flood Progression:\n")
for date, filename in DATES.items():
    try:
        path = f"data/ndwi/FL20230606UKR_SHP.zip!FL20230606UKR_SHP/{filename}"
        gdf = gpd.read_file(path)
        gdf_equal_area = gdf.to_crs("EPSG:6933")
        area_km2 = gdf_equal_area.geometry.area.sum() / 1_000_000
        print(f"{date}: {area_km2:.2f} km² ({len(gdf)} feature(s))")
    except Exception as e:
        print(f"{date}: FAILED - {e}")