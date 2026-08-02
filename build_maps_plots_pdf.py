import os
from reportlab.lib.pagesizes import A4, landscape, portrait
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from PIL import Image

BASE = "outputs"
OUT_PDF = "ECOCIDE_Maps_and_Plots.pdf"

DARK_BG = HexColor("#0a1628")
TEXT_WHITE = HexColor("#ffffff")
TEXT_GREY = HexColor("#B0BEC5")
ACCENT = HexColor("#00b4d8")

FIGURES = [
    {
        "num": 1,
        "path": "plots/study_area_overview.png",
        "title": "Study Area Overview",
        "caption": "Treatment zone (Kherson Oblast, Ukraine) and matched control zone "
                   "(Tulcea County, Romania) used in the Difference-in-Differences design. "
                   "Boundaries: GADM v4.1.",
    },
    {
        "num": 2,
        "path": "maps/before_may2023_final.png",
        "title": "Before the Dam's Destruction (May 2023)",
        "caption": "Sentinel-2 true-colour imagery of the Kakhovka reservoir immediately before "
                   "the dam's destruction, showing the full reservoir.",
    },
    {
        "num": 2,
        "path": "maps/after_july_2023_final.png",
        "title": "After the Dam's Destruction (July 2023)",
        "caption": "Sentinel-2 true-colour imagery of the same area after the breach, showing "
                   "near-complete drainage of the reservoir and exposure of the former lakebed.",
    },
    {
        "num": 3,
        "path": "plots/flood_extent_map.png",
        "title": "Verified Flood-Extent Map",
        "caption": "UNOSAT multi-sensor flood-extent polygons over the Kherson Oblast flood "
                   "corridor at three dates (6, 9, 21 June 2023), showing the flood's rise, "
                   "peak, and recession.",
    },
    {
        "num": 4,
        "path": "plots/flood_hydrograph.png",
        "title": "Flood Hydrograph",
        "caption": "Verified flood extent over time: 122.50 km² (6 June) → 464.18 km² "
                   "peak (9 June) → 21.17 km² (21 June) — a complete rise-peak-recession "
                   "cycle within two weeks.",
    },
    {
        "num": 5,
        "path": "plots/ndvi_comparison.png",
        "title": "NDVI: Treatment vs. Control Over Time",
        "caption": "Monthly mean NDVI for Kherson (treatment) and Tulcea (control), Jan 2022 "
                   "– Dec 2024, showing a visible divergence after the dam's destruction.",
    },
    {
        "num": 6,
        "path": "plots/event_study.png",
        "title": "Quarterly Event Study",
        "caption": "Quarterly treatment-effect estimates (Newey-West HAC standard errors) "
                   "relative to the event date, including the disclosed pre-treatment-quarter "
                   "signal.",
    },
    {
        "num": 7,
        "path": "plots/robustness_check.png",
        "title": "Robustness: Classical vs. HAC Standard Errors",
        "caption": "Point estimates and 95% confidence intervals for all four causal-inference "
                   "models under classical OLS versus Newey-West HAC standard errors.",
    },
]


def draw_cover(c, page_w, page_h):
    c.setFillColor(DARK_BG)
    c.rect(0, 0, page_w, page_h, fill=1, stroke=0)

    c.setFillColor(TEXT_WHITE)
    c.setFont("Helvetica-Bold", 30)
    c.drawCentredString(page_w / 2, page_h - 80 * mm, "ECOCIDE")

    c.setFillColor(TEXT_GREY)
    c.setFont("Helvetica", 14)
    c.drawCentredString(page_w / 2, page_h - 92 * mm,
                         "A Satellite-Based Evidentiary Framework for War-Time Environmental Crimes")

    c.setFillColor(ACCENT)
    c.setFont("Helvetica-Bold", 13)
    c.drawCentredString(page_w / 2, page_h - 110 * mm, "Maps and Plots — Complete Figure Set")

    c.setFillColor(TEXT_WHITE)
    c.setFont("Helvetica", 11)
    y = page_h - 135 * mm
    seen = set()
    for fig in FIGURES:
        label = f"Figure {fig['num']}"
        if label in seen:
            continue
        seen.add(label)
        c.drawCentredString(page_w / 2, y, f"{label} — {fig['title']}")
        y -= 7 * mm

    c.setFillColor(TEXT_GREY)
    c.setFont("Helvetica", 10)
    c.drawCentredString(page_w / 2, 20 * mm, "Sakshi D. Maske — Independent Geospatial Researcher")


def draw_figure_page(c, fig):
    img_path = os.path.join(BASE, fig["path"])
    with Image.open(img_path) as im:
        iw, ih = im.size
    is_landscape = iw >= ih

    page_size = landscape(A4) if is_landscape else portrait(A4)
    page_w, page_h = page_size
    c.setPageSize(page_size)

    c.setFillColor(DARK_BG)
    c.rect(0, 0, page_w, page_h, fill=1, stroke=0)

    margin = 15 * mm
    title_h = 14 * mm
    caption_h = 20 * mm
    avail_w = page_w - 2 * margin
    avail_h = page_h - 2 * margin - title_h - caption_h

    scale = min(avail_w / iw, avail_h / ih)
    draw_w, draw_h = iw * scale, ih * scale
    x = (page_w - draw_w) / 2
    y = margin + caption_h + (avail_h - draw_h) / 2

    c.setFillColor(TEXT_WHITE)
    c.setFont("Helvetica-Bold", 15)
    c.drawCentredString(page_w / 2, page_h - margin - 8, f"Figure {fig['num']} — {fig['title']}")

    c.drawImage(img_path, x, y, width=draw_w, height=draw_h, preserveAspectRatio=True, mask="auto")

    c.setFillColor(TEXT_GREY)
    c.setFont("Helvetica", 10)
    caption_y = margin + caption_h - 6
    words = fig["caption"].split(" ")
    line, lines = "", []
    max_chars = 105 if is_landscape else 78
    for w in words:
        trial = f"{line} {w}".strip()
        if len(trial) > max_chars:
            lines.append(line)
            line = w
        else:
            line = trial
    if line:
        lines.append(line)
    for i, l in enumerate(lines):
        c.drawCentredString(page_w / 2, caption_y - i * 5 * mm, l)


def main():
    c = canvas.Canvas(OUT_PDF, pagesize=portrait(A4))
    draw_cover(c, *portrait(A4))
    c.showPage()

    for fig in FIGURES:
        draw_figure_page(c, fig)
        c.showPage()

    c.save()
    print(f"Saved: {OUT_PDF}")


if __name__ == "__main__":
    main()
