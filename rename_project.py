"""
Rename this Django project to a new name. Use when reusing this template for a new project.

Usage:
    python rename_project.py <new_project_name>

Examples:
    python rename_project.py my_app
    python rename_project.py my-app      # hyphens become underscores
    python rename_project.py "Acme Corp" # spaces/special chars become underscores

The new name is normalized to a valid Python module name (lowercase, alphanumeric + underscores).
"""

import argparse
import re
import shutil
import sys
from pathlib import Path


# Current project package name (Python module)
CURRENT_NAME = "django_saas_template"

# Directories to skip when scanning for text replacement
SKIP_DIRS = {".git", ".venv", "venv", "env", "__pycache__", ".mypy_cache", ".pytest_cache", "node_modules"}

# Files to skip (e.g. this script, binary files)
SKIP_FILES = {"rename_project.py"}


def normalize_project_name(name: str) -> str:
    """Convert input to a valid Python module name: lowercase, alphanumeric and underscores only."""
    if not name or not name.strip():
        raise ValueError("Project name cannot be empty.")
    # Replace hyphens and spaces with underscores, then keep only valid identifier chars
    normalized = re.sub(r"[-.\s]+", "_", name.strip())
    normalized = re.sub(r"\W", "", normalized)
    normalized = normalized.lower()
    if not normalized:
        raise ValueError(
            "Project name must contain at least one letter or number. "
            f"Got: {name!r}"
        )
    return normalized


def find_project_root() -> Path:
    """Project root is the directory containing manage.py and the config package."""
    script_dir = Path(__file__).resolve().parent
    if (script_dir / "manage.py").exists() and (script_dir / CURRENT_NAME).is_dir():
        return script_dir
    raise SystemExit(
        "Error: Could not find project root (manage.py and django_saas_template/). "
        "Run this script from the project root."
    )


def should_skip(path: Path, root: Path) -> bool:
    """Whether to skip this path when scanning or renaming."""
    try:
        rel = path.relative_to(root)
    except ValueError:
        return True
    parts = rel.parts
    if not parts:
        return False
    if parts[0] in SKIP_DIRS:
        return True
    if path.name in SKIP_FILES:
        return True
    if path.suffix in {".pyc", ".pyo", ".so", ".egg", ".whl"}:
        return True
    return False


def replace_in_file(file_path: Path, old: str, new: str) -> bool:
    """Replace old with new in file; return True if file was modified."""
    try:
        text = file_path.read_text(encoding="utf-8", errors="replace")
    except OSError as e:
        print(f"  Warning: Could not read {file_path}: {e}", file=sys.stderr)
        return False
    if old not in text:
        return False
    new_text = text.replace(old, new)
    try:
        file_path.write_text(new_text, encoding="utf-8")
    except OSError as e:
        print(f"  Warning: Could not write {file_path}: {e}", file=sys.stderr)
        return False
    return True


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Rename the Django project to a new name (for template reuse)."
    )
    parser.add_argument(
        "name",
        help="New project name (e.g. my_app, my-app). Will be normalized to a valid Python module name.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without making changes.",
    )
    args = parser.parse_args()

    try:
        new_name = normalize_project_name(args.name)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    if new_name == CURRENT_NAME:
        print(f"Project is already named {CURRENT_NAME}. Nothing to do.")
        sys.exit(0)

    root = find_project_root()
    config_dir = root / CURRENT_NAME
    new_config_dir = root / new_name

    if new_config_dir.exists():
        print(f"Error: Target directory already exists: {new_config_dir}", file=sys.stderr)
        sys.exit(1)

    dry = args.dry_run
    if dry:
        print("DRY RUN — no changes will be made.\n")

    # 1) Replace in file contents (including files inside the config package)
    updated = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if should_skip(path, root):
            continue
        try:
            content = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if CURRENT_NAME in content:
            if dry:
                print(f"Would update: {path.relative_to(root)}")
            elif replace_in_file(path, CURRENT_NAME, new_name):
                updated.append(path.relative_to(root))
    if updated:
        print("Updated references in:", ", ".join(str(p) for p in updated))

    # 2) Rename the config package directory
    if dry:
        print(f"Would rename: {config_dir.name} -> {new_name}")
    else:
        shutil.move(str(config_dir), str(new_config_dir))
        print(f"Renamed: {config_dir.name} -> {new_name}")

    if dry:
        print("\nRun without --dry-run to apply changes.")
    else:
        print(f"\nProject renamed to '{new_name}'. Next steps:")
        print("  - Update .env / .env.example with your DATABASE_URL if needed.")
        print("  - Run: python manage.py check")


if __name__ == "__main__":
    main()
