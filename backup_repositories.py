#!/usr/bin/env python3

"""
Backup multiple Loop-related repositories.
"""

from typing import List

import tempfile
import os
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path


REPOSITORIES: List[str] = [
    # LoopKit Org Repos
    "https://github.com/LoopKit/Loop.git",
    "https://github.com/LoopKit/loopdocs.git",
    "https://github.com/LoopKit/G4ShareSpy.git",
    "https://github.com/LoopKit/dexcom-share-client-swift.git",
    "https://github.com/LoopKit/CGMBLEKit.git",
    "https://github.com/LoopKit/LoopWorkspace.git",
    "https://github.com/LoopKit/Amplitude-iOS.git",
    "https://github.com/LoopKit/Assets.git",
    "https://github.com/LoopKit/MKRingProgressView.git",
    # Direct Dependencies
    "https://github.com/i-schuetz/SwiftCharts.git",
    "https://github.com/ps2/rileylink_ios.git",
]

SCRIPT_DIRECTORY: Path = Path(__file__).parent.absolute()


def archive_folder(*, source: Path, destination: Path) -> None:
    print(source, destination)
    p = subprocess.Popen(
        [
            "tar",
            "zcvf",
            str(destination.resolve()),
            f"--directory={str(source.parent.resolve())}",
            source.name,
        ],
        stdout=sys.stdout,
        stderr=sys.stderr,
        cwd=source.parent,
    )
    if p.wait() != 0:
        raise Exception("Could not create tarball!")


def clone_repositories(*, archive_directory: Path) -> None:
    for repository in REPOSITORIES:
        print(f"Cloning {repository} ...")
        p = subprocess.Popen(
            ["git", "clone", "--mirror", repository],
            stdout=sys.stdout,
            stderr=sys.stderr,
            cwd=archive_directory,
        )
        if p.wait() != 0:
            raise Exception(f"Failed to clone {repository}")


def main() -> None:
    temp_folder: Path = Path(tempfile.mkdtemp())

    current_date: str = datetime.now().strftime("%Y-%m-%d")
    archive_title = f"loop-backup-{current_date}"

    archive_directory: Path = temp_folder.joinpath(archive_title)
    os.mkdir(archive_directory)

    try:
        clone_repositories(archive_directory=archive_directory)

        destination_file: Path = SCRIPT_DIRECTORY.joinpath(
            f"{archive_title}.tar.gz"
        )
        archive_folder(source=archive_directory, destination=destination_file)

    finally:
        shutil.rmtree(archive_directory)


if __name__ == "__main__":
    main()
