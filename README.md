# th-file-utils

A lightweight and robust utility package for safe file operations, fast binary comparisons, hashing, and filename sanitization in Python.

## Features & API Reference

### 1. Binary File Writing (`th_file_utils.bin`)

- **`write_bytes(data: bytes, file_path: str | Path) -> bool`**
  - Safely saves bytes data to the specified file path using a context manager. Returns `True` on success, `False` on failure.

### 2. Fast File Comparison (`th_file_utils.comp`)

- **`cmp_is_equal_fast(a: str | Path, b: str | Path, block_size: int = 4096) -> bool`**
  - Compares two files chunk-by-chunk in blocks. Returns `False` immediately if file sizes differ or on the first byte mismatch, making it extremely efficient for large files.

### 3. File Hashing & Verification (`th_file_utils.hash`)

- **`get_file_hash(file_path: str | Path, algo: str = "sha256") -> str`**
  - Calculates and returns the hexadecimal hash string of a file (supports Python 3.14 `hashlib.file_digest` with fallback).
- **`comp_file_hash(file_path: str | Path, hash_code: str) -> bool`**
  - Compares the file's hash value against an expected hash string.

### 4. Filename Sanitization (`th_file_utils.name`)

- **`to_safe_common(text: str) -> str`**
  - Converts Windows-forbidden characters and unwanted symbols into safe alternatives.
- **`safe_name(target: Path) -> Path`**
  - Applies common and OS-specific sanitization to generate a safe path, automatically appending `(1)`, `(2)` if a file collision occurs.

### 5. Safe File Removal & Moving (`th_file_utils.rm`)

- **`safe_remove(file_path: str | Path, dest_dir: str | Path | None = None) -> bool`**
  - Safely deletes a file. If `dest_dir` is specified, moves the file to that directory instead of deleting it.

---

## Installation

```bash
pip install th-file-utils
