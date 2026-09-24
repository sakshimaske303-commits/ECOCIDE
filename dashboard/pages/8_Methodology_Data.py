import streamlit as st
import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(PROJECT_ROOT)
sys.path.append(os.path.join(PROJECT_ROOT, "dashboard"))
from results import R, FLOOD, p, c, ci
from styles import apply_custom_style, PALETTE

apply_custom_style()

st.markdown("<h1 style='text-align: center;'>📖 METHODOLOGY & DATA</h1>", unsafe_allow_html=True)
st.markdown(
    "<h3 style='text-align: center; color: #B0BEC5; font-weight: 700;'>Full Transparency and Reproducibility</h3>",
    unsafe_allow_html=True,
)
st.markdown("---")

# Proof-of-work popovers next to each data source/script — screenshots live in outputs/proof_screenshots/
st.markdown(f"""
<style>
    div[data-testid="stPopover"] button {{
        animation: proof-blink 1.8s ease-in-out infinite;
        border: 3px solid {PALETTE['accent']} !important;
        width: 32px !important;
        height: 32px !important;
        border-radius: 50% !important;
        padding: 0 !important;
        min-height: unset !important;
        min-width: unset !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }}
    div[data-testid="stPopover"] button p {{
        margin: 0 !important;
        font-size: 0.95rem !important;
        line-height: 1 !important;
    }}
    @keyframes proof-blink {{
        0%, 100% {{ box-shadow: 0 0 0px rgba(0, 172, 193, 0); }}
        50% {{ box-shadow: 0 0 12px rgba(0, 172, 193, 0.85); }}
    }}
</style>
""", unsafe_allow_html=True)

PROOF_DIR = os.path.join(PROJECT_ROOT, "outputs", "proof_screenshots")

def proof_popover(filename, caption):
    path = os.path.join(PROOF_DIR, filename)
    with st.popover("View"):
        if os.path.exists(path):
            st.image(path, caption=caption, width="stretch")
        else:
            st.caption(f"Screenshot not added yet — save it as `outputs/proof_screenshots/{filename}`.")

st.markdown("### Data Sources")

col1, col2 = st.columns(2)
with col1:
    st.markdown("""
    - **NDVI** — Sentinel-2 L2A via the Sentinel Hub Statistical API (Copernicus Data Space
      Ecosystem), monthly, Jan 2022 – Nov 2024, each zone's GADM v4.1 polygon, pixel-level
      Scene Classification masking of cloud, cloud shadow, cirrus and snow.
    - **True-colour imagery** — Sentinel-2 L2A via the Sentinel Hub Process API (context only).
    - **Boundaries** — GADM v4.1.
    """)
with col2:
    r1a, r1b = st.columns([0.88, 0.12])
    with r1a:
        st.markdown("- **Flood extent** — UNOSAT FL20230606UKR layers: Sentinel-3 (6, 9 June), ICEYE (7 June), "
                    "Sentinel-2 (8, 13 June), Sentinel-1 (21 June). Preliminary, not field-validated.")
    with r1b:
        proof_popover("01_kherson_flood_extent_qgis.png", "UNOSAT flood-extent layers for Kherson Oblast loaded in QGIS alongside the Sentinel-2 imagery.")
    st.markdown("- **Reservoir volume/area** — documented values (≈18.2 km³, ≈2,155 km²), quoted for scale only.")

st.markdown("---")

st.markdown("### How the Analysis Changed — and Why")

with st.expander("**Seasonal controls: month effects alone are not enough**"):
    st.markdown(f"""
    Monthly NDVI is dominated by the seasonal cycle. Early models added month-of-year effects shared
    by both zones. But Tulcea's seasonal swing ({R['pre_period']['tulcea']['seasonal_amplitude']:.2f} NDVI) is larger
    than Kherson's ({R['pre_period']['kherson']['seasonal_amplitude']:.2f}), and the post-event window contains two
    June–November seasons against one in the pre-event window. Shared month effects cannot absorb that,
    so part of the "effect" is seasonal. Allowing each zone its own seasonal cycle changes the primary
    estimate from {c(R['main_did'])} to {c(R['main_did_seasonal'])}.
    """)

