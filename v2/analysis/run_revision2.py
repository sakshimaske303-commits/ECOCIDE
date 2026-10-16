"""Runs Registered Revision 2 (ANALYSIS_PLAN_v2_ADDENDUM_2.md) after run_all.py, run_revision.py and the
downloads of steps 9–11. Stops first if the addendum differs from its approved version.

    python v2/analysis/run_revision2.py
"""
import os
import runpy
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
STEPS = ["r2_prepare.py", "r2_h1.py", "r2_h1_placebo.py", "r2_h2.py", "r2_h3_h4.py", "r2_summary.py"]

if __name__ == "__main__":
    sys.path.insert(0, HERE)
    import r2lib
    print("Addendum 2 SHA-256 OK:", r2lib.check_addendum())
    for s in STEPS:
        t0 = time.time()
        print(f"\n===== {s} =====", flush=True)
        sys.argv = [s]
        runpy.run_path(os.path.join(HERE, s), run_name="__main__")
        print(f"----- done in {time.time() - t0:.0f}s", flush=True)
