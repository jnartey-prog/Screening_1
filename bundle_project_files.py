"""Bundle project structure and selected source files into one text file."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable, List, Sequence

# Easy to extend later, e.g. {".py", ".md", ".yaml"}
INCLUDED_EXTENSIONS = {".py"}

EXCLUDED_NAMES = {
    ".git",
    "__pycache__",
    ".pytest_cache",
    "venv",
    ".venv",
    "env",
    "node_modules",
    "build",
    "dist",
    ".idea",
    ".vscode",
    ".mypy_cache",
    ".ruff_cache",
}

DEFAULT_OUTPUT = "project_code_bundle.txt"
SEPARATOR = "=" * 100


def is_excluded(path: Path) -> bool:
    """Return True if any part of the path matches an excluded name."""
    return any(part in EXCLUDED_NAMES for part in path.parts)


def iter_paths(root: Path) -> Iterable[Path]:
    """Yield all non-excluded paths under root, recursively, in sorted order."""
    for entry in sorted(root.iterdir(), key=lambda p: p.name.lower()):
        if is_excluded(entry.relative_to(root)):
            continue
        yield entry
        if entry.is_dir():
            yield from _iter_paths_recursive(entry, root)


def _iter_paths_recursive(current: Path, root: Path) -> Iterable[Path]:
    """Recursive helper for iter_paths."""
    for entry in sorted(current.iterdir(), key=lambda p: p.name.lower()):
        rel = entry.relative_to(root)
        if is_excluded(rel):
            continue
        yield entry
        if entry.is_dir():
            yield from _iter_paths_recursive(entry, root)


def collect_tree_lines(root: Path) -> List[str]:
    """Build a tree-style list of relative paths for the project structure."""
    lines: List[str] = [root.name or "."]
    for path in iter_paths(root):
        rel = path.relative_to(root)
        depth = len(rel.parts)
        indent = "    " * depth
        suffix = "/" if path.is_dir() else ""
        lines.append(f"{indent}- {rel.name}{suffix}")
    return lines


def collect_source_files(root: Path, extensions: Sequence[str]) -> List[Path]:
    """Collect source files under root matching the given extensions."""
    normalized_exts = {ext.lower() if ext.startswith(".") else f".{ext.lower()}" for ext in extensions}
    files: List[Path] = []
    for path in iter_paths(root):
        if path.is_file() and path.suffix.lower() in normalized_exts:
            files.append(path)
    return sorted(files, key=lambda p: str(p.relative_to(root)).lower())


def write_bundle(root: Path, output_file: Path, extensions: Sequence[str]) -> int:
    """Write project structure and source file contents to the bundle file.

    Returns:
        int: Number of files successfully bundled.
    """
    tree_lines = collect_tree_lines(root)
    source_files = collect_source_files(root, extensions)

    print(f"Scanning root: {root}")
    print(f"Matched source files: {len(source_files)}")
    print(f"Writing bundle: {output_file}")

    bundled_count = 0
    with output_file.open("w", encoding="utf-8") as out:
        out.write("PROJECT STRUCTURE\n")
        out.write(SEPARATOR + "\n")
        out.write("\n".join(tree_lines))
        out.write("\n\n")

        out.write("FILE CONTENTS\n")
        out.write(SEPARATOR + "\n\n")

        for index, file_path in enumerate(source_files, start=1):
            rel = file_path.relative_to(root)
            print(f"[{index}/{len(source_files)}] Bundling: {rel}")
            out.write(SEPARATOR + "\n")
            out.write(f"FILE: {rel.as_posix()}\n")
            out.write(SEPARATOR + "\n")
            try:
                content = file_path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                try:
                    content = file_path.read_text(encoding="latin-1")
                except Exception as exc:  # noqa: BLE001
                    print(f"  Error reading {rel}: {exc}")
                    out.write(f"[ERROR] Could not read file: {exc}\n\n")
                    continue
            except Exception as exc:  # noqa: BLE001
                print(f"  Error reading {rel}: {exc}")
                out.write(f"[ERROR] Could not read file: {exc}\n\n")
                continue

            out.write(content)
            if not content.endswith("\n"):
                out.write("\n")
            out.write("\n")
            bundled_count += 1

    print(f"Done. Total files bundled: {bundled_count}")
    return bundled_count


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Create a single text bundle with project structure and selected source file contents."
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path("."),
        help="Project root directory to scan (default: current directory).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(DEFAULT_OUTPUT),
        help=f"Output bundle file (default: {DEFAULT_OUTPUT}).",
    )
    parser.add_argument(
        "--ext",
        action="append",
        default=None,
        help="File extension to include (repeatable). Example: --ext .py --ext .md",
    )
    return parser.parse_args()


def main() -> None:
    """Entry point for script execution."""
    args = parse_args()
    root = args.root.resolve()
    output = args.output.resolve()
    extensions = args.ext if args.ext else sorted(INCLUDED_EXTENSIONS)

    if not root.exists() or not root.is_dir():
        raise SystemExit(f"Invalid root directory: {root}")

    write_bundle(root=root, output_file=output, extensions=extensions)


if __name__ == "__main__":
    main()
