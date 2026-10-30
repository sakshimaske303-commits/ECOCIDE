import json
import os

import geopandas as gpd
from shapely.geometry import mapping
from shapely.ops import unary_union

os.makedirs("data/boundaries/geometries", exist_ok=True)

# Same 5 boundary files already produced by extract_boundaries.py and
# extract_control_zone_boundaries.py earlier in the project — this script
# does not re-fetch GADM, it only converts what's already on disk into the
# GeoJSON geometry that Sentinel Hub's Statistics API needs, simplified
# enough that the API will actually accept it.
ZONE_FILES = {
    "kherson": "data/boundaries/kherson_oblast.gpkg",
    "tulcea": "data/boundaries/tulcea_county.gpkg",
    "galati": "data/boundaries/galati_county.gpkg",
    "constanta": "data/boundaries/constanta_county.gpkg",
    "braila": "data/boundaries/braila_county.gpkg",
}

# Degrees of tolerance for shapely's simplify() (Douglas-Peucker). ~0.001
# degrees is roughly 100m at these latitudes -- small relative to a whole
# oblast/county, but enough to cut a complex coastline/river-delta boundary
# down to a vertex count the Statistics API will accept in one request.
# If a zone still fails with a 400/timeout from Sentinel Hub, raise this
# zone's tolerance (e.g. to 0.002 or 0.005) and re-run just that zone --
# don't blanket-raise it for every zone, since Tulcea/Galați/Brăila/
# Constanța sit on the much more convoluted Danube Delta coastline than
# Kherson does and may need more simplification.
SIMPLIFY_TOLERANCE_DEG = {
    "kherson": 0.001,
    "tulcea": 0.002,
    "galati": 0.002,
    "constanta": 0.002,
    "braila": 0.002,
}


def count_vertices(geom):
    if geom.geom_type == "Polygon":
        return len(geom.exterior.coords) + sum(len(r.coords) for r in geom.interiors)
    if geom.geom_type == "MultiPolygon":
        return sum(count_vertices(p) for p in geom.geoms)
    return None


def main():
    for zone, path in ZONE_FILES.items():
        gdf = gpd.read_file(path)

        # GADM ships in EPSG:4326 already, but reproject defensively in case
        # a saved .gpkg was ever re-exported in a different CRS.
        if gdf.crs is not None and gdf.crs.to_epsg() != 4326:
            gdf = gdf.to_crs(epsg=4326)

        # Some GADM layers return the boundary as multiple feature rows
        # (islands, exclaves); union them into one geometry so Sentinel Hub
        # gets a single Polygon/MultiPolygon per zone, not a FeatureCollection.
        geom = unary_union(gdf.geometry.values)

        vertices_before = count_vertices(geom)
        tolerance = SIMPLIFY_TOLERANCE_DEG[zone]
        simplified = geom.simplify(tolerance, preserve_topology=True)
        vertices_after = count_vertices(simplified)

        out_path = f"data/boundaries/geometries/{zone}_geometry.json"
        with open(out_path, "w") as f:
            json.dump(mapping(simplified), f)

        print(f"{zone:12s} vertices: {vertices_before:6d} -> {vertices_after:5d}  "
              f"(tolerance={tolerance})  saved: {out_path}")

    print("\nIf Sentinel Hub rejects a geometry as too complex when you run "
          "download_ndvi_polygon.py next, raise that specific zone's "
          "SIMPLIFY_TOLERANCE_DEG above and re-run this script before retrying.")


if __name__ == "__main__":
    main()
