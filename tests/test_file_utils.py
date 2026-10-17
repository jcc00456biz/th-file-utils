#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path

from th_file_utils.bin import write_bytes
from th_file_utils.comp import cmp_is_equal_fast
from th_file_utils.hash import comp_file_hash, get_file_hash
from th_file_utils.name import safe_name, to_safe_common
from th_file_utils.rm import safe_remove


def test_write_bytes(tmp_path: Path) -> None:
    """bin.write_bytes のテスト"""
    target_file = tmp_path / "test.bin"
    data = b"Hello, Python 3.14!"

    # 正常系: 書き込み成功
    assert write_bytes(data, target_file) is True
    assert target_file.exists()

    with target_file.open("rb") as f:
        assert f.read() == data

    # 異常系: 存在しない不正なパスへの書き込み
    invalid_file = tmp_path / "nonexistent_dir" / "test.bin"
    assert write_bytes(data, invalid_file) is False


def test_cmp_is_equal_fast(tmp_path: Path) -> None:
    """comp.cmp_is_equal_fast のテスト"""
    file_a = tmp_path / "a.bin"
    file_b = tmp_path / "b.bin"
    file_c = tmp_path / "c.bin"

    write_bytes(b"same content", file_a)
    write_bytes(b"same content", file_b)
    write_bytes(b"different content", file_c)
    write_bytes(b"too short", tmp_path / "short.bin")

    # 同一内容ファイルの一致確認
    assert cmp_is_equal_fast(file_a, file_b) is True

    # 異なる内容ファイルの不一致確認
    assert cmp_is_equal_fast(file_a, file_c) is False

    # サイズが異なる場合の高速不一致確認
    assert cmp_is_equal_fast(file_a, tmp_path / "short.bin") is False


def test_hash_functions(tmp_path: Path) -> None:
    """hash.get_file_hash および hash.comp_file_hash のテスト"""
    target_file = tmp_path / "hash.bin"
    content = b"hash verification target"
    write_bytes(content, target_file)

    # 既知のSHA256ハッシュ値計算
    expected_hash = get_file_hash(target_file, "sha256")
    assert isinstance(expected_hash, str)
    assert len(expected_hash) == 64

    # ハッシュ一致検証
    assert comp_file_hash(target_file, expected_hash) is True
    assert comp_file_hash(target_file, "0" * 64) is False


def test_name_safe_common() -> None:
    """name.to_safe_common のテスト"""
    raw_text = 'test file name?*<>"|&%+= \u2661\u2665'
    sanitized = to_safe_common(raw_text)

    assert "?" not in sanitized
    assert "*" not in sanitized
    assert "<" not in sanitized
    assert ">" not in sanitized
    assert "_" in sanitized

    excl_text = "\u203c?"
    # \u203c (‼) は ！！ に変換され、? は ？ に変換されるため ！！？ になる
    assert to_safe_common(excl_text) == "！！？"


def test_name_safe_name(tmp_path: Path) -> None:
    """name.safe_name のテスト"""
    target = tmp_path / "test file?.txt"
    resolved = safe_name(target)

    assert "?" not in resolved.name
    assert "_" in resolved.name

    # 既存ファイルの衝突回避確認（安全化されたパスに対して作成する）
    resolved.touch()
    resolved_conflict = safe_name(target)
    assert "(1)" in resolved_conflict.name


def test_safe_remove(tmp_path: Path) -> None:
    """rm.safe_remove のテスト（削除および移動）"""
    target_file = tmp_path / "remove_target.txt"
    write_bytes(b"delete me", target_file)

    # 正常系: 削除
    assert safe_remove(target_file) is True
    assert not target_file.exists()

    # 異常系: 存在しないファイルの削除
    assert safe_remove(target_file) is False

    # 正常系: 移動（dest_dir 指定）
    move_file = tmp_path / "move_target.txt"
    write_bytes(b"move me", move_file)
    dest_dir = tmp_path / "backup"

    assert safe_remove(move_file, dest_dir) is True
    assert not move_file.exists()
    assert (dest_dir / "move_target.txt").exists()
