"""Runs the whole Study 2 analysis in order (after steps 1–6 of v2/README_v2.md).

    python v2/analysis/run_all.py

Needs about 6 GB of free RAM (H2 has 1.6 million pixels x 9 years) and ~20 minutes.
Outputs: data/v2/derived/*, outputs/v2/*.json, outputs/v2/figures/*.png
"""
import runpy
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
STEPS = ["a1_layers.py", "a2_panel.py", "a3_h1.py", "a4_h2.py", "a5_h1_placebo.py",
         "a6_h3_h4.py", "a7_summary.py", "a8_figures.py"]

if __name__ == "__main__":
    sys.path.insert(0, HERE)
    for s in STEPS:
        t0 = time.time()
        print(f"\n===== {s} =====", flush=True)
        runpy.run_path(os.path.join(HERE, s), run_name="__main__")
        print(f"----- {s} done in {time.time() - t0:.0f}s", flush=True)
