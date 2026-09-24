import os
from reportlab.lib.pagesizes import A4, landscape, portrait
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from PIL import Image

BASE = "outputs"
OUT_PDF = "ECOCIDE_Maps_and_Plots.pdf"

DARK_BG = HexColor("#FFFFFF")
TEXT_WHITE = HexColor("#111111")
TEXT_GREY = HexColor("#444444")
ACCENT = HexColor("#1F77B4")

FIGURES = [
    {"num": 1, "path": "plots/study_area_overview.png", "title": "Study area",
     "caption": "Treatment zone (Kherson Oblast, Ukraine) and the four Romanian control counties (Tulcea, Galati, "
                "Braila, Constanta) in their true geographic positions. Boundaries: GADM v4.1."},
    {"num": 2, "path": "maps/before_may2023_final.png", "title": "Lower Dnipro before the breach (April-May 2023)",
     "caption": "Sentinel-2 L2A true-colour mosaic, 1 April - 31 May 2023, least-cloud mosaicking, bbox 32.0-33.6E, "
                "46.3-46.9N. The frame covers the downstream floodplain and only the south-western tip of the reservoir."},
    {"num": 3, "path": "maps/after_july_2023_final.png", "title": "Lower Dnipro after the breach (July 2023)",
     "caption": "Same bbox and processing, July 2023. The drained reservoir tip near Nova Kakhovka is visible at "
                "top right. Context only; not used as statistical evidence."},
    {"num": 4, "path": "plots/flood_extent_map.png", "title": "UNOSAT flood-extent layers",
     "caption": "UNOSAT FL20230606UKR layers for 6 June (Sentinel-3), 9 June (Sentinel-3) and 21 June (Sentinel-1). "
                "Preliminary, not field-validated; layers differ in sensor and analysis extent."},
    {"num": 5, "path": "plots/flood_hydrograph.png", "title": "UNOSAT flood-extent observations by sensor",
     "caption": "Mapped flood area in each UNOSAT layer, labelled by sensor. Separate observations, not a continuous "
                "series; see outputs/flood_extent_table.csv."},
    {"num": 6, "path": "plots/ndvi_comparison.png", "title": "Monthly NDVI, Kherson vs Tulcea",
     "caption": "Monthly mean NDVI (Sentinel-2, GADM polygons, SCL masking), January 2022 - November 2024. Descriptive."},
    {"num": 7, "path": "plots/event_study.png", "title": "Quarterly event study",
     "caption": "Kherson minus Tulcea NDVI gap by quarter relative to June 2023 (reference Mar-May 2023), Newey-West "
                "HAC 95% CIs; dagger marks quarters surviving Bonferroni correction."},
    {"num": 8, "path": "plots/robustness_check.png", "title": "Primary and narrowed-baseline estimates with placebos",
     "caption": "Classical and Newey-West HAC 95% CIs. Values from outputs/model_results.json."},
    {"num": 9, "path": "plots/control_panel_comparison.png", "title": "Kherson against each control and pooled",
     "caption": "DiD estimates against each Romanian control county and their mean, Newey-West HAC 95% CIs."},
    {"num": 10, "path": "plots/placebo_in_space.png", "title": "Placebo in space",
     "caption": "Each of the five units assigned 'treated' in turn against the other four; exact randomization "
                "p-values from Kherson's rank."},
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
                         "Kakhovka Dam destruction: satellite vegetation and flood evidence")

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
