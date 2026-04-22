# Fork Doctor Launch Content

## HackerNews (Show HN)

**Title:** Show HN: Fork Doctor – Automatically improve any GitHub repo's infrastructure

**Body:**

I got tired of forking repos only to find they were missing CI, security scanning, dependabot, pre-commit hooks, and a dozen other infrastructure basics. So I built Fork Doctor.

It analyzes any GitHub repo against 13 infrastructure checks, then auto-generates the missing pieces:

- GitHub Actions CI/CD (language-aware: Python, JS/TS, Go, Rust)
- CodeQL security scanning
- Dependabot configuration
- Pre-commit hooks
- Issue & PR templates
- CONTRIBUTING.md
- Semantic versioning + release automation
- Dev containers
- README badges
- License compliance
- Performance benchmarks
- SBOM generation

Usage:

```
pip install fork-doctor
fork-doctor analyze https://github.com/user/repo
fork-doctor improve https://github.com/user/repo  # forks + adds everything
fork-doctor report https://github.com/user/repo    # health report without forking
```

Example: OpenClaw scored 10/13 → 13/13 after running fork-doctor improve.

The existing tools in this space (repocheckai at 109 stars) are AI-powered analysis only — they tell you what's wrong but don't fix it. Fork Doctor actually generates the files and commits them.

Built with Python, Typer, Rich, and Jinja2 templates. Language detection is automatic.

GitHub: https://github.com/c6zks4gssn-droid/fork-doctor

Feedback welcome!

---

## Reddit (r/Python)

**Title:** 🩺 Fork Doctor – automatically add CI, security scanning, Dependabot, and 9 more infra checks to any GitHub repo

**Body:**

Hey r/Python,

I built Fork Doctor because every time I fork a repo, I find it's missing basic infrastructure — no CI, no Dependabot, no pre-commit hooks, no CONTRIBUTING.md.

Fork Doctor analyzes repos against 13 checks and auto-generates whatever's missing:

```bash
pip install fork-doctor
fork-doctor analyze https://github.com/user/repo
```

What it adds (with language-aware templates for Python, JS/TS, Go, and Rust):

1. GitHub Actions CI/CD
2. CodeQL security scanning
3. Dependabot
4. Pre-commit hooks (ruff, black, isort, mypy for Python)
5. Issue & PR templates
6. CONTRIBUTING.md
7. Release automation
8. Dev containers
9. README badges
10. License check
11. Performance benchmarks
12. SBOM generation

It actually creates the files, commits them on a feature branch, and opens a PR. Not just analysis — actual fixes.

```bash
fork-doctor improve https://github.com/user/repo  # fork + improve + PR
fork-doctor report https://github.com/user/repo    # just the report
```

Open source, MIT licensed: https://github.com/c6zks4gssn-droid/fork-doctor

Would love feedback on what checks to add next!

---

## Reddit (r/github)

**Title:** Built a tool that auto-improves GitHub repos — adds CI, security scanning, Dependabot, and more

**Body:**

Same content as r/Python but framed more for GitHub users/devops.

---

## LinkedIn

🩺 Just open-sourced Fork Doctor — a CLI that automatically improves any GitHub repo's infrastructure.

Fork a repo → run one command → get CI, security scanning, Dependabot, pre-commit hooks, templates, benchmarks, and SBOM generation added automatically.

13 checks, language-aware templates (Python, JS/TS, Go, Rust), and it creates actual files + opens a PR.

Check it out: https://github.com/c6zks4gssn-droid/fork-doctor

#OpenSource #DevOps #GitHub #Python #Automation