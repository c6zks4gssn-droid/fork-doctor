"""Auto-detect repository language/framework from file extensions."""

from pathlib import Path


def detect_language(repo_dir: str) -> str:
    """Best-effort language detection from file extensions.

    Returns one of: python, javascript, typescript, go, rust, unknown
    """
    exts: dict[str, int] = {}
    for p in Path(repo_dir).rglob("*"):
        if ".git" in p.parts or "node_modules" in p.parts or ".tox" in p.parts:
            continue
        ext = p.suffix
        if ext:
            exts[ext] = exts.get(ext, 0) + 1

    py = exts.get(".py", 0)
    js = exts.get(".js", 0)
    ts = exts.get(".ts", 0) + exts.get(".tsx", 0)
    go = exts.get(".go", 0)
    rs = exts.get(".rs", 0)

    if py >= js and py >= ts and py >= go and py >= rs and py > 0:
        return "python"
    if ts > py and ts >= js:
        return "typescript"
    if js > py and js > 0:
        return "javascript"
    if go > 0:
        return "go"
    if rs > 0:
        return "rust"
    return "unknown"