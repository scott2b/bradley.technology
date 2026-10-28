"""Standalone preview of the Experience timeline concept.

Reads the real role dates out of content/experience/*.md so the preview cannot
drift from the site. Academic spans are held here because the site does not
record study periods — only completion years, in content/credentials/.

    python3 tools/timeline_preview.py && open build/timeline-preview.html

See EXPERIENCE_TIMELINE.md in the vault project (~/vault/projects/BradleyTechnology)
for the concept and the open questions. The output is not tracked.
"""
import pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "build" / "timeline-preview.html"
FONTS = ROOT / "static" / "fonts"
NOW, LO, W, LAB = 2026, 1994, 742, 256

# (institution, [(start, end), ...]) — a row may hold several spans, because
# study was not always continuous. All dates from the transcript record in
# vault/archive/courses-and-academic-completions.md. Nothing here is assumed.
# Wheaton is deliberately absent. This is a technical timeline and a theology
# M.A. is not technical study; it lives in Credentials instead. It also covers
# nothing here — its coursework (1995-1997) overlaps Perkins & Will and Nortel,
# and its thesis term (fa 2000) sits beside a gap that is 2001 either way.
ACADEMIC = [
    ("Capella University", [(2002, 2004)]),   # sp 2002 - sp 2004
    ("DePaul University",  [(2004, 2008)]),   # fa 2004 - au 2008
    ("UIC",                [(2006, 2007)]),   # fa 2006 - su 2007
]


def roles():
    out = []
    for f in sorted((ROOT / "content" / "experience").glob("*.md")):
        if f.name == "_index.md":
            continue
        fm = f.read_text().split("+++")[1]
        title = re.search(r'^title = "(.*)"$', fm, re.M).group(1)
        sub = (re.search(r'^subtitle = "(.*)"$', fm, re.M) or [None, ""])[1]
        m = re.search(r'(\d{4})\s*[–-]\s*(present|\d{4})', sub, re.I)
        if not m:
            continue
        now = m.group(2).lower() == "present"
        end = NOW if now else int(m.group(2))
        out.append(dict(name=title, spans=[(int(m.group(1)), end)],
                        kind="now" if now else "past"))
    return out


def build():
    items = roles() + [dict(name=n, spans=sp, kind="study") for n, sp in ACADEMIC]
    items.sort(key=lambda i: (-min(a for a, _ in i["spans"]),
                              -max(b for _, b in i["spans"])))
    x = lambda y: LAB + (y - LO) / (NOW - LO) * W
    css = f"""
@font-face{{font-family:'IBM Plex Sans';src:url('../static/fonts/IBMPlexSans-400.woff2') format('woff2');font-weight:400}}
@font-face{{font-family:'IBM Plex Sans';src:url('../static/fonts/IBMPlexSans-600.woff2') format('woff2');font-weight:600}}
@font-face{{font-family:'IBM Plex Mono';src:url('../static/fonts/IBMPlexMono-400.woff2') format('woff2');font-weight:400}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:'IBM Plex Sans',sans-serif;color:#333;background:#fff;padding:44px 56px;line-height:1.6}}
h1{{font-size:2.3rem}} h1::before{{content:"";display:inline-block;width:28px;height:3px;background:#e63946;vertical-align:middle;margin-right:14px}}
.lede{{color:#666;margin:.2rem 0 34px;max-width:640px}}
.chart{{position:relative;max-width:1040px}}
.axis{{position:relative;height:24px;border-bottom:1px solid #e6e6e6;margin-bottom:12px}}
.tick{{position:absolute;font-family:'IBM Plex Mono';font-size:.72rem;color:#8d9199;transform:translateX(-50%)}}
.tick i{{position:absolute;left:50%;top:19px;width:1px;height:6px;background:#e0e0e0}}
.row{{position:relative;height:36px}}
.row .lab{{position:absolute;left:0;top:7px;width:240px;text-align:right;font-size:.93rem;font-weight:600;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
.row.study .lab{{font-weight:400;color:#8d9199}}
.bar{{position:absolute;top:9px;height:16px;border-radius:8px}}
.bar.past{{background:#333;opacity:.55}} .bar.now{{background:#e63946}}
.bar.study{{background:#fff;border:2.5px solid #b9bcc1}}
.bar.assumed{{border-style:dashed}}
.note{{font-size:.8rem;color:#8d9199;margin-top:24px;padding-top:14px;border-top:1px solid #eee;max-width:780px}}
.key{{display:inline-block;width:22px;height:9px;border-radius:5px;vertical-align:middle;margin:0 4px}}"""
    o = [f"<!doctype html><meta charset=utf-8><title>Experience timeline — concept</title><style>{css}</style>",
         '<h1>Experience</h1><p class=lede>Labs, companies, and classrooms where I have built systems.</p><div class=chart><div class=axis>']
    for y in range(1995, NOW + 1, 5):
        o.append(f'<div class=tick style="left:{x(y):.0f}px">{y}<i></i></div>')
    o.append("</div>")
    for i in items:
        bars = "".join(
            f'<div class="bar {i["kind"]}" style="left:{x(a):.0f}px;'
            f'width:{max(x(b) - x(a), 12):.0f}px"></div>' for a, b in i["spans"])
        o.append(f'<div class="row{" study" if i["kind"] == "study" else ""}">'
                 f'<div class=lab>{i["name"]}</div>{bars}</div>')
    o.append('</div><p class=note><span class="key" style="background:#e63946"></span>current &nbsp;'
             '<span class="key" style="background:#333;opacity:.55"></span>past &nbsp;'
             '<span class="key" style="border:2.5px solid #b9bcc1"></span>study &nbsp;'
             '<br>All dates from the transcript record.</p>')
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text("".join(o))
    print(f"wrote {OUT}  ({len(items)} rows)")


build()
