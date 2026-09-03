#!/usr/bin/env python3
"""Search the Markdown Kimu case bank with lightweight keyword ranking."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
CASES_FILE = SKILL_ROOT / "references" / "cases.md"
ENTRY_RE = re.compile(
    r"^##\s+(KCB-\d{3})｜(.+?)\n(.*?)(?=^##\s+KCB-\d{3}｜|\Z)",
    re.MULTILINE | re.DOTALL,
)


def field(body: str, name: str) -> str:
    match = re.search(rf"^- {re.escape(name)}：(.+)$", body, re.MULTILINE)
    return match.group(1).strip() if match else ""


def query_terms(raw: str) -> list[str]:
    terms = [part.lower() for part in re.split(r"[\s,，;；、/]+", raw) if part.strip()]
    if len(terms) == 1 and len(terms[0]) >= 6:
        # Keep the complete Chinese phrase and add bigrams for unspaced queries.
        text = terms[0]
        terms.extend(text[i : i + 2] for i in range(len(text) - 1))
    return list(dict.fromkeys(terms))


def load_entries() -> list[dict[str, str]]:
    text = CASES_FILE.read_text(encoding="utf-8")
    entries = []
    for match in ENTRY_RE.finditer(text):
        case_id, title, body = match.groups()
        entries.append(
            {
                "id": case_id,
                "title": title.strip(),
                "type": field(body, "类型"),
                "priority": field(body, "优先级"),
                "topics": field(body, "适用主题"),
                "evidence": field(body, "证据状态"),
                "source": field(body, "来源"),
                "search_terms": field(body, "搜索词"),
                "body": body.strip(),
            }
        )
    return entries


def score(entry: dict[str, str], terms: list[str]) -> int:
    title = entry["title"].lower()
    topics = entry["topics"].lower()
    tags = entry["search_terms"].lower()
    body = entry["body"].lower()
    total = 0
    for term in terms:
        if term in title:
            total += 8
        if term in topics:
            total += 5
        if term in tags:
            total += 4
        if term in body:
            total += min(body.count(term), 3)
    try:
        total += max(0, 5 - int(entry["priority"]))
    except ValueError:
        pass
    return total


def main() -> None:
    parser = argparse.ArgumentParser(description="Search Kimu cases by topic, problem, or result.")
    parser.add_argument("query", help="Space-separated search terms")
    parser.add_argument("--limit", type=int, default=5, help="Maximum results (default: 5)")
    parser.add_argument("--json", action="store_true", help="Print JSON")
    args = parser.parse_args()

    terms = query_terms(args.query)
    ranked = []
    for entry in load_entries():
        item_score = score(entry, terms)
        if item_score:
            ranked.append((item_score, entry))
    ranked.sort(key=lambda item: (-item[0], int(item[1]["priority"] or 99), item[1]["id"]))
    results = [dict(score=item_score, **entry) for item_score, entry in ranked[: max(args.limit, 0)]]

    if args.json:
        print(json.dumps([{k: v for k, v in item.items() if k != "body"} for item in results], ensure_ascii=False, indent=2))
        return

    if not results:
        print("No matching cases.")
        return
    for item in results:
        print(f"{item['id']}｜{item['title']}  score={item['score']}")
        print(f"  类型：{item['type']}  优先级：{item['priority']}  证据：{item['evidence']}")
        print(f"  主题：{item['topics']}")


if __name__ == "__main__":
    main()
