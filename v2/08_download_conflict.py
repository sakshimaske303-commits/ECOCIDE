"""Step 8 (Registered Revision 1, R4) — conflict events and territorial control.

Tries VIINA (Zhukov; github.com/zhukovyuri/VIINA) first: lists the repository's Data
folder through the GitHub API and downloads the event and control files. If that
fails, tries UCDP GED (events only). Everything goes to data/v2/conflict/ and a
manifest (conflict_manifest.json) records what was obtained.

    python v2/08_download_conflict.py
"""
import json
import os
import time

import requests

OUT = "data/v2/conflict"
H = {"User-Agent": "ECOCIDE-research/2.0 (academic study)", "Accept": "application/vnd.github+json"}
UCDP = ["https://ucdp.uu.se/downloads/ged/ged251-csv.zip", "https://ucdp.uu.se/downloads/ged/ged241-csv.zip"]


def get(url, **kw):
    for a in range(3):
        try:
            r = requests.get(url, headers=H, timeout=600, **kw)
            if r.status_code == 200:
                return r
            print(f"  {url}: HTTP {r.status_code}")
        except Exception as ex:  # noqa: BLE001
            print(f"  {url}: {ex}")
        time.sleep(10 * (a + 1))
    return None


def main():
    os.makedirs(OUT, exist_ok=True)
    man = {"downloaded": time.strftime("%Y-%m-%d"), "files": [], "source": None}
    r = get("https://api.github.com/repos/zhukovyuri/VIINA/contents/Data")
    if r is not None:
        listing = r.json()
        names = [(e["name"], e.get("size", 0), e.get("download_url")) for e in listing if e.get("type") == "file"]
        print("VIINA Data folder:", [n for n, _, _ in names])
        man["viina_listing"] = [n for n, _, _ in names]
        want = [x for x in names if any(k in x[0].lower() for k in ("event", "control"))
                and x[0].lower().endswith((".zip", ".csv", ".gz")) and x[2]]
        for name, size, url in want:
            p = os.path.join(OUT, name)
            if os.path.exists(p):
                continue
            print(f"downloading {name} ({size/1e6:.1f} MB)")
            d = get(url)
            if d is not None:
                open(p, "wb").write(d.content)
                man["files"].append(name)
        if man["files"]:
            man["source"] = "VIINA"
    if not man["files"]:
        print("VIINA not obtained; trying UCDP GED")
        for u in UCDP:
            d = get(u)
            if d is not None:
                name = u.rsplit("/", 1)[1]
                open(os.path.join(OUT, name), "wb").write(d.content)
                man["files"].append(name)
                man["source"] = "UCDP GED"
                break
    json.dump(man, open(os.path.join(OUT, "conflict_manifest.json"), "w"), indent=1)
    print(json.dumps(man, indent=1))
    if not man["files"]:
        print("Nothing downloaded — tell Claude; the fallback occupation proxy (Addendum R4) will be used.")


if __name__ == "__main__":
    main()
