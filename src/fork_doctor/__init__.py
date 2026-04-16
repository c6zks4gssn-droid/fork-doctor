"""Fork Doctor — Automated fork analysis and structural improvement for GitHub repos."""

__version__ = "0.1.0"
__all__ = ["ForkDoctor"]

from fork_doctor.analyzer import analyze_repo
from fork_doctor.language_detect import detect_language
from fork_doctor.improver import apply_improvements


class ForkDoctor:
    """Analyze and improve GitHub repositories.

    Args:
        repo_url: GitHub repository URL.
        language: Override auto-detected language (python/javascript/typescript/go/rust).
        dry_run: Preview changes without committing.
        verbose: Show detailed output.
    """

    def __init__(
        self,
        repo_url: str,
        language: str | None = None,
        dry_run: bool = False,
        verbose: bool = False,
    ):
        self.repo_url = repo_url
        self.language_override = language
        self.dry_run = dry_run
        self.verbose = verbose
        self._repo_dir: str | None = None
        self._fork_full: str | None = None

    def analyze(self) -> dict[str, bool]:
        """Analyze the repo and return a dict of check -> bool (True = present)."""
        from fork_doctor.cli import _clone_or_fork, _parse_repo_url

        owner, repo = _parse_repo_url(self.repo_url)
        repo_dir, fork_full = _clone_or_fork(
            owner, repo, fork=True, dry_run=self.dry_run, verbose=self.verbose
        )
        self._repo_dir = repo_dir
        self._fork_full = fork_full
        lang = self.language_override or detect_language(repo_dir)
        return analyze_repo(repo_dir)

    def improve(self) -> list[str]:
        """Apply all missing improvements. Returns list of applied improvement names."""
        from fork_doctor.cli import _clone_or_fork, _parse_repo_url

        owner, repo = _parse_repo_url(self.repo_url)
        repo_dir, fork_full = _clone_or_fork(
            owner, repo, fork=True, dry_run=self.dry_run, verbose=self.verbose
        )
        self._repo_dir = repo_dir
        self._fork_full = fork_full
        lang = self.language_override or detect_language(repo_dir)
        results = analyze_repo(repo_dir)
        return apply_improvements(repo_dir, results, lang, fork_full, self.dry_run)

    def report(self) -> dict[str, bool]:
        """Generate a report without forking."""
        from fork_doctor.cli import _clone_or_fork, _parse_repo_url

        owner, repo = _parse_repo_url(self.repo_url)
        repo_dir, _ = _clone_or_fork(
            owner, repo, fork=False, dry_run=self.dry_run, verbose=self.verbose
        )
        self._repo_dir = repo_dir
        lang = self.language_override or detect_language(repo_dir)
        return analyze_repo(repo_dir)