# src/

Study 1 scripts and the helpers shared with Study 2. Run every script from the repository root, for example
`python src/generate_model_results.py`; paths to `data/` and `outputs/` are relative to the root.

| Group | Scripts |
|---|---|
| Boundaries (both studies) | `download_gadm.py`, `extract_boundaries.py`, `extract_control_zone_boundaries.py`, `export_zone_geometries.py` |
| Study 1 data | `download_ndvi_polygon_v3.py` (current), `download_ndvi_polygon.py` (version 2), `download_true_color_images.py`, `redownload_before.py`, `auth_sentinelhub.py` |
| Study 1 estimation | `eco_core.py` (engine), `generate_model_results.py` (all results -> `outputs/model_results.json`) |
| Study 1 individual checks | `did_model*.py`, `placebo*.py`, `event_study*.py`, `placebo_in_space_test.py`, `control_only_spillover_check.py`, `low_coverage_month_check.py`, `specification_robustness_check.py` |
| UNOSAT flood layers | `eco_flood.py`, `flood_progression.py` (-> `outputs/flood_extent_table.*`) |
| Figures | `eco_style.py` (shared style), `map1`–`map8_*.py`, `build_interactive_plots.py`, `build_kherson_flood_map.py`, `build_maps_plots_pdf.py`, `build_all_figures.py` (runs them all) |
| Documents | `make_submission.py` (PDF versions of the paper, summary and log for the dashboard) |

Study 2 lives in `v2/` (downloads) and `v2/analysis/` (models, figures, `run_all.py`, `run_revision.py`, `run_revision2.py`).
