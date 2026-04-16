"""Tests for the CLI module."""

from unittest.mock import patch
import pytest
from typer.testing import CliRunner

from fork_doctor.cli import app

runner = CliRunner()


def test_version():
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert "0.1.0" in result.stdout


def test_no_args_shows_help():
    result = runner.invoke(app)
    assert result.exit_code == 0
    assert "fork-doctor" in result.output.lower() or "Usage" in result.output