with st.expander("**Monthly event study was not estimable — quarterly bins used instead**"):
    st.markdown("""
    A month-by-month event study needs almost as many parameters as there are months, so it could
    not be estimated. Quarterly bins (reference quarter March–May 2023) keep the model estimable.
    """)

with st.expander("**Standard errors: HAC on the monthly gap series**"):
    st.markdown("""
    With one treated zone and one control, cluster-robust standard errors are not usable, so
    Newey-West HAC standard errors are used for serial correlation. Earlier versions applied HAC to a
    stacked table of both zones, so the lag window ran across the join between zones and treated
    same-month observations as independent. Every model is now fitted to the single monthly
    treated-minus-control gap (same point estimates, correctly ordered lags), with a t-distribution.
    This widened the primary confidence interval considerably.
    """)

with st.expander("**Bounding box vs true polygon, and pixel-level cloud masking**"):
    st.markdown(f"""
    NDVI was originally requested over each zone's rectangular bounding box with only a scene-level
    cloud filter. It is now requested over the GADM polygon with a per-pixel Scene Classification
    mask. Because a polygon covers less area than its bounding box, valid coverage is
    structurally lower (Kherson at most {100*R['valid_fraction']['kherson']['max']:.0f}% of the request grid,
    minimum {100*R['valid_fraction']['kherson']['min']:.0f}% in {R['valid_fraction']['kherson']['min_month']}).
    Dropping low-coverage months does not change the conclusion.
    """)

with st.expander("**Third correction: pixel size, water mask and monthly compositing**"):
    st.markdown(f"""
    The second extraction did not set a pixel size, so every zone was sampled on a 256 × 256 grid
    (≈880 m over Kherson, ≈335 m over Brăila), water pixels were kept, and each pixel's monthly value came
    from a single scene. `download_ndvi_polygon_v3.py` uses a common 0.002° grid (≈150–220 m), masks water,
    and takes each pixel's median over all clear acquisitions in the month. With these data the primary
    estimate became {c(R['main_did'])} (p = {p(R['main_did']['p'])}), from −0.0747 (p = 0.162).
    """)

with st.expander("**Optical NDWI flood detection was replaced by UNOSAT layers**"):
    st.markdown("""
    NDWI-based flood detection from Sentinel-2 produced implausible week-to-week swings caused by
    cloud contamination, so UNOSAT's published flood-extent layers are used instead, each labelled
    with its own sensor.
    """)

st.markdown("---")

st.markdown("### Limitations")

st.warning(f"""
- **Treatment zone vs flood footprint.** The NDVI unit is the whole Kherson Oblast (≈25,500 km²); the
  mapped flood covered roughly {FLOOD['composite_6_9_june']['flood_in_oblast_km2']:.0f} km² of it, and several hundred km² of
  former reservoir bed inside the oblast re-vegetated after draining. An oblast-wide change cannot be
  attributed to the flood itself.
- **Valid coverage.** Monthly composites rest on {100*R['valid_fraction']['kherson']['min']:.0f}–{100*R['valid_fraction']['kherson']['max']:.0f}% of Kherson's grid cells.
- **Few units.** One treated oblast and four hand-picked control counties; randomization inference
  cannot reach p < 0.20, and two controls diverge on their own.
- **Pre-trends and seasonality.** Significant pre-event quarters and a seasonal pattern in the gap.
- **Single index.** NDVI measures greenness only — not soil, water quality or biodiversity.
""")

st.error(f"""
**Bottom line.** Primary DiD {c(R['main_did'])} (95% CI {ci(R['main_did'])}, HAC p = {p(R['main_did']['p'])}).
Kherson's vegetation declined relative to its controls after June 2023, but the design does not
attribute that decline to the dam: randomization rank {R['placebo_in_space']['rank_one_sided']} of 5, and pre-event quarters already deviate.
Code: `generate_model_results.py` reproduces every number on this dashboard.
""")

st.markdown("---")
st.markdown(
    "<p class='caption-text' style='text-align:center;'>ECOCIDE — Kakhovka Dam study</p>",
    unsafe_allow_html=True,
)
