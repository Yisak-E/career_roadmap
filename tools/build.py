#!/usr/bin/env python3
"""
Career Vault builder — turns the vault (single source of truth) into resumes and CVs.

  python tools/build.py check                      # list every TODO / unverified item
  python tools/build.py match  applications/<id>   # rank projects & skills against job.md
  python tools/build.py resume applications/<id>   # tailored 1–2 page resume  -> applications/<id>/
  python tools/build.py cv                         # full academic-style CV    -> output/

Outputs: .md (always), .html (print to PDF from any browser), .docx (if pandoc is installed).
Only dependency: PyYAML  (pip install pyyaml)
"""
import html, re, shutil, subprocess, sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("PyYAML missing — run:  pip install pyyaml")

ROOT = Path(__file__).resolve().parent.parent
TODO = re.compile(r"\bTODO\b")


# ───────────────────────── loading ─────────────────────────
def load_yaml(rel):
    p = ROOT / rel
    return yaml.safe_load(p.read_text(encoding="utf-8")) if p.exists() else None


def load_projects():
    out = []
    for f in sorted((ROOT / "Projects").glob("*/project.md")):
        txt = f.read_text(encoding="utf-8")
        m = re.match(r"^---\n(.*?)\n---\n", txt, re.S)
        if not m:
            continue
        p = yaml.safe_load(m.group(1))
        p["_path"] = f.relative_to(ROOT).as_posix()
        out.append(p)
    return sorted(out, key=lambda p: p.get("priority", 999))


def vault():
    return dict(
        profile=load_yaml("profile.yml"),
        education=load_yaml("Education/education.yml") or [],
        skills=(load_yaml("Skills/skills.yml") or {}).get("groups", {}),
        experience=load_yaml("Work-Experience/experience.yml") or [],
        certs=load_yaml("Certifications/certifications.yml") or [],
        achievements=load_yaml("Achievements/achievements.yml") or [],
        projects=load_projects(),
        personal=load_yaml("private/personal.yml") or {},
    )


def has_todo(x):
    return bool(TODO.search(yaml.safe_dump(x)))


# ───────────────────────── check ─────────────────────────
def cmd_check():
    v = vault()
    issues = []
    for key in ("email", "phone", "location"):
        if has_todo(v["profile"].get(key, "")):
            issues.append(f"profile.yml: {key}")
    for e in v["education"]:
        if has_todo(e):
            issues.append(f"Education: {e.get('id')} has TODO fields")
    for x in v["experience"]:
        if x.get("include") and not x.get("bullets"):
            issues.append(f"Work-Experience: {x['id']} has no bullets yet")
    for c in v["certs"]:
        if c.get("verified") and not (c.get("issuer") and c.get("issued")):
            issues.append(f"Certifications: {c['id']} missing issuer/date")
    if not any(x.get("include") for x in v["experience"]):
        issues.append("Work-Experience: no real roles yet (include: true)")
    for c in v["certs"]:
        if not c.get("verified"):
            issues.append(f"Certifications: {c['id']} not verified (hidden from output)")
    for a in v["achievements"]:
        if not a.get("verified"):
            issues.append(f"Achievements: {a['id']} not verified (hidden from output)")
    for p in v["projects"]:
        if p.get("status") != "complete":
            issues.append(f"Projects: {p['id']} status={p.get('status')} (hidden from output)")
        elif has_todo({k: p[k] for k in ("title", "summary", "bullets")}):
            issues.append(f"Projects: {p['id']} has TODO in printed text")
    for g in v["skills"].values():
        for s in g["items"]:
            if s.get("level") == "TODO":
                issues.append(f"Skills: '{s['name']}' needs evidence (hidden from output)")
    print(f"{len(issues)} open items\n" + "\n".join(" - " + i for i in issues))


