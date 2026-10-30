"""Reservoir context figures (documented, not derived here) alongside the
downstream flood-extent areas computed from UNOSAT layers.

This script does NOT quantify reservoir water loss from satellite data. The
reservoir's pre-breach area (~2,155 km²) and volume (~18.2 km³) are
documented values quoted for scale; the areas printed below are downstream
floodplain inundation, a different quantity.
"""
import eco_flood as ef

PRE_BREACH_RESERVOIR_AREA_KM2 = 2155   # documented value, quoted for scale only
PRE_BREACH_RESERVOIR_VOLUME_KM3 = 18.2  # documented value, quoted for scale only


def main():
    print("Kakhovka reservoir (documented, not computed here): "
          f"{PRE_BREACH_RESERVOIR_AREA_KM2} km², {PRE_BREACH_RESERVOIR_VOLUME_KM3} km³\n")
    rows, comp = ef.table()
    for r in rows:
        print(f"{r['date']}  {r['sensor']:17s} downstream flood extent = {r['flood_km2']:.2f} km²")
    print(f"UNOSAT 6–9 June cumulative composite = {comp['flood_km2']:.2f} km²")


if __name__ == "__main__":
    main()
