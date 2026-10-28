# Career Vault: Yisak Metaferiya

One git-tracked source of truth for your career. Resumes and CVs are **generated** from it, so you never start from a blank page. You update the vault whenever something happens (new project, new cert, new role), commit it, and rebuild.

```
career_roadmap/
├── profile.yml                 name, contact, links, headline + summary per track
├── Education/education.yml
├── Skills/skills.yml           every skill lists the repos that prove it
├── Work-Experience/experience.yml
├── Projects/
│   ├── MegaSeller-Ticketing-API/project.md      ← one folder per project
│   ├── Spring-Boot-APIs/project.md
│   ├── ROAR/  NLP-Sentiment-Analysis/  JMeter-Load-Testing/   (need details)
│   └── …
├── Certifications/certifications.yml  (+ files/ for certificate PDFs)
├── Achievements/achievements.yml
├── applications/
│   ├── _template/              job.md + tailor.yml — copy for each new application
│   └── 2026-10_indeed-…/       one folder per job: JD, tailoring, the resume you sent
├── private/                    passport, DOB, address, photo — git-ignored (see personal.example.yml)
├── cv.yml                      settings for the full CV
├── ROADMAP.md                  where you're going + what to do next
└── tools/
    ├── build.py                the generator
    └── two_column.py           your resume design (header band + photo, two columns, A4)
```

## Setup (once)

```bash
pip install pyyaml          # the only dependency
# optional, for .docx output: install pandoc  (winget install pandoc)
```

## Everyday use

```bash
python tools/build.py check                         # what's still missing / unverified
python tools/build.py cv                            # full CV  -> output/
```

**Applying for a job:**

```bash
cp -r applications/_template applications/2026-11_company-role
# 1. paste the job description into job.md
python tools/build.py match  applications/2026-11_company-role   # ranks your projects for this job
# 2. put the top project ids, track and focus_tags into tailor.yml
python tools/build.py resume applications/2026-11_company-role   # -> .md / .html / .docx
# 3. open the .html in Chrome/Edge -> Print -> Save as PDF
#    (Margins: None, Background graphics: ON). Then:
git add -A && git commit -m "Apply: Company – Role"
```

Git tracks each application's `job.md` + `tailor.yml`, so any resume you sent can be rebuilt exactly; `git log applications/` is your application history. The generated resume files themselves are git-ignored because they contain your passport number and date of birth.

**Privacy:** `private/` (passport, DOB, address, photo) is never committed. If you push this repo to GitHub, keep it private anyway, and remove `passport` from `personal_fields` in tailor.yml unless an employer asks for it.

## Rules that keep the vault trustworthy

- **Nothing invented.** Project bullets were written from the code in each repo. If something isn't in the code, it says `TODO`.
- **Unverified items are never printed.** Certifications and achievements need `verified: true`. Projects need `status: complete`. Skills with `level: TODO` are skipped.
- **Add numbers when you have them** (users, requests/sec, % faster, grade, placement). Numbers are what make a bullet stand out.
- **Commit small and often:** `git commit -m "Add nanoVOLTZ bullets"`.

## Project file format

```yaml
---
id: mega-seller                # used in tailor.yml
title: …
period: 2026
status: complete               # complete | needs-details | archived
repos: [https://github.com/Yisak-E/…]
tags: [backend, java, …]       # matched against job descriptions
stack: [Java 21, Spring Boot, …]
summary: one line (CV only)
bullets:
  - text: Built …
    tags: [concurrency]        # bullets whose tags match focus_tags are chosen first
priority: 1                    # default order on the CV
---
Free notes + STAR interview story (never printed).
```
