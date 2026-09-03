#!/usr/bin/env python3
"""Validate Kimu-style page-numbered PPT prompter scripts."""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path


PAGE_RE = re.compile(r"^【本段P(\d+)】$")
FILLER_PHRASES = (
    "这一篇的核心",
    "接下来我们",
    "首先我们",
    "然后我们",
    "其实本质上",
    "理解这个意思",
    "所以说",
    "大家记住",
    "大家可以",
    "我们会发现",
)


def parse_pages(lines: list[str]) -> tuple[list[tuple[int, list[str]]], list[str]]:
    pages: list[tuple[int, list[str]]] = []
    outside: list[str] = []
    current_number: int | None = None
    current_lines: list[str] = []

    for raw in lines:
        line = raw.strip()
        match = PAGE_RE.match(line)
        if match:
            if current_number is not None:
                pages.append((current_number, current_lines))
            current_number = int(match.group(1))
            current_lines = []
        elif line:
            if current_number is None:
                outside.append(line)
            else:
                current_lines.append(line)

    if current_number is not None:
        pages.append((current_number, current_lines))
    return pages, outside


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("draft", type=Path)
    parser.add_argument("--max-lines", type=int, default=5)
    parser.add_argument("--start", type=int, default=1)
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()

    text = args.draft.read_text(encoding="utf-8")
    pages, outside = parse_pages(text.splitlines())
    errors: list[str] = []
    warnings: list[str] = []

    if not pages:
        errors.append("未找到【本段P数字】页码。")
    if outside:
        errors.append("首个页码前存在可见文本：" + " / ".join(outside[:3]))

    expected = list(range(args.start, args.start + len(pages)))
    actual = [number for number, _ in pages]
    if actual != expected:
        errors.append(f"页码不连续：期望 {expected[:5]}...，实际 {actual[:5]}...")

    for number, content in pages:
        if not content:
            errors.append(f"P{number} 没有内容。")
        if len(content) > args.max_lines:
            errors.append(f"P{number} 有 {len(content)} 行，超过上限 {args.max_lines}。")
        for line in content:
            for phrase in FILLER_PHRASES:
                if phrase in line:
                    warnings.append(f"P{number} 可能含口水词“{phrase}”：{line}")

    occurrences: Counter[str] = Counter(
        line for _, content in pages for line in content if len(line) >= 4
    )
    for line, count in occurrences.most_common():
        if count > 1:
            warnings.append(f"完全重复 {count} 次：{line}")

    print(f"pages={len(pages)} max_lines={max((len(c) for _, c in pages), default=0)}")
    for item in errors:
        print(f"ERROR: {item}")
    for item in warnings:
        print(f"WARN: {item}")

    if errors or (args.strict and warnings):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