# ───────────────────────── match ─────────────────────────
ALIASES = {
    "spring-boot": ["spring boot", "spring"], "nestjs": ["nest.js", "nestjs", "nest"],
    "nextjs": ["next.js", "nextjs"], "react-native": ["react native"], "rest": ["rest", "restful", "api"],
    "api": ["api", "apis", "microservice"], "sql": ["sql", "mysql", "postgres", "postgresql", "database", "rdbms"],
    "mongodb": ["mongo", "mongodb", "nosql"], "docker": ["docker", "container", "kubernetes", "k8s"],
    "devops": ["ci/cd", "devops", "pipeline", "cloud", "aws", "azure"], "security": ["security", "auth", "oauth", "jwt"],
    "concurrency": ["concurrency", "multithread", "thread", "scalab", "high-load", "performance"],
    "distributed": ["distributed", "microservice", "message queue", "kafka", "rabbitmq", "event-driven"],
    "messaging": ["kafka", "rabbitmq", "message", "queue", "event"], "testing": ["test", "qa", "junit", "jmeter", "automation"],
    "performance": ["performance", "load test", "jmeter", "latency"], "ai": ["ai", "machine learning", "ml", "llm", "gemini", "openai"],
    "nlp": ["nlp", "natural language", "sentiment"], "data": ["data", "analytics", "pandas", "bi", "dashboard"],
    "mobile": ["mobile", "android", "ios", "react native", "flutter"], "frontend": ["frontend", "front-end", "ui", "react", "angular", "vue"],
    "backend": ["backend", "back-end", "server-side", "api"], "fullstack": ["full stack", "full-stack", "fullstack"],
    "java": ["java"], "python": ["python"], "typescript": ["typescript", "ts"], "c": [" c ", "c/c++", "c++"],
    "real-time": ["real-time", "realtime", "websocket", "streaming"], "oop": ["oop", "object-oriented", "design pattern"],
    "algorithms": ["algorithm", "data structure"], "flask": ["flask"], "firebase": ["firebase", "gcp", "google cloud"],
}


def job_terms(jd):
    jd = " " + re.sub(r"\s+", " ", jd.lower()) + " "
    return {k for k, alts in ALIASES.items() if any(a in jd for a in alts)}, jd


def score_project(p, terms, jd):
    s = sum(2 for t in p.get("tags", []) if t in terms)
    s += sum(1 for st in p.get("stack", []) if st.lower().split(" (")[0] in jd)
    return s


def cmd_match(app):
    app = Path(app)
    jd = (app / "job.md").read_text(encoding="utf-8")
    terms, jdl = job_terms(jd)
    v = vault()
    ranked = sorted((p for p in v["projects"] if p.get("status") == "complete"),
                    key=lambda p: -score_project(p, terms, jdl))
    print("Job themes detected:", ", ".join(sorted(terms)) or "(none — is job.md filled in?)")
    print("\nProject ranking (score = tag hits x2 + stack hits):")
    for p in ranked:
        print(f"  {score_project(p, terms, jdl):>3}  {p['id']:<24} {p['title']}")
    hits = [s["name"] for g in v["skills"].values() for s in g["items"]
            if s.get("level") != "TODO" and s["name"].lower().split(" (")[0].split(" /")[0] in jdl]
    print("\nSkills named in the job that you have evidence for:", ", ".join(hits) or "-")
    print("\nCopy the top project ids into tailor.yml -> projects:")


# ───────────────────────── render ─────────────────────────
def fmt_skills(v, groups, max_items):
    lines = []
    for gk in groups or v["skills"].keys():
        g = v["skills"].get(gk)
        if not g:
            continue
        items = [s["name"] for s in g["items"] if s.get("level") in ("strong", "working", "familiar")]
        if max_items:
            items = items[:max_items]
        if items:
            lines.append(f"- **{g['label']}:** " + ", ".join(items))
    return lines


def pick_bullets(bullets, focus, n):
    if not focus:
        return bullets[:n]
    ranked = sorted(enumerate(bullets), key=lambda ib: (-len(set(ib[1].get("tags", [])) & focus), ib[0]))
    keep = sorted(ranked[:n], key=lambda ib: ib[0])
    return [b for _, b in keep]


def select_certs(all_certs, cfg, focus, mode):
    """Verified certs, newest first. Resume: best `max_certs` matches for focus_tags (0 / "all" = every one)."""
    datenum = lambda c: int(re.sub(r"\D", "", str(c.get("issued") or "")) or 0)
    certs = sorted((c for c in all_certs if c.get("verified")), key=lambda c: -datenum(c))
    if cfg.get("certifications"):                      # explicit list wins
        byid = {c["id"]: c for c in certs}
        return [byid[i] for i in cfg["certifications"] if i in byid]
    limit = cfg.get("max_certs", 5)
    if mode == "resume" and limit not in (0, "all", None):
        keep = sorted(certs, key=lambda c: (-(len(set(c.get("tags", [])) & focus) + bool(c.get("featured"))),
                                            -datenum(c)))[:limit]
        certs = [c for c in certs if c in keep]
    return certs


