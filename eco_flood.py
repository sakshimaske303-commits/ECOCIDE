"""Shared definitions for the UNOSAT FL20230606UKR flood layers.

Sensor names are taken from each shapefile's own Sensor_ID attribute (ST1 =
Sentinel-1, ST2 = Sentinel-2, ST3 = Sentinel-3). UNOSAT labels these products
as preliminary analyses not yet validated in the field. Each layer has its
own analysis extent and, for optical sensors, cloud obstruction, so areas
from different layers are separate observations, not one continuous series.
"""
import geopandas as gpd

ZIP = "data/ndwi/FL20230606UKR_SHP.zip"
BOUNDARY = "data/boundaries/kherson_oblast.gpkg"
EQUAL_AREA = "EPSG:6933"

# date, layer, sensor, analysis-extent layer, cloud-obstruction layer (or None)
LAYERS = [
    ("2023-06-06", "ST3_20230606_FloodExtent_KhersonskaOblast_UKR.shp", "Sentinel-3",
     "ST3_20230606_AnalysisExtent_KhersonskaOblast_UKR.shp", "ST3_20230606_CloudObstructionKhersonskaOblast_UKR.shp"),
    ("2023-06-07", "ICEYE_20230607_FloodExtent_KhersonskaOblast_UKR.shp", "ICEYE (SAR)",
     "ICEYE_20230607_AnalysisExtent_KhersonskaOblast_UKR.shp", None),
    ("2023-06-08", "ST2_20230608_FloodExtent_KhersonskarOblast_UKR.shp", "Sentinel-2",
     "ST3_20230609_ST2_20230608_AnalysisExtent_KhersonskaOblast_UKR.shp", None),
    ("2023-06-09", "ST3_20230609_FloodExtent_KhersonskaOblast_UKR.shp", "Sentinel-3",
     "ST3_20230609_ST2_20230608_AnalysisExtent_KhersonskaOblast_UKR.shp", None),
    ("2023-06-13", "ST2_20230613_FloodExtent_KhersonskaOblast_UKR.shp", "Sentinel-2",
     "ST2_20230613_AnalysisExtent_KhersonskaOblast_UKR.shp", "ST2_20230613_CloudObstruction_KhersonskaOblast_UKR.shp"),
    ("2023-06-21", "ST1_20230621_FloodExtent_KhersonskarOblast_UKR.shp", "Sentinel-1 (SAR)",
     "ST1_20230621_AnalysisExtent_KhersonskarOblast_UKR.shp", None),
]
COMPOSITE = "ST3_20230606_20230607_20230609_ST2_20230608_ICEYE_20230607_FloodExtent_KhersonskaOblast.shp"
MAP_DATES = ["2023-06-06", "2023-06-09", "2023-06-21"]


def read(layer):
    return gpd.read_file(f"zip://{ZIP}!FL20230606UKR_SHP/{layer}")


def area_km2(gdf, clip=None):
    g = gdf.to_crs(EQUAL_AREA)
    if clip is not None:
        g = g.geometry.intersection(clip)
        return float(g.area.sum() / 1e6)
    return float(g.geometry.area.sum() / 1e6)


def table():
    """Area of every layer, total and inside the Kherson Oblast polygon."""
    oblast = gpd.read_file(BOUNDARY).to_crs(EQUAL_AREA).union_all()
    rows = []
    for date, layer, sensor, ext, cloud in LAYERS:
        f = read(layer)
        rows.append({
            "date": date, "sensor": sensor, "layer": layer,
            "flood_km2": area_km2(f), "flood_in_oblast_km2": area_km2(f, oblast),
            "analysis_extent_km2": area_km2(read(ext)),
            "cloud_km2": area_km2(read(cloud)) if cloud else 0.0,
        })
    comp = read(COMPOSITE)
    composite = {"flood_km2": area_km2(comp), "flood_in_oblast_km2": area_km2(comp, oblast),
                 "note": "UNOSAT cumulative product: ICEYE 7 Jun, Sentinel-3 6–9 Jun, Sentinel-2 8 Jun"}
    return rows, composite
