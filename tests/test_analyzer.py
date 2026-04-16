"""Tests for the analyzer module."""

import os
import tempfile
from pathlib import Path

import pytest

from fork_doctor.analyzer import analyze_repo, CHECKS, CHECK_NAMES


@pytest.fixture
def empty_repo(tmp_path):
    """Create a minimal empty repo directory."""
    return str(tmp_path)


@pytest.fixture
def full_repo(tmp_path):
    """Create a repo with all checks present."""
    d = tmp_path
    # CI
    (d / ".github/workflows").mkdir(parents=True)
    (d / ".github/workflows/ci.yml").write_text("name: CI\n")
    (d / ".github/workflows/codeql.yml").write_text("name: CodeQL\n")
    (d / ".github/workflows/release.yml").write_text("name: Release\n")
    (d / ".github/workflows/benchmark.yml").write_text("name: Benchmark\n")
    (d / ".github/workflows/sbom.yml").write_text("name: SBOM\n")
    # Dependabot
    (d / ".github/dependabot.yml").write_text("version: 2\n")
    # Pre-commit
    (d / ".pre-commit-config.yaml").write_text("repos: []\n")
    # Issue templates
    (d / ".github/ISSUE_TEMPLATE").mkdir(parents=True)
    (d / ".github/ISSUE_TEMPLATE/bug.md").write_text("bug")
    # PR template
    (d / ".github/PULL_REQUEST_TEMPLATE.md").write_text("## Summary\n")
    # Contributing
    (d / "CONTRIBUTING.md").write_text("# Contributing\n")
    # Dev container
    (d / ".devcontainer").mkdir(parents=True)
    (d / ".devcontainer/devcontainer.json").write_text("{}")
    # README with badges
    (d / "README.md").write_text("# Test\n[![CI](badges)]\n")
    # License
    (d / "LICENSE").write_text("MIT\n")
    # Benchmarks dir
    (d / "benchmarks").mkdir()
    return str(d)


def test_analyze_empty_repo(empty_repo):
    results = analyze_repo(empty_repo)
    assert all(not v for v in results.values()), "Empty repo should fail all checks"


def test_analyze_full_repo(full_repo):
    results = analyze_repo(full_repo)
    assert all(results.values()), f"Full repo should pass all checks, failed: {[k for k, v in results.items() if not v]}"


def test_analyze_partial_repo(tmp_path):
    d = tmp_path
    (d / ".github/workflows").mkdir(parents=True)
    (d / ".github/workflows/ci.yml").write_text("name: CI\n")
    (d / "LICENSE").write_text("MIT\n")
    results = analyze_repo(str(d))
    assert results["ci"] is True
    assert results["license"] is True
    assert results["codeql"] is False
    assert results["dependabot"] is False


def test_checks_constant():
    assert len(CHECKS) == 13
    assert len(CHECK_NAMES) == 13
    assert set(CHECKS) == set(CHECK_NAMES.keys())