def render(v, cfg, mode):
    pr = v["profile"]
    track = cfg.get("track", "default")
    focus = set(cfg.get("focus_tags", []))
    L = []
    L.append(f"# {pr['name']}")
    L.append(f"**{cfg.get('headline') or pr['headlines'].get(track, pr['headlines']['default'])}**\n")
    contact = [pr.get("location"), pr.get("email"), pr.get("phone")]
    contact = [c for c in contact if c and not TODO.search(str(c))]
    LBL = {"github": "GitHub", "linkedin": "LinkedIn", "portfolio": "Portfolio", "credly": "Credly"}
    links = [f"[{LBL.get(k, k.title())}]({u})" for k, u in pr.get("links", {}).items() if u and not TODO.search(u)]
    L.append(" · ".join(contact + links) + "\n")

    L.append("## Summary")
    L.append((cfg.get("summary") or pr["summaries"].get(track, pr["summaries"]["default"])).strip() + "\n")

    order = cfg.get("sections") or (["summary", "skills", "experience", "projects", "education", "certifications", "achievements"])
    body = {}

    body["skills"] = ["## Technical Skills", *fmt_skills(v, cfg.get("skill_groups"), cfg.get("max_skills_per_group")), ""]

    exp = [e for e in v["experience"] if e.get("include")]
    if exp:
        s = ["## Experience"]
        for e in exp:
            s.append(f"### {e['title']} — {e['company']}")
            s.append(f"*{e.get('type', '')} · {e.get('location', '')} · {e['start']} – {e['end']}*\n")
            if mode == "resume" and cfg.get("compact_experience") and not e.get("bullets"):
                pass
            s += [f"- {b['text']}" for b in pick_bullets(e.get("bullets", []), focus, cfg.get("bullets_per_role", 4))]
            s.append("")
        body["experience"] = s

    allp = {p["id"]: p for p in v["projects"] if p.get("status") == "complete"}
    ids = cfg.get("projects") or list(allp)
    ids = [i for i in ids if i in allp]
    if mode == "resume":
        ids = ids[: cfg.get("max_projects", 4)]
    s = ["## Projects" if mode == "resume" else "## Selected Projects"]
    for i in ids:
        p = allp[i]
        repo = p["repos"][0] if p.get("repos") else ""
        title = f"[{p['title']}]({repo})" if repo else p["title"]
        s.append(f"### {title}")
        s.append(f"*{', '.join(p.get('stack', [])[: cfg.get('max_stack', 8)])}* · {p.get('period', '')}\n")
        if mode == "cv":
            s.append(p["summary"] + "\n")
        n = cfg.get("bullets_per_project", 3 if mode == "resume" else 10)
        s += [f"- {b['text']}" for b in pick_bullets(p.get("bullets", []), focus, n)]
        s.append("")
    body["projects"] = s

    s = ["## Education"]
    for e in v["education"]:
        if mode == "resume" and e.get("show_on_resume") is False:
            continue
        s.append(f"### {e['degree']} — {e['institution']}")
        s.append(f"*{e.get('location', '')} · {e.get('start', '')} – {e.get('end', '')}*" + (f" · GPA {e['gpa']}" if e.get("gpa") else "") + "\n")
        if e.get("relevant_courses"):
            s.append("Relevant coursework: " + ", ".join(e["relevant_courses"]) + "\n")
    body["education"] = s

    certs = select_certs(v["certs"], cfg, focus, mode)
    if certs:
        s = ["## Certifications"]
        for c in certs:
            name = f"[{c['name']}]({c['credential_url']})" if c.get("credential_url", "").startswith("http") else c["name"]
            meta = ", ".join(x for x in (c.get("issuer"), str(c.get("issued") or "")[:7]) if x)
            s.append(f"- {name}" + (f" — {meta}" if meta else ""))
        body["certifications"] = s + [""]

    ach = [a for a in v["achievements"] if a.get("verified")]
    if ach:
        body["achievements"] = ["## Achievements", *[f"- **{a['title']}** ({a['date']}) — {a.get('description', '').strip()}" for a in ach], ""]

    for sec in order:
        if sec != "summary" and sec in body:
            L += body[sec]
    md = "\n".join(L)
    if TODO.search(md):
        print("WARNING: output still contains TODO text — run `check`.")
    return md


