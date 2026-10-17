#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import platform
from pathlib import Path


def safe_name(target: Path) -> Path:
    """Generate a safe file name by
    applying common sanitization and OS-specific rules.

    Appends (1), (2)... if a collision occurs.
    """
    parent = target.parent
    stem = target.stem
    suffix = target.suffix.lower()

    stem = to_safe_common(stem)

    system = platform.system()
    if system != "Windows":
        stem = stem.replace("/", "_")

    normalized = parent / f"{stem}{suffix}"

    if not normalized.exists():
        return normalized

    index = 1
    while True:
        candidate = parent / f"{stem}({index}){suffix}"
        if not candidate.exists():
            return candidate
        index += 1


def to_safe_common(text: str) -> str:
    """Apply common sanitization to text,
    replacing Windows forbidden and unwanted characters."""
    double_excl = "\u203c"
    var_selector = "\ufe0e"
    heart_white = "\u2661"
    heart_black = "\u2665"

    # fmt: off
    trans_table1 = str.maketrans(
        {
            " ": "_",
            ".": "．",
            "\\": "￥",
            "/": "／",
            ":": "：",
            ";": "；",
            ",": "，",
            "*": "＊",
            "?": "？",
            '"': "”",
            "<": "＜",
            ">": "＞",
            "|": "｜",
            "!": "！",
            "&": "＆",
            "%": "％",
            "+": "＋",
            "=": "＝",
            heart_white: "",
            heart_black: "",
        }
    )
    # fmt: on

    trans_table2 = str.maketrans(
        {
            0x203C: "！！",
            0x2048: "？！",
            0x2049: "！？",
        }
    )

    text = text.replace(f"{double_excl}{var_selector}", "！！")
    text = text.translate(trans_table1)
    return text.translate(trans_table2)
