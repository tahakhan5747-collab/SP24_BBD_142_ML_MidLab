"""Convert our simple Markdown report to printable HTML, using only the standard library."""

from pathlib import Path
from html import escape
import re

ROOT = Path(__file__).resolve().parent


def inline(s):
    s = escape(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    return re.sub(r"`([^`]+)`", r"<code>\1</code>", s)


if __name__ == "__main__":
    lines = (ROOT / "docs/REPORT.md").read_text(encoding="utf-8").splitlines()
    out = []
    i = 0
    while i < len(lines):
        s = lines[i]
        if s.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                cells = [x.strip() for x in lines[i].strip("|").split("|")]
                if not all(re.fullmatch(r"[-: ]+", x) for x in cells):
                    rows.append(cells)
                i += 1
            out.append(
                '<div class="table"><table><thead><tr>'
                + "".join("<th>" + inline(x) + "</th>" for x in rows[0])
                + "</tr></thead><tbody>"
            )
            out.extend(
                "<tr>" + "".join("<td>" + inline(x) + "</td>" for x in row) + "</tr>"
                for row in rows[1:]
            )
            out.append("</tbody></table></div>")
            continue
        if s.startswith("# "):
            out.append("<h1>" + inline(s[2:]) + "</h1>")
        elif s.startswith("## "):
            out.append("<h2>" + inline(s[3:]) + "</h2>")
        elif s.strip():
            out.append("<p>" + inline(s) + "</p>")
        i += 1
    style = """body{max-width:1080px;margin:45px auto;padding:0 25px;color:#19352f;font:14px/1.6 system-ui,sans-serif}h1{font-size:32px;line-height:1.2;border-bottom:3px solid #087f75;padding-bottom:20px}h2{font-size:20px;margin-top:32px;break-after:avoid}p{margin:10px 0}table{width:100%;border-collapse:collapse;font-size:11px;margin:12px 0}th,td{text-align:left;padding:7px;border:1px solid #dbe5df}th{background:#e7f1eb}.table{overflow-x:auto}code{font-size:12px}a{color:#087f75}@media print{body{margin:0;padding:0;font-size:10pt}h1{font-size:23pt}h2{font-size:14pt}table{font-size:8pt}.table{overflow:visible}tr{break-inside:avoid}thead{display:table-header-group}@page{size:A4;margin:16mm}}"""
    html = (
        '<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>ML Lab Report</title><style>'
        + style
        + "</style><body>"
        + "".join(out)
        + "</body></html>"
    )
    (ROOT / "docs/REPORT.html").write_text(html, encoding="utf-8")
    print("Saved docs/REPORT.html")
