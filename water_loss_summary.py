import geopandas as gpd

# Pre-breach reservoir extent (approximate, from documented literature:
# Kakhovka reservoir was 2,155 km² at full capacity before the breach)
PRE_BREACH_RESERVOIR_AREA_KM2 = 2155

# Post-breach flood extent at various dates (already loaded from UNOSAT)
dates_data = {
    "2023-06-06": "ST3_20230606_FloodExtent_KhersonskaOblast_UKR.shp",
    "2023-06-09": "ST3_20230609_FloodExtent_KhersonskaOblast_UKR.shp",
    "2023-06-21": "ST1_20230621_FloodExtent_KhersonskarOblast_UKR.shp",
}

print("Kakhovka Reservoir Water-Loss Quantification\n")
print(f"Pre-breach reservoir area (documented): {PRE_BREACH_RESERVOIR_AREA_KM2} km²\n")

for date, filename in dates_data.items():
    path = f"data/ndwi/FL20230606UKR_SHP.zip!FL20230606UKR_SHP/{filename}"
    gdf = gpd.read_file(path)
    gdf_equal_area = gdf.to_crs("EPSG:6933")
    downstream_flood_km2 = gdf_equal_area.geometry.area.sum() / 1_000_000

    print(f"{date}: Downstream flood extent = {downstream_flood_km2:.2f} km²")

print(f"\nNote: This represents downstream floodplain inundation, distinct from")
print(f"upstream reservoir drainage. The reservoir itself lost approximately")
print(f"18.2 km³ of water volume (per documented sources), while this")
print(f"downstream data captures the resulting land-surface flood impact.")