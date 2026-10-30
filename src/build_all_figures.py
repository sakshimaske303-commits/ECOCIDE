"""Regenerates every Study 1 figure from the current data and outputs/model_results.json.
Run from the repository root, after src/generate_model_results.py:

    python src/build_all_figures.py
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

SCRIPTS = [
    "flood_progression.py",
    "map1_flood_hydrograph.py",
    "map2_ndvi_comparison.py",
    "map3_event_study.py",
    "map4_flood_extent_geospatial.py",
    "map5_study_area_overview.py",
    "map6_robustness_check.py",
    "map7_control_panel_comparison.py",
    "map8_placebo_in_space.py",
    "build_interactive_plots.py",
    "build_kherson_flood_map.py",
    "build_maps_plots_pdf.py",
]

for s in SCRIPTS:
    print(f"--- {s}")
    subprocess.run([sys.executable, os.path.join(HERE, s)], check=True)
