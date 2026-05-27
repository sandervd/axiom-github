#!/usr/bin/env python3
"""Backfill schema paths expected by axiom-cli 0.1.0."""

from __future__ import annotations

import shutil
from pathlib import Path

import axiom_cli


def copy_if_missing(source: Path, destination: Path) -> None:
    if not source.is_file():
        return
    if destination.is_file():
        return
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, destination)
    print(f"Created Axiom schema compatibility file {destination}")


def main() -> None:
    package_dir = Path(axiom_cli.__file__).parent
    install_root = package_dir.parent

    copy_if_missing(
        package_dir / "model" / "repository_schema.yaml",
        install_root / "src" / "axiom" / "model" / "repository_schema.yaml",
    )

    for source in package_dir.glob("distribution_type/*/distribution_type_*.yaml"):
        relative = source.relative_to(package_dir)
        copy_if_missing(source, install_root / "src" / "axiom_cli" / relative)


if __name__ == "__main__":
    main()
