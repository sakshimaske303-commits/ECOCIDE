"""Runs Registered Revision 1 (ANALYSIS_PLAN_v2_ADDENDUM_1.md) after run_all.py and steps 7–8.

    python v2/analysis/run_revision.py
"""
import os
import runpy
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
STEPS = [("r1_prepare.py", []), ("r1_h1.py", []), ("a5_h1_placebo.py", ["--r1"]), ("r1_h3_h4.py", []),
         ("r1_h2.py", []), ("r1_summary.py", []), ("r1_figures.py", [])]

if __name__ == "__main__":
    sys.path.insert(0, HERE)
    for s, args in STEPS:
        t0 = time.time()
        print(f"\n===== {s} {' '.join(args)} =====", flush=True)
        sys.argv = [s] + args
        runpy.run_path(os.path.join(HERE, s), run_name="__main__")
        print(f"----- done in {time.time() - t0:.0f}s", flush=True)
