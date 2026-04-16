# Fork Doctor — Usage Guide

## Installation

```bash
pip install fork-doctor
```

## Quick Start

### Analyze a repository

```bash
fork-doctor analyze https://github.com/owner/repo
```

This forks the repo, clones it, runs 13 health checks, and prints a detailed report.

### Improve a repository

```bash
fork-doctor improve https://github.com/owner/repo
```

This forks the repo, applies all missing improvements, pushes a branch, and opens a PR.

### Generate a report (no fork)

```bash
fork-doctor report https://github.com/owner/repo
```

This clones the repo (no fork) and prints a health report.

## Options

| Flag | Short | Description |
|------|-------|-------------|
| `--language` | `-l` | Override auto-detected language (python, javascript, typescript, go, rust) |
| `--dry-run` | | Preview changes without committing or pushing |
| `--verbose` | `-V` | Show detailed output |
| `--version` | `-v` | Show version |

## Programmatic Usage

```python
from fork_doctor import ForkDoctor

fd = ForkDoctor("https://github.com/owner/repo")

# Analyze
results = fd.analyze()
print(results)
# {'ci': True, 'codeql': False, ...}

# Improve
applied = fd.improve()
print(applied)
# ['codeql', 'dependabot', ...]

# Report
report = fd.report()
print(report)
```

## Language Detection

Fork Doctor auto-detects the primary language from file extensions:

| Language | Extensions |
|----------|-----------|
| Python | `.py` |
| JavaScript | `.js` |
| TypeScript | `.ts`, `.tsx` |
| Go | `.go` |
| Rust | `.rs` |

Override with `--language python` if detection is incorrect.

## The 13 Health Checks

1. **CI** — GitHub Actions CI/CD pipeline
2. **CodeQL** — Security scanning
3. **Dependabot** — Automated dependency updates
4. **Pre-commit** — Git hook configuration
5. **Issue Templates** — Structured issue forms
6. **PR Templates** — Pull request templates
7. **CONTRIBUTING.md** — Contribution guide
8. **Release** — Semantic versioning & release automation
9. **DevContainer** — Dev container configuration
10. **README Badges** — Status badges and improved structure
11. **License** — License file & compliance
12. **Benchmark** — Performance benchmarking
13. **SBOM** — Software Bill of Materials generation