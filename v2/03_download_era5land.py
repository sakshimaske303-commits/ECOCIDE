"""Step 3 — ERA5-Land monthly means (weather covariates), 2015–2024.

Source: Copernicus Climate Data Store, dataset
`reanalysis-era5-land-monthly-means` (free account + API key needed; see
v2/README_v2.md). Variables: 2 m temperature, total precipitation,
volumetric soil water (0–7 cm), at 0.1°.

Output: data/v2/era5land_monthly_2015_2024.nc

    python v2/03_download_era5land.py
"""
import os
import zipfile

import cdsapi

OUT = "data/v2/era5land_monthly_2015_2024.nc"
AREA = [49.5, 28.8, 45.1, 36.7]  # N, W, S, E (slightly larger than the analysis grid)


def main():
    if os.path.exists(OUT):
        print(f"{OUT} already exists.")
        return
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    c = cdsapi.Client()
    tmp = OUT + ".download"
    c.retrieve(
        "reanalysis-era5-land-monthly-means",
        {
            "product_type": ["monthly_averaged_reanalysis"],
            "variable": ["2m_temperature", "total_precipitation", "volumetric_soil_water_layer_1"],
            "year": [str(y) for y in range(2015, 2025)],
            "month": [f"{m:02d}" for m in range(1, 13)],
            "time": ["00:00"],
            "area": AREA,
            "data_format": "netcdf",
            "download_format": "unarchived",
        },
        tmp,
    )
    # the CDS sometimes returns a zip even when 'unarchived' is requested
    if zipfile.is_zipfile(tmp):
        with zipfile.ZipFile(tmp) as z:
            names = [n for n in z.namelist() if n.endswith(".nc")]
            if len(names) == 1:
                with z.open(names[0]) as src, open(OUT, "wb") as dst:
                    dst.write(src.read())
            else:
                folder = OUT.replace(".nc", "")
                z.extractall(folder)
                print(f"Several files returned; extracted to {folder}")
        os.remove(tmp)
    else:
        os.replace(tmp, OUT)
    print(f"Saved {OUT}")


if __name__ == "__main__":
    main()
