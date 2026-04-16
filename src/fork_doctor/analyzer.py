"""Core analysis logic for repository health checks."""

from pathlib import Path

CHECKS = [
    "ci", "codeql", "dependabot", "precommit", "issue_templates",
    "pr_templates", "contributing", "semver", "devcontainer",
    "readme_badges", "license", "perf_bench", "sbom",
]

CHECK_NAMES = {
    "ci": "GitHub Actions CI/CD",
    "codeql": "CodeQL Security Scanning",
    "dependabot": "Dependabot Configuration",
    "precommit": "Pre-commit Hooks",
    "issue_templates": "Issue Templates",
    "pr_templates": "PR Templates",
    "contributing": "CONTRIBUTING.md",
    "semver": "Semantic Versioning + Release Automation",
    "devcontainer": "Dev Container Config",
    "readme_badges": "README Improvements (badges, structure)",
    "license": "License Compliance Check",
    "perf_bench": "Performance Benchmarking Setup",
    "sbom": "SBOM Generation Config",
}


def _check_exists(repo_dir: str, path: str) -> bool:
    return (Path(repo_dir) / path).exists()


def analyze_repo(repo_dir: str) -> dict[str, bool]:
    """Analyze a repo and return dict of check -> bool (True = present)."""
    results: dict[str, bool] = {}
    d = Path(repo_dir)
    workflows_dir = d / ".github/workflows"

    # CI
    results["ci"] = _check_exists(repo_dir, ".github/workflows") and any(workflows_dir.glob("*.yml"))

    # CodeQL
    if results["ci"]:
        results["codeql"] = any(
            "codeql" in f.read_text(errors="ignore").lower()
            for f in workflows_dir.glob("*.yml")
        )
    else:
        results["codeql"] = False

    # Dependabot
    results["dependabot"] = (
        _check_exists(repo_dir, ".github/dependabot.yml")
        or _check_exists(repo_dir, ".github/dependabot.yaml")
    )

    # Pre-commit
    results["precommit"] = _check_exists(repo_dir, ".pre-commit-config.yaml")

    # Issue templates
    issue_dir = d / ".github/ISSUE_TEMPLATE"
    results["issue_templates"] = issue_dir.exists() and len(list(issue_dir.glob("*"))) > 0

    # PR templates
    results["pr_templates"] = (
        _check_exists(repo_dir, ".github/PULL_REQUEST_TEMPLATE.md")
        or _check_exists(repo_dir, ".github/pull_request_template.md")
    )

    # Contributing
    results["contributing"] = _check_exists(repo_dir, "CONTRIBUTING.md")

    # Semver / release
    if results["ci"]:
        results["semver"] = any(
            "release" in f.read_text(errors="ignore").lower()
            for f in workflows_dir.glob("*.yml")
        )
    else:
        results["semver"] = False

    # Dev container
    results["devcontainer"] = _check_exists(repo_dir, ".devcontainer/devcontainer.json")

    # README badges
    readme = d / "README.md"
    if readme.exists():
        txt = readme.read_text(errors="ignore")
        results["readme_badges"] = "[!" in txt or "![Build]" in txt or "badge" in txt.lower()
    else:
        results["readme_badges"] = False

    # License
    results["license"] = (
        _check_exists(repo_dir, "LICENSE")
        or _check_exists(repo_dir, "LICENSE.md")
        or _check_exists(repo_dir, "LICENSE.txt")
    )

    # Perf benchmark
    if results["ci"]:
        results["perf_bench"] = (
            _check_exists(repo_dir, "benchmarks")
            or _check_exists(repo_dir, ".github/workflows/benchmark.yml")
            or any(
                "benchmark" in f.read_text(errors="ignore").lower()
                for f in workflows_dir.glob("*.yml")
            )
        )
    else:
        results["perf_bench"] = False

    # SBOM
    if results["ci"]:
        results["sbom"] = any(
            "sbom" in f.read_text(errors="ignore").lower()
            for f in workflows_dir.glob("*.yml")
        )
    else:
        results["sbom"] = False

    return results