"""Common analysis grid for the v2 (pixel-level) ECOCIDE study.

All rasters (MODIS NDVI, WorldCover fractions, exposure masks) are put on ONE
grid so every pixel means the same place in every dataset:

  * CRS: ETRS89 / LAEA Europe (EPSG:3035) — equal-area, standard for Europe.
  * Pixel size: 231.656358 m (the MODIS 250 m product's true pixel size).
  * Extent: 29.0–36.5 °E, 45.3–49.3 °N (lower Dnipro, Kakhovka reservoir,
    upstream Dnipro reservoirs, Southern Buh and lower Dniester), snapped to
    whole pixels.
  * A 10x finer grid (23.1656 m), nested exactly inside the coarse grid, is
    used to compute land-cover fractions per coarse pixel.
"""
import json
import os

from odc.geo.geobox import GeoBox
from odc.geo.geom import BoundingBox

BBOX_LONLAT = (29.0, 45.3, 36.5, 49.3)          # west, south, east, north
CRS = "EPSG:3035"
RES = 231.656358                                  # metres (MODIS 250 m nominal)
FINE_FACTOR = 10


def coarse_geobox():
    bb = BoundingBox(*BBOX_LONLAT, crs="EPSG:4326").to_crs(CRS)
    return GeoBox.from_bbox(bb, crs=CRS, resolution=RES, tight=False)


def fine_geobox():
    c = coarse_geobox()
    return GeoBox.from_bbox(c.boundingbox, crs=CRS, resolution=RES / FINE_FACTOR, tight=False)


def describe(path=None):
    c, f = coarse_geobox(), fine_geobox()
    info = {
        "crs": CRS, "res_m": RES, "bbox_lonlat": BBOX_LONLAT,
        "coarse_shape_yx": [c.shape.y, c.shape.x], "fine_shape_yx": [f.shape.y, f.shape.x],
        "coarse_bounds": list(c.boundingbox), "affine": list(c.affine)[:6],
    }
    if path:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as fh:
            json.dump(info, fh, indent=2)
    return info


if __name__ == "__main__":
    print(json.dumps(describe(), indent=2))
