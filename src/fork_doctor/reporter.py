"""Report generation for repository health analysis."""

from rich.console import Console
from rich.table import Table

from fork_doctor.analyzer import CHECKS, CHECK_NAMES


def generate_report(results: dict[str, bool], owner: str, repo: str, language: str) -> str:
    """Generate a text report of analysis results."""
    lines = [
        f"Fork Doctor Report: {owner}/{repo}",
        f"Language: {language}",
        "=" * 60,
        "",
    ]
    missing = [c for c in CHECKS if not results[c]]
    for check in CHECKS:
        status = "✅" if results[check] else "❌"
        lines.append(f"  {status}  {CHECK_NAMES[check]}")

    score = len(CHECKS) - len(missing)
    lines.append(f"\nScore: {score}/{len(CHECKS)}")

    if missing:
        lines.append("\nRecommended improvements:")
        for c in missing:
            lines.append(f"  → {CHECK_NAMES[c]}")
    else:
        lines.append("\n🎉 All checks present!")

    return "\n".join(lines)


def print_report(results: dict[str, bool], owner: str, repo: str, language: str) -> None:
    """Print a rich-formatted report to the console."""
    console = Console()

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