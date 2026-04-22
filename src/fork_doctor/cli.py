"""Fork Doctor CLI — Typer-based command line interface."""

import shutil
import subprocess
import sys
import tempfile
import re
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

from fork_doctor import __version__
from fork_doctor.analyzer import CHECKS, CHECK_NAMES, analyze_repo
from fork_doctor.language_detect import detect_language
from fork_doctor.improver import apply_improvements

app = typer.Typer(
    name="fork-doctor",
    help="🏥 Automated fork analysis and structural improvement for GitHub repos.",
    no_args_is_help=True,
    rich_markup_mode="rich",
)
console = Console()


def _run(cmd: str, cwd=None, check=True, capture=True) -> subprocess.CompletedProcess:
    """Run a shell command."""
    kwargs = dict(shell=True, cwd=cwd, text=True)
    if capture:
        kwargs.update(stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    r = subprocess.run(cmd, **kwargs)
    if check and r.returncode != 0:
        console.print(f"[red]ERROR:[/red] {cmd}\n{r.stderr}")
        raise typer.Exit(1)
    return r


def _parse_repo_url(url: str) -> tuple[str, str]:
    """Return (owner, repo) from a GitHub URL."""
    m = re.match(r"https://github\.com/([^/]+)/([^/\s]+?)(?:\.git)?$", url)
    if not m:
        console.print(f"[red]Invalid GitHub URL:[/red] {url}")
        raise typer.Exit(1)
    return m.group(1), m.group(2)


def _gh_fork(owner: str, repo: str) -> str:
    """Fork a repo using gh CLI."""
    r = _run(f"gh repo fork {owner}/{repo} --clone=false", check=False)
    # gh repo fork outputs a full URL like https://github.com/owner/repo
    # Extract owner/repo from the URL
    url_match = re.search(r'https://github\.com/([^/]+/[^/\s]+)', r.stdout.strip())
    if url_match:
        return url_match.group(1).rstrip(']')
    # Fallback: parse owner/repo from any format
    matches = re.findall(r"([\w.-]+/[\w.-]+)", r.stdout.strip())
    if matches:
        for match in matches:
            if repo in match:
                return match
    u = _run("gh api user -q .login", check=True)
    return f"{u.stdout.strip()}/{repo}"


def _clone_and_checkout(repo_full: str, branch: str = "improvements/fork-doctor") -> str:
    """Clone repo to temp dir, create feature branch. Return path."""
    d = tempfile.mkdtemp(prefix="fork-doctor-")
    _run(f"gh repo clone {repo_full} {d}")
    _run(f"git checkout -b {branch}", cwd=d)
    return d


def _clone_only(owner: str, repo: str) -> str:
    """Clone without forking."""
    d = tempfile.mkdtemp(prefix="fork-doctor-report-")
    _run(f"gh repo clone {owner}/{repo} {d}")
    return d


def _clone_or_fork(
    owner: str, repo: str, fork: bool = True, dry_run: bool = False, verbose: bool = False
) -> tuple[str, str]:
    """Clone repo, optionally fork first. Returns (repo_dir, fork_full)."""
    if fork:
        console.print(f"🔍 Forking [bold]{owner}/{repo}[/bold]...")
        fork_full = _gh_fork(owner, repo)
        console.print(f"✅ Forked to [green]{fork_full}[/green]")
        console.print("📂 Cloning and creating branch...")
        repo_dir = _clone_and_checkout(fork_full)
    else:
        fork_full = f"{owner}/{repo}"
        console.print(f"📂 Cloning [bold]{owner}/{repo}[/bold]...")
        repo_dir = _clone_only(owner, repo)
    return repo_dir, fork_full


def _git_commit(repo_dir: str, msg: str) -> bool:
    _run("git add -A", cwd=repo_dir)
    r = _run("git diff --cached --quiet", cwd=repo_dir, check=False, capture=False)
    if r.returncode != 0:
        _run(f'git commit -m "{msg}"', cwd=repo_dir)
        return True
    return False


def version_callback(value: bool):
    if value:
        console.print(f"fork-doctor {__version__}")
        raise typer.Exit()


@app.callback()
def main_callback(
    version: bool = typer.Option(None, "--version", "-v", help="Show version.", callback=version_callback, is_eager=True),
):
    """🏥 Fork Doctor — Automated fork analysis and structural improvement."""


@app.command()
def analyze(
    repo_url: str = typer.Argument(..., help="GitHub repo URL"),
    language: Optional[str] = typer.Option(None, "--language", "-l", help="Override language detection (python/javascript/typescript/go/rust)"),
    verbose: bool = typer.Option(False, "--verbose", "-V", help="Show detailed output"),
):
    """Fork repo and analyze what's missing."""
    owner, repo = _parse_repo_url(repo_url)
    repo_dir, fork_full = _clone_or_fork(owner, repo, fork=True, verbose=verbose)
    lang = language or detect_language(repo_dir)
    console.print(f"🔤 Detected language: [bold]{lang}[/bold]")

    results = analyze_repo(repo_dir)

    table = Table(title="📋 Analysis Results", show_header=True, header_style="bold magenta")
    table.add_column("Status", justify="center")
    table.add_column("Check")
    for check in CHECKS:
        status = "✅" if results[check] else "❌"
        table.add_row(status, CHECK_NAMES[check])

    console.print()
    console.print(table)

    missing = [c for c in CHECKS if not results[c]]
    score = len(CHECKS) - len(missing)
    console.print(f"\n[bold]{score}/{len(CHECKS)}[/bold] checks present, [bold red]{len(missing)}[/bold red] missing")

    shutil.rmtree(repo_dir)


@app.command()
def improve(
    repo_url: str = typer.Argument(..., help="GitHub repo URL"),
    language: Optional[str] = typer.Option(None, "--language", "-l", help="Override language detection"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Preview changes without pushing"),
    verbose: bool = typer.Option(False, "--verbose", "-V", help="Show detailed output"),
):
    """Fork repo and apply all missing improvements."""
    owner, repo = _parse_repo_url(repo_url)
    repo_dir, fork_full = _clone_or_fork(owner, repo, fork=True, dry_run=dry_run, verbose=verbose)
    lang = language or detect_language(repo_dir)
    console.print(f"🔤 Detected language: [bold]{lang}[/bold]")

    results = analyze_repo(repo_dir)
    missing = [c for c in CHECKS if not results[c]]

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), console=console) as progress:
        task = progress.add_task(f"🔧 Applying {len(missing)} improvements...", total=len(missing))
        for check in missing:
            progress.update(task, description=f"➕ Adding {CHECK_NAMES[check]}...")
            apply_improvements(repo_dir, results, lang, fork_full, dry_run)
            if not dry_run:
                _git_commit(repo_dir, f"feat: add {CHECK_NAMES[check]}")
            progress.advance(task)

    if missing and not dry_run:
        console.print("\n🚀 Pushing branch and creating PR...")
        _run("git push -u origin improvements/fork-doctor", cwd=repo_dir)
        body = "Automated improvements by fork-doctor:\n" + "\n".join(f"- {CHECK_NAMES[c]}" for c in missing)
        r = _run(
            f'gh pr create --title "🏥 Fork Doctor: structural improvements" --body "{body}" --base main',
            cwd=repo_dir, check=False
        )
        if r.returncode == 0:
            console.print(f"✅ PR created: [green]{r.stdout.strip()}[/green]")
        else:
            console.print(f"⚠️  PR creation: [yellow]{r.stderr.strip()}[/yellow]")
    elif dry_run:
        console.print("\n[yellow]Dry run — no changes pushed.[/yellow]")
    else:
        console.print("\n🎉 Repo already has all improvements!")

    shutil.rmtree(repo_dir)


