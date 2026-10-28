"""
Two-column resume template (Yisak's design): beige header band with photo,
left sidebar + right main column, A4, two pages.

Which section goes where is set in tailor.yml -> layout (defaults below).
Print the generated .html from Chrome/Edge: Print -> Save as PDF, Margins: None,
Background graphics: ON.
"""
import base64, html, re
from pathlib import Path

DEFAULT_LAYOUT = {
    "page1": {"left": ["personal", "summary", "hobbies"], "right": ["experience", "education", "projects"]},
    "page2": {"left": ["skills"], "right": ["certifications", "achievements"]},
}

PERSONAL_LABELS = {"date_of_birth": "Date of birth", "passport": "Passport",
                   "visa_status": "Visa status", "nationality": "Nationality"}

E = lambda s: html.escape(str(s or ""))


def _link(text, url):
    return f'<a href="{E(url)}">{E(text)}</a>' if url else E(text)


def _bullets(items, cls=""):
    if not items:
        return ""
    return f'<ul class="b {cls}">' + "".join(f"<li>{i}</li>" for i in items) + "</ul>"


def _entry(title, dates, sub, bullets):
    return (f'<div class="entry"><div class="row"><span class="t">{title}</span>'
            f'<span class="d">{E(dates)}</span></div>'
            + (f'<div class="sub">{sub}</div>' if sub else "") + _bullets(bullets) + "</div>")


def render_two_column(v, cfg, root, pick_bullets, select_certs):
    pr, personal = v["profile"], v.get("personal") or {}
    track = cfg.get("track", "personal")
    focus = set(cfg.get("focus_tags", []))
    S = {}

    # ── left-column sections ──
    fields = cfg.get("personal_fields", ["date_of_birth", "passport", "visa_status"])
    rows = [(PERSONAL_LABELS.get(f, f.replace("_", " ").title()), personal.get(f)) for f in fields if personal.get(f)]
    if rows:
        S["personal"] = ("Personal Details", '<table class="kv">' + "".join(
            f"<tr><th>{E(k)}:</th><td>{E(val)}</td></tr>" for k, val in rows) + "</table>")

    summary = cfg.get("summary") or pr["summaries"].get(track) or pr["summaries"]["default"]
    S["summary"] = ("Summary", f'<p class="summary">{E(summary.strip())}</p>')

    if pr.get("hobbies"):
        S["hobbies"] = ("Hobbies &amp; Interests", _bullets([E(h) for h in pr["hobbies"]]))

    groups = cfg.get("skill_groups") or list(v["skills"].keys())
    items = []
    for gk in groups:
        g = v["skills"].get(gk)
        if not g:
            continue
        names = [s["name"] for s in g["items"] if s.get("level") in ("strong", "working", "familiar")]
        if cfg.get("max_skills_per_group"):
            names = names[: cfg["max_skills_per_group"]]
        if names:
            items.append(f'<b>{E(g["label"])}:</b> ' + E(", ".join(names)))
    S["skills"] = ("Skills", _bullets(items, "skills"))

    # ── right-column sections ──
    exp = []
    for e in (x for x in v["experience"] if x.get("include")):
        bl = pick_bullets(e.get("bullets", []), focus, cfg.get("bullets_per_role", 4))
        exp.append(_entry(E(e["title"]), f'{e["start"]} — {e["end"]}',
                          f'{E(e["company"])} - {E(e.get("location", ""))}', [E(b["text"]) for b in bl]))
    if exp:
        S["experience"] = ("Experience", "".join(exp))

    edu = []
    for e in v["education"]:
        if e.get("show_on_resume") is False:
            continue
        sub = f'{E(e.get("location", ""))} | {E(e["degree"])}'
        hl = [E(h) for h in e.get("highlights", [])]
        if cfg.get("show_coursework") and e.get("relevant_courses"):
            hl.append("<b>Relevant coursework:</b> " + E(", ".join(e["relevant_courses"])))
        edu.append(_entry(E(e["institution"]), f'{e.get("start", "")} — {e.get("end", "")}', sub, hl))
    S["education"] = ("Education", "".join(edu))

    allp = {p["id"]: p for p in v["projects"] if p.get("status") == "complete"}
    ids = [i for i in (cfg.get("projects") or list(allp)) if i in allp][: cfg.get("max_projects", 3)]
    proj = []
    for i in ids:
        p = allp[i]
        repo = (p.get("repos") or [""])[0]
        stack = ", ".join(p.get("stack", [])[: cfg.get("max_stack", 6)])
        bl = pick_bullets(p.get("bullets", []), focus, cfg.get("bullets_per_project", 2))
        proj.append(_entry(_link(p["title"], repo), str(p.get("period", "")),
                           f'<i>{E(stack)}</i>', [E(b["text"]) for b in bl]))
    if proj:
        S["projects"] = ("Selected Projects", "".join(proj))

    certs = select_certs(v["certs"], cfg, focus, "resume")
    if certs:
        lines = []
        for c in certs:
            meta = ", ".join(x for x in (c.get("issuer"), str(c.get("issued") or "")[:7]) if x)
            lines.append(_link(c["name"], c.get("credential_url", "") if str(c.get("credential_url", "")).startswith("http") else "")
                         + (f' <span class="m">— {E(meta)}</span>' if meta else ""))
        S["certifications"] = ("Certifications &amp; Licenses", _bullets(lines, "certs"))

    ach = [a for a in v["achievements"] if a.get("verified")]
    if ach:
        S["achievements"] = ("Achievements", _bullets([f'<b>{E(a["title"])}</b> ({E(a["date"])}) — {E(a.get("description", ""))}' for a in ach]))

    # ── header ──
    photo = ""
    ph = personal.get("photo")
    if ph and cfg.get("show_photo", True) and (root / ph).exists():
        mime = "image/png" if ph.lower().endswith(".png") else "image/jpeg"
        photo = f'<img class="photo" src="data:{mime};base64,{base64.b64encode((root / ph).read_bytes()).decode()}" alt="">'
    headline = cfg.get("headline") or pr["headlines"].get(track) or pr["headlines"]["default"]
    LBL = {"github": "GitHub", "linkedin": "LinkedIn", "portfolio": "Portfolio", "credly": "Credly"}
    links = " · ".join(_link(LBL.get(k, k.title()), u) for k, u in pr.get("links", {}).items()
                       if u and k in cfg.get("header_links", ["github", "linkedin", "portfolio", "credly"]))
    contact = " · ".join(E(x) for x in (pr.get("phone"), pr.get("email")) if x)
    header = (f'<header>{photo}<div class="hd"><h1>{E(pr["name"])}</h1><div class="hl">{E(headline)}</div>'
              f'<div class="ct">{E(personal.get("address") or pr.get("location"))}</div>'
              f'<div class="ct">{contact}</div><div class="ct links">{links}</div></div></header>')

    def col(names):
        return "".join(f'<section><h2>{S[n][0]}</h2>{S[n][1]}</section>' for n in names if n in S)

    layout = cfg.get("layout") or DEFAULT_LAYOUT
    pages = []
    for i, key in enumerate(sorted(layout)):
        pg = layout[key]
        pages.append(f'<div class="page">{header if i == 0 else ""}<div class="cols">'
                     f'<aside class="left">{col(pg.get("left", []))}</aside>'
                     f'<main class="right">{col(pg.get("right", []))}</main></div></div>')
    return f"""<!doctype html><html><head><meta charset="utf-8"><title>{E(pr['name'])} — Resume</title>
<style>{CSS}</style></head><body>{''.join(pages)}</body></html>"""


