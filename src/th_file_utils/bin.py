#!/usr/init/env python3
# -*- coding: utf-8 -*-
from pathlib import Path


def write_bytes(data: bytes, file_path: str | Path) -> bool:
    """Save bytes data to the specified file path. Returns False on failure.

    Args:
        data: The bytes data to save.
        file_path: The target file path (str or Path).

    Returns:
        True: Successfully saved.
        False: Failed (exception raised).
    """
    try:
        path = Path(file_path)
        with path.open("wb") as f:
            f.write(data)
        return True
    except Exception:
        return False
