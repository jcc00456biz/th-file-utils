#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import shutil
from pathlib import Path


def safe_remove(
    file_path: str | Path, dest_dir: str | Path | None = None
) -> bool:
    """Safely remove a file,
    or move it to the destination directory if specified.

    Args:
        file_path: Path to the target file.
        dest_dir: Destination directory
        for moving instead of deleting (deletes if None).

    Returns:
        True: Removal or movement succeeded.
        False: Failed (exception raised).
    """
    try:
        src = Path(file_path)

        if not src.exists():
            return False

        if dest_dir is None:
            src.unlink()
            return True

        dst = Path(dest_dir)
        dst.mkdir(parents=True, exist_ok=True)

        shutil.move(str(src), str(dst))
        return True

    except Exception:
        return False
