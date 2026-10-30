"""Builds the anonymized submission files from ECO_Research_Paper_v2.md.

    python make_submission.py

Writes submission/Manuscript_anonymized.{md,docx,pdf}; needs pandoc (+ xelatex for the PDF).
"""
import re
import subprocess

SRC = "ECO_Research_Paper_v2.md"
OUT = "submission/Manuscript_anonymized"

s = open(SRC, encoding="utf-8").read()
# remove author block (lines between title and Abstract)
title, rest = s.split("\n", 1)
rest = rest[rest.index("## Abstract"):]
s = title + "\n\n" + rest
s = s.replace("github.com/sakshimaske303-commits/ECOCIDE", "[repository URL withheld for anonymous review]")
s = re.sub(r"\(previous version of this paper; all code and results retained in the repository\)",
           "(an earlier analysis; reference withheld for anonymous review)", s)
open(OUT + ".md", "w", encoding="utf-8").write(s)
subprocess.run(["pandoc", OUT + ".md", "-o", OUT + ".docx", "--resource-path=."], check=True)
CSS = """body{font-family:'DejaVu Serif',serif;font-size:11pt;line-height:1.55;max-width:none;margin:0}
h1{font-size:17pt}h2{font-size:14pt;margin-top:1.4em}h3{font-size:12pt}
img{max-width:100%}table{border-collapse:collapse;font-size:9.5pt;margin:0.8em 0}
td,th{border:1px solid #999;padding:3px 6px;vertical-align:top}p{text-align:justify}"""
open("/tmp/_ms.css", "w").write(CSS)
subprocess.run(["pandoc", OUT + ".md", "-o", "/tmp/_ms.html", "--standalone", "--embed-resources",
                "--resource-path=.", "--css=/tmp/_ms.css", "--metadata", "title= "], check=True)
subprocess.run(["wkhtmltopdf", "--quiet", "--enable-local-file-access", "-s", "A4", "-T", "22mm", "-B", "22mm",
                "-L", "22mm", "-R", "22mm", "--footer-center", "[page]", "--footer-font-size", "9",
                "/tmp/_ms.html", OUT + ".pdf"], check=True)
print("written", OUT + ".{md,docx,pdf}")


def md_to_pdf(src, dst):
    subprocess.run(["pandoc", src, "-o", "/tmp/_doc.html", "--standalone", "--embed-resources",
                    "--resource-path=.", "--css=/tmp/_ms.css", "--metadata", "title= "], check=True)
    subprocess.run(["wkhtmltopdf", "--quiet", "--enable-local-file-access", "-s", "A4", "-T", "20mm", "-B", "20mm",
                    "-L", "20mm", "-R", "20mm", "/tmp/_doc.html", dst], check=True)


# PDFs shown in the dashboard's document viewer
md_to_pdf("ECO_Research_Paper_v2.md", "dashboard/static/ECO_Research_Paper_v2.pdf")
md_to_pdf("ECO_Executive_Summary.md", "dashboard/static/ECO_Executive_Summary.pdf")
md_to_pdf("ECO_Development_Log.md", "dashboard/static/ECO_Development_Log.pdf")
print("written dashboard/static PDFs")