CSS = """
@page{size:A4;margin:11mm 13mm}
body{font:9.8pt/1.3 'Segoe UI',Calibri,Arial,sans-serif;color:#1d1d1f;max-width:820px;margin:24px auto;padding:0 16px}
h1{font-size:22pt;margin:0;letter-spacing:.3px}
h1+p{margin:2px 0 4px;color:#1f4e79}
h2{font-size:10.8pt;text-transform:uppercase;letter-spacing:1px;color:#1f4e79;border-bottom:1.2px solid #1f4e79;padding-bottom:2px;margin:9px 0 4px}
h3{font-size:10.2pt;margin:5px 0 0}
h3+p{margin:0 0 2px;color:#555;font-size:9.5pt}
ul{margin:2px 0 4px;padding-left:18px} li{margin:1px 0}
p{margin:3px 0} a{color:#1f4e79;text-decoration:none}
@media print{body{margin:0;max-width:none}}
"""


def write_outputs(md, out_dir, stem):
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / f"{stem}.md").write_text(md, encoding="utf-8")
    pandoc = shutil.which("pandoc")
    if pandoc:
        body = subprocess.run([pandoc, "-f", "markdown", "-t", "html"], input=md.encode(), capture_output=True).stdout.decode()
    else:  # minimal fallback converter
        body = md_to_html(md)
    (out_dir / f"{stem}.html").write_text(
        f"<!doctype html><html><head><meta charset='utf-8'><title>{stem}</title><style>{CSS}</style></head><body>{body}</body></html>",
        encoding="utf-8")
    made = [f"{stem}.md", f"{stem}.html"]
    if pandoc:
        r = subprocess.run([pandoc, str(out_dir / f"{stem}.md"), "-o", str(out_dir / f"{stem}.docx")], capture_output=True)
        if r.returncode == 0:
            made.append(f"{stem}.docx")
    print(f"Wrote {', '.join(made)} to {out_dir.relative_to(ROOT)}/  (open the .html and Print → Save as PDF)")


def md_to_html(md):
    out, inlist = [], False
    for line in md.splitlines():
        t = html.escape(line)
        t = re.sub(r"\[(.+?)\]\((.+?)\)", r"<a href='\2'>\1</a>", t)
        t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
        t = re.sub(r"\*(.+?)\*", r"<i>\1</i>", t)
        if t.startswith("- "):
            if not inlist:
                out.append("<ul>"); inlist = True
            out.append(f"<li>{t[2:]}</li>"); continue
        if inlist:
            out.append("</ul>"); inlist = False
        m = re.match(r"(#+) (.*)", t)
        out.append(f"<h{len(m.group(1))}>{m.group(2)}</h{len(m.group(1))}>" if m else (f"<p>{t}</p>" if t.strip() else ""))
    return "\n".join(out + (["</ul>"] if inlist else []))


def cmd_resume(app):
    app = Path(app).resolve()
    cfg = yaml.safe_load((app / "tailor.yml").read_text(encoding="utf-8")) or {}
    v = vault()
    name = v["profile"]["name"].replace(" ", "_")
    if cfg.get("template", "two-column") == "two-column":
        sys.path.insert(0, str(Path(__file__).parent))
        from two_column import render_two_column
        out = app / f"{name}_Resume.html"
        out.write_text(render_two_column(v, cfg, ROOT, pick_bullets, select_certs), encoding="utf-8")
        print(f"Wrote {out.relative_to(ROOT)}  — open in Chrome/Edge → Print → Save as PDF "
              "(Margins: None, Background graphics: on)")
        return
    write_outputs(render(v, cfg, "resume"), app, f"{name}_Resume")   # template: simple


def cmd_cv():
    cfg = load_yaml("cv.yml") or {}
    md = render(vault(), cfg, "cv")
    name = vault()["profile"]["name"].replace(" ", "_")
    write_outputs(md, ROOT / "output", f"{name}_CV")


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a or a[0] not in ("check", "match", "resume", "cv"):
        sys.exit(__doc__)
    {"check": lambda: cmd_check(), "cv": lambda: cmd_cv(),
     "match": lambda: cmd_match(a[1]), "resume": lambda: cmd_resume(a[1])}[a[0]]()
