---
name: kimu-case-bank
description: Search, select, verify, add, and maintain Kimu's shared Chinese case bank for courses, PPT prompter scripts, opinion content, teacher training, knowledge-IP, self-media, and AI content. Use when the user asks to 查找案例、替换案例、补充Kimu/Nova/学员案例、把新材料收录进案例库、核对案例证据，or when another Kimu skill needs the best fitting real case or a clearly labeled placeholder.
---

# Kimu Case Bank

Maintain one shared source of truth for cases used by all Kimu skills. Prefer real, traceable Kimu and Nova material. Never invent an experience, result, quote, identity, date, or number.

## Route the request

Choose one mode before acting:

- **Retrieve**: find and return the best case for a topic, judgment, course page, or content outline.
- **Add or update**: turn user-authorized source material into a reusable record, or correct an existing record.
- **Audit**: check duplication, evidence status, privacy boundaries, and whether a case actually proves the claim.

For retrieval, read `references/index.md` first. Run `scripts/search_case_bank.py` when the library is larger than a few entries or the query has several concepts. Read the matching full records in `references/cases.md` before returning a case.

For additions, updates, or audits, read `references/schema.md` completely before editing. Modify the source files only when the user explicitly asks to store or update a case.

## Selection order

Use this order unless the user overrides it:

1. Kimu真实经历、Nova业务或学员案例
2. 教培与知识IP案例
3. 自媒体与AI案例
4. 公众熟悉且可核实的案例
5. 明确标注的待补案例

Prefer one case that directly proves the current judgment over several adjacent cases. Keep a second or third case only when the concept is difficult and the additional case explains a genuinely different angle.

## Retrieve a case

1. Translate the request into 2–6 concrete search terms: audience, problem, mechanism, result, and scenario.
2. Search the index or run:

   ```bash
   python3 scripts/search_case_bank.py "定位 精准粉 成交" --limit 5
   ```

3. Read the full record. Separate `核心事实` from `可用表达（非逐字引语）`.
4. Check `证据状态` and `使用边界`.
5. Return at most three ranked options. State why the first option proves the point.
6. If no case fits, do not force one. Output a concrete placeholder such as:

   ```text
   待补案例：需要一条Kimu关于「低反馈期仍持续更新」的真实视频或经历
   ```

When the case will appear on a PPT page, compress it to only the facts required to understand the judgment. Do not paste the entire record.

## Evidence rules

- Treat `已核对` as source-level verified.
- Treat `可追溯` as usable for selection but not yet line-by-line verified. Re-open the named source before using a precise number, date, quote, or causal claim in a final deliverable.
- Treat `用户提供` as attributable to the user but not independently verified.
- Treat `待核对` as an internal lead, not a publishable fact.
- Treat `案例方向` as a placeholder only.
- Verify public-person, company-history, academic, or historical cases with reliable web sources at the time of use. Do not store viral retellings as facts.
- Never present a generated golden line as a literal quote. The field `可用表达（非逐字引语）` is wording guidance, not source quotation.

## Add or update a case

1. Work from the user-provided artifact or a named source file. Do not infer missing results.
2. Extract only reusable facts. Remove administrative chatter and unsupported interpretation.
3. Assign the next unused `KCB-xxx` identifier. Preserve identifiers when updating.
4. Follow `references/schema.md`; add the full record to `references/cases.md` and one row to `references/index.md`.
5. Mark names or sensitive details as anonymized when the source does not authorize disclosure.
6. Run:

   ```bash
   python3 scripts/validate_case_bank.py
   ```

7. Report which records changed and which claims still need source verification.

When two records describe the same event, update the stronger record rather than creating a duplicate. When the facts conflict, keep both claims out of final content until the source is resolved.

## Output contract

For retrieval, use this compact shape:

```markdown
首选案例：KCB-xxx｜案例名
适用判断：它具体证明什么
可用事实：只列当前内容需要的事实
PPT压缩：可直接放入提词页的1—3行
来源与状态：来源名；证据状态
使用提醒：只在确有风险时填写

备选案例：最多2条（可选）
```

For updates, report added or changed case IDs, source names, evidence status, and validation result. Do not expose private chain-of-thought.

## Shared-skill contract

Other Kimu skills should call this library instead of copying its records into their own folders. They may keep only the selection order and a pointer to `$kimu-case-bank`. If this skill is unavailable in a host Agent, read the canonical `references/index.md` and `references/cases.md` from this skill directory; do not create a divergent local copy.
