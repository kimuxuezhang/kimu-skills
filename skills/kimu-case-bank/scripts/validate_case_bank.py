#!/usr/bin/env python3
"""Validate a public or private Kimu case-bank layer."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
PUBLIC_ROOT = SKILL_ROOT / "references"
ENTRY_RE = re.compile(
    r"^##\s+(KCB-[PU]\d{3})｜(.+?)\n(.*?)(?=^##\s+KCB-[PU]\d{3}｜|\Z)",
    re.MULTILINE | re.DOTALL,
)
REQUIRED_FIELDS = (
    "类型",
    "优先级",
    "适用主题",
    "核心事实",
    "可用判断",
    "可用表达（非逐字引语）",
    "提词稿压缩",
    "来源",
    "证据状态",
    "使用边界",
    "搜索词",
)
VALID_EVIDENCE = {"已核对", "可追溯", "用户提供", "待核对", "案例方向"}


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate one Kimu case-bank layer.")
    parser.add_argument("--root", type=Path, default=PUBLIC_ROOT)
    parser.add_argument("--layer", choices=("public", "private"), default="public")
    args = parser.parse_args()

    errors: list[str] = []
    root = args.root.expanduser()
    cases_file = root / "cases.md"
    index_file = root / "index.md"
    if not cases_file.exists() or not index_file.exists():
        missing = [str(path) for path in (cases_file, index_file) if not path.exists()]
        print("Validation failed:")
        print(f"- missing files: {', '.join(missing)}")
        return 1

    cases_text = cases_file.read_text(encoding="utf-8")
    index_text = index_file.read_text(encoding="utf-8")
    entries = list(ENTRY_RE.finditer(cases_text))
    ids = [match.group(1) for match in entries]
    expected_prefix = "KCB-P" if args.layer == "public" else "KCB-U"

    if len(ids) != len(set(ids)):
        duplicates = sorted({case_id for case_id in ids if ids.count(case_id) > 1})
        errors.append(f"duplicate IDs: {', '.join(duplicates)}")

    for match in entries:
        case_id, title, body = match.groups()
        if not case_id.startswith(expected_prefix):
            errors.append(f"{case_id}: expected {args.layer} ID prefix {expected_prefix}")
        if not title.strip():
            errors.append(f"{case_id}: empty title")
        for name in REQUIRED_FIELDS:
            if not re.search(rf"^- {re.escape(name)}：", body, re.MULTILINE):
                errors.append(f"{case_id}: missing field {name}")
        evidence = re.search(r"^- 证据状态：(.+)$", body, re.MULTILINE)
        if evidence and evidence.group(1).strip() not in VALID_EVIDENCE:
            errors.append(f"{case_id}: invalid evidence status {evidence.group(1).strip()}")
        if args.layer == "public" and evidence and evidence.group(1).strip() != "已核对":
            errors.append(f"{case_id}: public cases must use evidence status 已核对")

    index_ids = re.findall(r"^\|\s*(KCB-[PU]\d{3})\s*\|", index_text, re.MULTILINE)
    if len(index_ids) != len(set(index_ids)):
        errors.append("index.md contains duplicate IDs")
    missing_index = sorted(set(ids) - set(index_ids))
    missing_cases = sorted(set(index_ids) - set(ids))
    if missing_index:
        errors.append(f"missing from index.md: {', '.join(missing_index)}")
    if missing_cases:
        errors.append(f"index IDs missing from cases.md: {', '.join(missing_cases)}")

    if errors:
        print("Validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        f"Validation passed: layer={args.layer}; {len(entries)} cases; "
        "IDs and index are consistent."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
