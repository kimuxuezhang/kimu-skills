---
name: kimu-viewpoint-script
description: 把中文课程长文、音频或转写稿提炼为可直接讲授、分段编号的 Kimu 风格观点提词稿。用户要求生成观点大纲、授课提词稿、继续下一章节或转换完整课程时使用。
---

# Kimu Viewpoint Script

Turn long course material into concise, audience-facing viewpoint prompts that Kimu can present directly. Preserve the source's strongest logic while rewriting the expression, removing chatter, and keeping only memory anchors.

This module can be routed from the Kimu entrypoint or used directly with natural language such as `Kimu 观点提词稿：把这份课程材料提炼成授课观点大纲`.

## Load the working standard

Read `references/style-rules.md` and `references/examples.md` before drafting. When the source is DOCX, also use the host's document-reading workflow. When the user asks for a PPTX rather than a text prompter script, finish the script first and then use the host's presentation workflow.

## Choose the execution mode

- Default to **segmented mode**: produce one coherent chapter covering about 35–45 minutes, then wait for review.
- Use **full-course mode** only after the user explicitly chooses it. If the request is ambiguous, ask before processing the whole course.
- In a continuation, inspect existing drafts and locate the exact source boundary before writing. Do not restart or skip ahead.
- Prefer a complete teaching unit over an exact timestamp. Stop early or extend modestly when a topic begins or ends near the time boundary, and report the source range.

## Read and filter the source

1. Read the complete source range needed to understand the argument, not only isolated paragraphs.
2. Separate the teaching spine from audience questions, exercises, promotion, administration, and casual conversation.
3. Delete audience chatter and stand-alone questions. Keep a teacher's answer only when it develops a reusable method directly related to the lesson.
4. Remove repeated explanations, verbal tics, exaggerated claims, unsupported platform folklore, and examples that do not advance the teaching point.
5. Retain the source's useful causal structure, distinctions, workflows, and difficult-to-replace examples. Rewrite them in Kimu's concise teaching language.

## Build the chapter

1. Define one sentence: by the end, what should the learners understand or be able to do?
2. Identify the chapter's 2–4 cumulative teaching moves.
3. Give every page one job and one primary claim.
4. Arrange pages so each creates the need for the next. Add a transition only when the logic would otherwise jump.
5. Open with the chapter and its core dimensions. Close only when a new synthesis or action is added; do not add a repetitive “这一篇的核心” page.

## Write each page

Use this exact shape:

```text
【本段P1】
页面主旨或核心概念
必要关系
必要判断
必要案例或动作
```

- Keep 1–5 visible lines after the page marker; prefer 3–4.
- Keep only concepts, relationships, judgments, actions, and necessary case facts.
- Delete subjects, connectors, qualifiers, and summary labels that Kimu can supply naturally while speaking.
- Use compact phrases when the relationship remains clear. Do not turn every page into a full sentence.
- Remove non-core words and repeated synonyms before creating another page.
- Do not expose timing, source-selection notes, production commentary, or internal instructions on audience-facing pages.

## Handle examples

Use the selection order from the `kimu-case-bank` skill instead of copying its records:

1. Kimu真实经历、Nova业务或学员案例
2. 教培与知识IP案例
3. 自媒体与AI案例
4. 公众熟悉且可核实的案例
5. 明确标注的待补案例

Use one case for an easy concept and up to three only when each explains a different angle. Never invent an experience, result, quote, identity, date, or number. If no suitable case exists, write a concrete placeholder such as:

```text
【需要一条Kimu学长关于“低反馈期持续更新”的真实案例】
```

## Number pages

- Reset to `【本段P1】` when the material forms a clear major chapter.
- Continue numbering across the whole course block when no meaningful chapter boundary exists.
- Ask only when the structure genuinely cannot determine which rule applies.
- Keep page markers in final TXT or Markdown output; they are required for later PPT production.

## Validate before delivery

Run:

```bash
python3 scripts/validate_viewpoint_script.py path/to/draft.txt
```

Fix every numbering or line-count error. Review warnings for filler phrases and exact repeated lines; keep a repetition only when it is an intentional concept label. Then verify:

- one page, one teaching job;
- no important logic gap;
- no non-core words or oral filler;
- no unnecessary recap page;
- examples directly prove the claim;
- the chapter begins and ends at a coherent boundary;
- the output can be taught from without reopening the source.

Deliver the TXT or Markdown file, page count, source range, chapter theme, and the next unused source boundary.
