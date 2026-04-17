# 🏥 Fork Doctor

[![CI](https://github.com/fork-doctor/fork-doctor/actions/workflows/ci.yml/badge.svg)](https://github.com/fork-doctor/fork-doctor/actions)
[![PyPI](https://img.shields.io/pypi/v/fork-doctor)](https://pypi.org/project/fork-doctor/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Downloads](https://img.shields.io/pypi/dm/fork-doctor)](https://pypi.org/project/fork-doctor/)

Automated fork analysis and structural improvement for GitHub repositories.

Fork Doctor forks a repo, analyzes what's missing (CI, security scanning, templates, etc.), and optionally creates a PR with all improvements applied.

![Fork Doctor demo](docs/demo.gif)

## ✨ Features

- **12 health checks** — CI, CodeQL, Dependabot, pre-commit, issue/PR templates, CONTRIBUTING, release automation, devcontainers, README badges, license, benchmarks, SBOM
- **Language-aware** — auto-detects Python, JavaScript, TypeScript, Go, Rust and generates appropriate configs
- **Dry-run mode** — preview changes without committing
- **Rich output** — beautiful tables, progress bars, colored terminal output
- **One command** — fork, analyze, improve, and open a PR in seconds

## 📦 Installation

```bash
pip install fork-doctor
```

Or with [uv](https://docs.astral.sh/uv/):

```bash
uv tool install fork-doctor
```

## 🚀 Usage

### Analyze a repo

```bash
fork-doctor analyze https://github.com/owner/repo
```

### Apply improvements

```bash
fork-doctor improve https://github.com/owner/repo
```

### Generate a report (no fork)

```bash
fork-doctor report https://github.com/owner/repo
```

### Options

| Flag | Description |
|------|-------------|
| `--dry-run` | Preview changes without committing or pushing |
| `--language <lang>` | Override auto-detected language (python/javascript/typescript/go/rust) |
| `--verbose` | Show detailed output |

### Programmatic usage

```python
from fork_doctor import ForkDoctor

fd = ForkDoctor("https://github.com/owner/repo")
results = fd.analyze()
print(results)
# {'ci': True, 'codeql': False, 'dependabot': False, ...}
```

## 📋 What It Checks

| # | Check | Description |
|---|-------|-------------|
| 1 | CI | GitHub Actions CI/CD pipeline |
| 2 | CodeQL | CodeQL security scanning |
| 3 | Dependabot | Automated dependency updates |
| 4 | Pre-commit | Pre-commit hook configuration |
| 5 | Issue Templates | Structured issue templates |
| 6 | PR Templates | Pull request templates |
| 7 | Contributing | CONTRIBUTING.md guide |
| 8 | Release | Semantic versioning + release automation |
| 9 | DevContainer | Dev container configuration |
| 10 | README Badges | Badges and improved structure |
| 11 | License | License file and compliance |
| 12 | Benchmark | Performance benchmarking setup |
| 13 | SBOM | Software Bill of Materials generation |

## 🛠️ Requirements

- Python 3.9+
- `gh` CLI authenticated (`gh auth login`)
- Git configured

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines. Bug reports and pull requests welcome!

## 📄 License

[MIT](LICENSE)

## 🔖 GitHub Topics

`python` `github` `repository-health` `devops` `automation` `ci-cd` `security` `sbom`