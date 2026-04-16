"""Tests for Jinja2 template rendering."""

import pytest
from jinja2 import Environment, FileSystemLoader, select_autoescape
from pathlib import Path

TEMPLATE_DIR = Path(__file__).parent.parent / "src" / "fork_doctor" / "templates"
REQUIRED_TEMPLATES = [
    "ci.yml.j2",
    "codeql.yml.j2",
    "dependabot.yml.j2",
    "pre-commit.yaml.j2",
    "issue_template.md.j2",
    "feature_request.md.j2",
    "pr_template.md.j2",
    "contributing.md.j2",
    "release.yml.j2",
    "devcontainer.json.j2",
    "readme_badges.md.j2",
    "benchmark.yml.j2",
    "sbom.yml.j2",
]


@pytest.fixture
def env():
    return Environment(
        loader=FileSystemLoader(str(TEMPLATE_DIR)),
        autoescape=select_autoescape(default_for_filename=False),
    )


def test_all_templates_exist():
    for name in REQUIRED_TEMPLATES:
        assert (TEMPLATE_DIR / name).exists(), f"Missing template: {name}"


@pytest.mark.parametrize("language", ["python", "javascript", "typescript", "go", "rust", "unknown"])
def test_ci_template_renders(env, language):
    tmpl = env.get_template("ci.yml.j2")
    result = tmpl.render(language=language, fork_full="user/repo", repo_name="repo")
    assert "name: CI" in result
    assert "on:" in result


@pytest.mark.parametrize("language", ["python", "javascript", "typescript", "go", "rust"])
def test_codeql_template_renders(env, language):
    tmpl = env.get_template("codeql.yml.j2")
    result = tmpl.render(language=language, fork_full="user/repo", repo_name="repo")
    assert "name: CodeQL" in result


@pytest.mark.parametrize("language", ["python", "javascript", "typescript", "go", "rust"])
def test_dependabot_template_renders(env, language):
    tmpl = env.get_template("dependabot.yml.j2")
    result = tmpl.render(language=language, fork_full="user/repo", repo_name="repo")
    assert "version: 2" in result


@pytest.mark.parametrize("language", ["python", "javascript", "typescript", "go", "rust"])
def test_precommit_template_renders(env, language):
    tmpl = env.get_template("pre-commit.yaml.j2")
    result = tmpl.render(language=language, fork_full="user/repo", repo_name="repo")
    assert "repos:" in result


@pytest.mark.parametrize("language", ["python", "javascript", "typescript", "go", "rust"])
def test_devcontainer_template_renders(env, language):
    tmpl = env.get_template("devcontainer.json.j2")
    result = tmpl.render(language=language, fork_full="user/repo", repo_name="repo")
    assert "name" in result


@pytest.mark.parametrize("language", ["python", "javascript", "typescript", "go", "rust"])
def test_benchmark_template_renders(env, language):
    tmpl = env.get_template("benchmark.yml.j2")
    result = tmpl.render(language=language, fork_full="user/repo", repo_name="repo")
    assert "name: Benchmark" in result


def test_sbom_template_renders(env):
    tmpl = env.get_template("sbom.yml.j2")
    result = tmpl.render(language="python", fork_full="user/repo", repo_name="repo")
    assert "name: SBOM" in result


def test_issue_template_renders(env):
    tmpl = env.get_template("issue_template.md.j2")
    result = tmpl.render(kind="bug")
    assert "Bug report" in result
    result = tmpl.render(kind="feature")
    assert "Feature request" not in result or "bug" not in result.lower()