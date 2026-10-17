#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path


def cmp_is_equal_fast(
    a: str | Path, b: str | Path, block_size: int = 4096
) -> bool:
    """Compare two files quickly in blocks,
    returning False immediately on mismatch.

    Args:
        a: Path to the first file.
        b: Path to the second file.
        block_size: Chunk size for reading (default: 4096 bytes).

    Returns:
        True if contents are identical, False otherwise.
    """
    pa, pb = Path(a), Path(b)

    if pa.stat().st_size != pb.stat().st_size:
        return False

    with pa.open("rb") as fa, pb.open("rb") as fb:
        while True:
            ca = fa.read(block_size)
            cb = fb.read(block_size)

            if not ca:
                return True

            if ca != cb:
                return False
