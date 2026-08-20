"""Folium rebuild of the Kherson flood-extent map (replaces old QGIS2Web export).
Same 3 verified UNOSAT flood polygons as map4_flood_extent_geospatial.py, interactive.
Outputs to dashboard/static/kherson_flood_extent_webmap/index.html."""
import os
import geopandas as gpd
import folium

SHP_DIR = "data/ndwi/FL20230606UKR_SHP/FL20230606UKR_SHP"
BOUNDARY_PATH = "data/boundaries/kherson_oblast.gpkg"
OUT_DIR = "dashboard/static/kherson_flood_extent_webmap"

BOUNDARY_COLOR = "#2d6a4f"
FLOOD_COLORS = {
    "2023-06-06": "#fca311",
    "2023-06-09": "#e63946",
    "2023-06-21": "#00b4d8",
}
FLOOD_LABEL = {
    "2023-06-06": "Flood Extent — 6 June 2023",
    "2023-06-09": "Flood Extent — 9 June 2023 (peak)",
    "2023-06-21": "Flood Extent — 21 June 2023 (recession)",
}
DATES = {
    "2023-06-06": "ST3_20230606_FloodExtent_KhersonskaOblast_UKR.shp",
    "2023-06-09": "ST3_20230609_FloodExtent_KhersonskaOblast_UKR.shp",
    "2023-06-21": "ST1_20230621_FloodExtent_KhersonskarOblast_UKR.shp",
}
SIMPLIFY_TOLERANCE = 0.0002  # degrees, display-only — see build_ecosystem_buffer_map.py in DOUBLE_JEOPARDY for the same approach


def main():
    boundary = gpd.read_file(BOUNDARY_PATH)
    minx, miny, maxx, maxy = boundary.total_bounds

    m = folium.Map(location=[46.63, 32.7], tiles="CartoDB dark_matter")
    # Zoom to the flood-affected corridor, matching the static map's own framing,
    # not the full oblast (most of the oblast never floods).
    m.fit_bounds([[46.2, 31.9], [47.0, 33.6]])

    boundary_simplified = boundary.copy()
    boundary_simplified["geometry"] = boundary_simplified.geometry.simplify(0.0005, preserve_topology=True)
    folium.GeoJson(
        boundary_simplified.__geo_interface__,
        name="Kherson Oblast Boundary",
        style_function=lambda f: {"color": BOUNDARY_COLOR, "weight": 1.5, "fillOpacity": 0},
    ).add_to(m)

    for date, filename in DATES.items():
        gdf = gpd.read_file(os.path.join(SHP_DIR, filename))
        area_ha = gdf["Area_ha"].iloc[0] if "Area_ha" in gdf.columns else None
        # Keep geometry only — the source attribute tables carry per-sensor
        # metadata (including a raw Timestamp column) that folium's GeoJson
        # serializer can't handle and this map doesn't need anyway; the date
        # and area are already in the popup text below.
        gdf = gdf[["geometry"]].copy()
        gdf["geometry"] = gdf.geometry.simplify(SIMPLIFY_TOLERANCE, preserve_topology=True)
        popup_html = (
            f"<b>{FLOOD_LABEL[date]}</b><br>"
            + (f"Extent: {area_ha:,.0f} ha<br>" if area_ha is not None else "")
            + "Source: UNOSAT Multi-Sensor Flood Mapping"
        )
        folium.GeoJson(
            gdf.__geo_interface__,
            name=FLOOD_LABEL[date],
            style_function=lambda f, c=FLOOD_COLORS[date]: {
                "color": "#ffffff", "weight": 0.5, "fillColor": c, "fillOpacity": 0.75,
            },
            popup=folium.Popup(popup_html, max_width=280),
        ).add_to(m)

    legend_html = f"""
    <div style="position: fixed; bottom: 30px; left: 30px; z-index: 9999;
                background: #0a1628; color: #ffffff; padding: 12px 16px; border-radius: 8px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.5); font-family: sans-serif; font-size: 13px; max-width: 300px;
                border: 1px solid #2d6a4f;">
      <b>Kherson Oblast — Kakhovka Dam Flood Extent</b><br><br>
      <span style="color:{BOUNDARY_COLOR};">■</span> Kherson Oblast boundary<br>
      <span style="color:{FLOOD_COLORS['2023-06-06']};">■</span> Flood extent, 6 June<br>
      <span style="color:{FLOOD_COLORS['2023-06-09']};">■</span> Flood extent, 9 June (peak)<br>
      <span style="color:{FLOOD_COLORS['2023-06-21']};">■</span> Flood extent, 21 June (recession)
    </div>
    """
    m.get_root().html.add_child(folium.Element(legend_html))
    folium.LayerControl(collapsed=False).add_to(m)

    os.makedirs(OUT_DIR, exist_ok=True)
    out_path = os.path.join(OUT_DIR, "index.html")
    m.save(out_path)
    size_mb = os.path.getsize(out_path) / 1_000_000
    print(f"Saved: {out_path} ({size_mb:.1f} MB)")


if __name__ == "__main__":
    main()
