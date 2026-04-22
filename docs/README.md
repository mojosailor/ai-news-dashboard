# Docs

Operational hand-offs, runbooks, and infrastructure notes for `ai-news-dashboard`.

## Hand-offs

Numbered, append-only. Each file is self-contained: problem, evidence, required change (with code or Terraform inline), acceptance tests, rollback, and a task checklist. Mark the checklist `[x]` and flip the **Status** banner to ✅ when completed — don't delete; we keep them as history and as templates.

| # | Title | Status | Target repo / system | Owner |
|---|---|---|---|---|
| [001](001-cloudfront-index-rewrite.md) | CloudFront index-document rewrite (default_root_object + viewer-request function) | ✅ Completed 2026-04-21 | `aws-master-tf` | Kiro / Seinfeld |

## Conventions

- **Filename:** `NNN-short-kebab-title.md` (zero-padded to 3). Do not encode the assignee's name — ownership is inside the doc.
- **Status banner:** first line after the title, one of:
  - 📝 **Draft** — not yet ready for the owner
  - 📤 **Ready** — waiting on owner to pick up
  - 🔧 **In progress** — owner is working on it
  - ✅ **Completed YYYY-MM-DD**
  - ❌ **Abandoned YYYY-MM-DD** — with a brief "why" note
- **Numbering:** take the next available integer. No reuse.
- **Completion:** check off the task list, update the banner, leave the rest of the doc intact so future readers can see what was actually done.

## When to write a hand-off

- Infra change needs to land in a different repo (Terraform, IAM, DNS, etc.)
- Non-trivial operational change that someone else will execute
- Anything that needs acceptance tests someone else will run

For day-to-day dashboard updates, the README's librarian workflow is enough — no hand-off needed.
