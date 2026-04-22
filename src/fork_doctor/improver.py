"""Auto-improvement logic — applies missing improvements using Jinja2 templates."""

from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape

from fork_doctor.analyzer import CHECKS

TEMPLATE_DIR = Path(__file__).parent / "templates"
_env = Environment(
    loader=FileSystemLoader(str(TEMPLATE_DIR)),
    autoescape=select_autoescape(),
)


def _mkdir(repo_dir: str | Path, path: str) -> None:
    Path(repo_dir / path).mkdir(parents=True, exist_ok=True)


def _write(repo_dir: str | Path, rel_path: str, content: str) -> None:
    p = Path(repo_dir) / rel_path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content)


def apply_improvements(
    repo_dir: str,
    results: dict[str, bool],
    language: str,
    fork_full: str,
    dry_run: bool = False,
) -> list[str]:
    """Apply all missing improvements. Returns list of applied check names."""
    applied = []
    missing = [c for c in CHECKS if not results.get(c, False)]

    for check in missing:
        _apply_check(repo_dir, check, language, fork_full, dry_run)
        applied.append(check)

    return applied


def _apply_check(repo_dir: str | Path, check: str, language: str, fork_full: str, dry_run: bool) -> None:
    """Apply a single check improvement."""
    template_map = {
        "ci": "ci.yml.j2",
        "codeql": "codeql.yml.j2",
        "dependabot": "dependabot.yml.j2",
        "precommit": "pre-commit.yaml.j2",
        "issue_templates": "issue_template.md.j2",
        "pr_templates": "pr_template.md.j2",
        "contributing": "contributing.md.j2",
        "semver": "release.yml.j2",
        "devcontainer": "devcontainer.json.j2",
        "readme_badges": "readme_badges.md.j2",
        "license": None,  # Handled specially
        "perf_bench": "benchmark.yml.j2",
        "sbom": "sbom.yml.j2",
    }

    template_name = template_map.get(check)
    ctx = {"language": language, "fork_full": fork_full, "repo_name": fork_full.split("/")[-1]}

    if check == "license":
        _apply_license(repo_dir, dry_run)
        return

    if check == "issue_templates":
        _apply_issue_templates(repo_dir, dry_run)
        return

    if check == "readme_badges":
        _apply_readme_badges(repo_dir, fork_full, dry_run)
        return

    if template_name is None:
        return

    if dry_run:
        return

    tmpl = _env.get_template(template_name)
    content = tmpl.render(**ctx)

    # Map check to output path
    path_map = {
        "ci": ".github/workflows/ci.yml",
        "codeql": ".github/workflows/codeql.yml",
        "dependabot": ".github/dependabot.yml",
        "precommit": ".pre-commit-config.yaml",
        "pr_templates": ".github/PULL_REQUEST_TEMPLATE.md",
        "contributing": "CONTRIBUTING.md",
        "semver": ".github/workflows/release.yml",
        "devcontainer": ".devcontainer/devcontainer.json",
        "perf_bench": ".github/workflows/benchmark.yml",
        "sbom": ".github/workflows/sbom.yml",
    }

    output_path = path_map.get(check)
    if output_path:
        _write(repo_dir, output_path, content)


def _apply_license(repo_dir: str | Path, dry_run: bool) -> None:
    if dry_run:
        return
    _write(repo_dir, "LICENSE", LICENSE_TEXT)


def _apply_issue_templates(repo_dir: str | Path, dry_run: bool) -> None:
    if dry_run:
        return
    tmpl_bug = _env.get_template("issue_template.md.j2")
    tmpl_feat = _env.get_template("feature_request.md.j2")
    _write(repo_dir, ".github/ISSUE_TEMPLATE/bug_report.md", tmpl_bug.render(kind="bug"))
    _write(repo_dir, ".github/ISSUE_TEMPLATE/feature_request.md", tmpl_feat.render(kind="feature"))


def _apply_readme_badges(repo_dir: str | Path, fork_full: str, dry_run: bool) -> None:
    if dry_run:
        return
    readme = Path(repo_dir) / "README.md"
    if not readme.exists():
        readme.write_text(f"# {Path(repo_dir).name}\n\n")
    txt = readme.read_text()
    if "[!" in txt:
        return
    badge_lines = (
        f"\n[![CI](https://github.com/{fork_full}/actions/workflows/ci.yml/badge.svg)]"
        f"(https://github.com/{fork_full}/actions)\n"
        f"[![CodeQL](https://github.com/{fork_full}/actions/workflows/codeql.yml/badge.svg)]"
        f"(https://github.com/{fork_full}/security/code-scanning)\n"
        f"[![Dependabot](https://img.shields.io/badge/dependabot-enabled-blue)](.github/dependabot.yml)\n\n"
    )
    lines = txt.split("\n")
    insert = 1
    for i, line in enumerate(lines):
        if line.startswith("#"):
            insert = i + 1
            break
    lines.insert(insert, badge_lines)
    for s in ["## Installation", "## Usage", "## Contributing", "## License"]:
        if s not in txt:
            lines.append(f"\n{s}\n\n_TBD_\n")
    readme.write_text("\n".join(lines))


LICENSE_TEXT = """MIT License

Copyright (c) 2026

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""