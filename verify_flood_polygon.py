import geopandas as gpd

flood = gpd.read_file(
    "data/ndwi/FL20230606UKR_SHP.zip!FL20230606UKR_SHP/ST3_20230606_FloodExtent_KhersonskaOblast_UKR.shp"
)
print("Columns:", flood.columns.tolist())
print("Features:", len(flood))
print("CRS:", flood.crs)
print("Bounds:", flood.total_bounds)

# Calculate total flooded area in km²
flood_equal_area = flood.to_crs("EPSG:6933")
total_area_km2 = flood_equal_area.geometry.area.sum() / 1_000_000
print(f"Total flood area: {total_area_km2:.2f} km²")