@app.command()
def report(
    repo_url: str = typer.Argument(..., help="GitHub repo URL"),
    language: Optional[str] = typer.Option(None, "--language", "-l", help="Override language detection"),
    verbose: bool = typer.Option(False, "--verbose", "-V", help="Show detailed output"),
):
    """Generate a report without forking."""
    owner, repo = _parse_repo_url(repo_url)
    repo_dir, fork_full = _clone_or_fork(owner, repo, fork=False, verbose=verbose)
    lang = language or detect_language(repo_dir)
    console.print(f"🔤 Detected language: [bold]{lang}[/bold]")

    results = analyze_repo(repo_dir)

    table = Table(title=f"📊 Fork Doctor Report: {owner}/{repo}", show_header=True, header_style="bold cyan")
    table.add_column("Status", justify="center")
    table.add_column("Check")
    for check in CHECKS:
        status = "✅" if results[check] else "❌"
        table.add_row(status, CHECK_NAMES[check])

    console.print()
    console.print(table)

    missing = [c for c in CHECKS if not results[c]]
    score = len(CHECKS) - len(missing)
    console.print(f"\n  Score: [bold green]{score}/{len(CHECKS)}[/bold green]")

    if missing:
        console.print("\n  [bold]Recommended improvements:[/bold]")
        for c in missing:
            console.print(f"    → {CHECK_NAMES[c]}")
    else:
        console.print("\n  🎉 [bold green]All checks present![/bold green]")

    shutil.rmtree(repo_dir)