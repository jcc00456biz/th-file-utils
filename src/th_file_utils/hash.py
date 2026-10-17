#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import hashlib
from pathlib import Path


def get_file_hash(file_path: str | Path, algo: str = "sha256") -> str:
    """Calculate and return the hash value of the specified file.

    Args:
        file_path: Path to the target file.
        algo: Hash algorithm name (e.g., "sha256", "md5").

    Returns:
        Hexadecimal string of the calculated hash.
    """
    block_size = 1024
    target = Path(file_path)

    with open(target, "rb") as f:
        if hasattr(hashlib, "file_digest"):
            h_obj = hashlib.file_digest(f, algo)
        else:
            h_obj = hashlib.new(algo)
            while chunk := f.read(block_size):
                h_obj.update(chunk)

    return h_obj.hexdigest()


def comp_file_hash(file_path: str | Path, hash_code: str) -> bool:
    """Compare the file's hash value with the expected hash.

    Args:
        file_path: Path to the target file.
        hash_code: Expected hexadecimal hash string.

    Returns:
        True if hashes match, False otherwise.
    """
    file_hash_code = get_file_hash(file_path)
    return file_hash_code == hash_code
