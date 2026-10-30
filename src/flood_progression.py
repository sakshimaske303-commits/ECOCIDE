"""Area of every UNOSAT flood-extent layer used in this project, with sensor,
analysis extent and cloud obstruction, written to outputs/flood_extent_table.csv."""
import json

import pandas as pd

import eco_flood as ef


def main():
    rows, comp = ef.table()
    df = pd.DataFrame(rows)
    df.to_csv("outputs/flood_extent_table.csv", index=False)
    with open("outputs/flood_extent_table.json", "w") as f:
        json.dump({"layers": rows, "composite_6_9_june": comp}, f, indent=2)
    pd.set_option("display.width", 200)
    print(df[["date", "sensor", "flood_km2", "flood_in_oblast_km2", "analysis_extent_km2", "cloud_km2"]].round(2).to_string(index=False))
    print(f"\nUNOSAT cumulative 6–9 June composite: {comp['flood_km2']:.2f} km² "
          f"({comp['flood_in_oblast_km2']:.2f} km² inside Kherson Oblast)")
    print("Saved: outputs/flood_extent_table.csv / .json")


if __name__ == "__main__":
    main()