CSS = """
:root{--band:#dcd9c8;--ink:#1c1c1c;--muted:#555;--rule:#c9c9c9;--link:#1c1c1c}
*{box-sizing:border-box}
html,body{margin:0;padding:0;background:#e9e9e9}
body{font-family:'Times New Roman',Times,'Liberation Serif',serif;color:var(--ink);font-size:9.4pt;line-height:1.31;
 -webkit-print-color-adjust:exact;print-color-adjust:exact}
.page{width:210mm;height:297mm;margin:10mm auto;background:#fff;box-shadow:0 1px 6px rgba(0,0,0,.18);
 overflow:hidden;display:flex;flex-direction:column}
header{background:var(--band);display:flex;align-items:center;gap:7mm;padding:6mm 10mm 6mm 12mm;min-height:44mm}
.photo{width:30mm;height:37.5mm;object-fit:cover;border:1.5mm solid #fff;flex:none}
h1{font-size:27pt;font-weight:normal;margin:0 0 2.5mm;letter-spacing:.2px;line-height:1.1}
.hl{font-weight:bold;font-size:9.6pt;margin-bottom:2.5mm}
.ct{font-size:9pt;margin-top:1mm}
.links a{color:var(--ink)}
.cols{display:flex;flex:1;min-height:0}
.left{width:36%;padding:7mm 6mm 8mm 12mm;border-right:.4mm solid var(--rule)}
.right{width:64%;padding:7mm 12mm 8mm 7mm}
section{margin-bottom:4.4mm}
h2{font-size:10.4pt;text-transform:uppercase;letter-spacing:.5px;margin:0 0 2.5mm;padding-bottom:.8mm;
 border-bottom:.45mm solid var(--ink);display:block}
table.kv{border-collapse:collapse;width:100%}
table.kv th{text-align:left;font-weight:bold;padding:.6mm 2mm .6mm 0;white-space:nowrap;vertical-align:top}
table.kv td{text-align:right;padding:.6mm 0}
.summary{margin:0;text-align:left}
.entry{margin-bottom:3mm}
.row{display:flex;justify-content:space-between;gap:4mm;align-items:baseline}
.row .t{font-weight:bold;font-style:italic}
.row .d{font-weight:bold;font-style:italic;white-space:nowrap}
.sub{margin:.6mm 0 1.2mm}
.t a,.certs a{color:var(--link);text-decoration:none}
ul.b{list-style:none;margin:0;padding:0}
ul.b li{position:relative;padding-left:3.6mm;margin:0 0 1.1mm}
ul.b li::before{content:"";position:absolute;left:.6mm;top:.47em;width:1.15mm;height:1.15mm;border-radius:50%;background:var(--ink)}
ul.skills li{margin-bottom:2mm}
ul.certs{font-size:8.9pt}
ul.certs li{margin-bottom:.9mm}
.m{color:var(--muted)}
a{color:inherit}
@page{size:A4;margin:0}
@media print{html,body{background:#fff}.page{margin:0;box-shadow:none;page-break-after:always;break-after:page}
 .page:last-child{page-break-after:auto;break-after:auto}}
@media screen and (max-width:820px){.page{transform-origin:top left}}
"""
