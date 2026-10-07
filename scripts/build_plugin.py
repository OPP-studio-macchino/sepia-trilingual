#!/usr/bin/env python3
"""Build the skills-only ZIP from a Git checkout, using only the standard library.

Run: python3 scripts/build_plugin.py
Only tracked skill resources and the explicit package files below are included.
ZIP entries have fixed timestamps and permissions and are stored uncompressed
so identical inputs produce identical bytes across platforms.
"""

import json
import subprocess
import zipfile
from pathlib import Path

import check_versions


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_FILES = (
    "plugin.json",
    ".codex-plugin/plugin.json",
    "LICENSE",
    "ATTRIBUTION.md",
    "CHATGPT.md",
    "examples/voice-profile.example.yaml",
    "assets/sepia-user-icon-128.png",
    "assets/sepia-user-icon-256.png",
    "assets/sepia-user-icon-512.png",
)


def build(output_dir=ROOT / "dist"):
    code, report = check_versions.run(ROOT)
    if code:
        raise ValueError(report)
    tracked = subprocess.check_output(
        ["git", "ls-files", "-z", "--", "skills"], cwd=ROOT
    ).decode("utf-8").split("\0")
    paths = sorted(set(PACKAGE_FILES) | {name for name in tracked if name})
    for name in paths:
        path = ROOT / name
        if (not path.is_file() or path.resolve() != path.absolute()
                or any(part.startswith(".") for part in path.relative_to(ROOT).parts
                       if part != ".codex-plugin")):
            raise ValueError(f"Missing, symlinked, or hidden package file: {name}")

    version = json.loads((ROOT / "plugin.json").read_text(encoding="utf-8"))["version"]
    output_dir.mkdir(parents=True, exist_ok=True)
    output = output_dir / f"sepia-trilingual-{version}-skills-only.zip"
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_STORED) as archive:
        for name in paths:
            entry = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            entry.create_system = 3
            entry.external_attr = 0o100644 << 16
            archive.writestr(entry, (ROOT / name).read_bytes())
    return output


if __name__ == "__main__":
    print(build())
