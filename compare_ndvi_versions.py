import json

ZONES = ["kherson", "tulcea", "galati", "constanta", "braila"]
FLAG_THRESHOLD = 0.02  # NDVI units; months differing by more than this are flagged


def load(zone, folder):
    with open(f"{folder}/{zone}_ndvi_monthly.json") as f:
        data = json.load(f)
    out = {}
    for entry in data["data"]:
        date = entry["interval"]["from"][:7]
        stats = entry["outputs"]["ndvi"]["bands"]["B0"]["stats"]
        sample_count = stats.get("sampleCount")
        no_data_count = stats.get("noDataCount", 0)
        valid_frac = (1 - no_data_count / sample_count) if sample_count else None
        out[date] = {"mean": stats["mean"], "valid_frac": valid_frac}
    return out


def main():
    """
    Run this AFTER export_zone_geometries.py + download_ndvi_polygon.py have
    produced data/ndvi_v2/*.json. Compares the new polygon+SCL-masked NDVI
    against the original bbox-based data/ndvi/*.json, month by month, so you
    can see exactly what changed before deciding whether to promote the new
    data to primary (see PHASE2_INSTRUCTIONS.md).
    """
    for zone in ZONES:
        old = load(zone, "data/ndvi")
        new = load(zone, "data/ndvi_v2")
        print(f"\n=== {zone.upper()} ===")
        print(f"{'month':>9s} {'old_mean':>10s} {'new_mean':>10s} {'diff':>8s} "
              f"{'old_valid%':>11s} {'new_valid%':>11s}")
        all_months = sorted(set(old) | set(new))
        for month in all_months:
            o = old.get(month)
            n = new.get(month)
            if o is None or n is None:
                print(f"{month:>9s}  missing in {'new' if n is None else 'old'} data")
                continue
            diff = n["mean"] - o["mean"]
            flag = "  <-- FLAG" if abs(diff) > FLAG_THRESHOLD else ""
            ov = f"{o['valid_frac']*100:.1f}" if o["valid_frac"] is not None else "n/a"
            nv = f"{n['valid_frac']*100:.1f}" if n["valid_frac"] is not None else "n/a"
            print(f"{month:>9s} {o['mean']:10.4f} {n['mean']:10.4f} {diff:+8.4f} "
                  f"{ov:>11s} {nv:>11s}{flag}")


if __name__ == "__main__":
    main()
