#!/usr/bin/env python3
"""
One-shot patcher: replace the broken render <script> block in
html/index.html and every html/archive/YYYY-MM-DD.html with a fixed
version that matches the actual REPORT data shape (title + bullets).

Idempotent: if the fixed marker is already present, the file is left alone.

Run:
    python scripts/patch_render_template.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_DIR = ROOT / "html"
ARCHIVE_DIR = HTML_DIR / "archive"

# Marker comment we inject — used for idempotence.
FIX_MARKER = "/* render-fix v1 — TAG_META + bullets */"

# The fixed renderer.  Preserves the existing CSS classes:
#   .card.spotlight-flux / -harmony / -both / -enterprise / -bonus
#   .pill.pill-groove / -harmony / -both / -enterprise / -bonus
# Adds a small <ul class="bullets"> style scoped to spotlight cards.
FIXED_RENDER_BLOCK = (
    "/* render-fix v1 — TAG_META + bullets */\n"
    "const TAG_META = {\n"
    "  groove:     { label: 'GrooveGrid',              pillClass: 'pill-groove',     cardClass: 'spotlight-flux'      },\n"
    "  harmony:    { label: 'HarmonyGrid',             pillClass: 'pill-harmony',    cardClass: 'spotlight-harmony'   },\n"
    "  both:       { label: 'GrooveGrid + HarmonyGrid',pillClass: 'pill-both',       cardClass: 'spotlight-both'      },\n"
    "  enterprise: { label: 'Enterprise',              pillClass: 'pill-enterprise', cardClass: 'spotlight-enterprise'},\n"
    "  bonus:      { label: 'Bonus',                   pillClass: 'pill-bonus',      cardClass: 'spotlight-bonus'     }\n"
    "};\n"
    "\n"
    "function escapeHTML(s) {\n"
    "  return String(s == null ? '' : s)\n"
    "    .replace(/&/g, '&amp;')\n"
    "    .replace(/</g, '&lt;')\n"
    "    .replace(/>/g, '&gt;')\n"
    "    .replace(/\"/g, '&quot;')\n"
    "    .replace(/'/g, '&#39;');\n"
    "}\n"
    "\n"
    "function pill(tag) {\n"
    "  const m = TAG_META[tag] || TAG_META.enterprise;\n"
    "  return `<span class=\"pill ${m.pillClass}\">${escapeHTML(m.label)}</span>`;\n"
    "}\n"
    "\n"
    "function externalIcon() {\n"
    "  return `<svg width=\"10\" height=\"10\" viewBox=\"0 0 12 12\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"1.6\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M5 2H2a1 1 0 0 0-1 1v7a1 1 0 0 0 1 1h7a1 1 0 0 0 1-1V7\"/><polyline points=\"8 1 11 1 11 4\"/><line x1=\"5\" y1=\"7\" x2=\"11\" y2=\"1\"/></svg>`;\n"
    "}\n"
    "\n"
    "/* ── Date ──────────────────────────────────────────────────────────────── */\n"
    "(function () {\n"
    "  try {\n"
    "    const d = new Date(REPORT.date + 'T12:00:00');\n"
    "    const fmt = d.toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });\n"
    "    const el = document.getElementById('report-date');\n"
    "    if (el) el.textContent = fmt;\n"
    "  } catch (e) { /* non-fatal */ }\n"
    "})();\n"
    "\n"
    "/* ── Spotlights ────────────────────────────────────────────────────────── */\n"
    "const spotlightsAll = (REPORT && Array.isArray(REPORT.spotlights)) ? REPORT.spotlights : [];\n"
    "const visibleSpotlights = spotlightsAll.filter((s, i) => {\n"
    "  if (s && s.bonus) return true;\n"
    "  return i < 4;  // safety cap; matches README 'hard cap 4'\n"
    "});\n"
    "\n"
    "function spotlightCard(s) {\n"
    "  const m = TAG_META[s.tag] || TAG_META.enterprise;\n"
    "  const heading = escapeHTML(s.title || s.headline || '(untitled)');\n"
    "  const bulletsArr = Array.isArray(s.bullets) ? s.bullets : (s.summary ? [s.summary] : []);\n"
    "  const bulletsHTML = bulletsArr.length\n"
    "    ? `<ul class=\"bullets\">${bulletsArr.map(b => `<li>${escapeHTML(b)}</li>`).join('')}</ul>`\n"
    "    : '';\n"
    "  const sourceLabel = escapeHTML(s.sourceLabel || 'Source');\n"
    "  const sourceUrl   = String(s.sourceUrl || '#');\n"
    "  return `\n"
    "    <div class=\"card ${m.cardClass}\">\n"
    "      <div class=\"card-header\">\n"
    "        <h2>${heading}</h2>\n"
    "        ${pill(s.tag)}\n"
    "      </div>\n"
    "      ${bulletsHTML}\n"
    "      <div class=\"card-footer\">\n"
    "        <span class=\"relevance\">${escapeHTML(s.relevance || '')}</span>\n"
    "        <a class=\"source-link\" href=\"${sourceUrl}\" target=\"_blank\" rel=\"noopener\">\n"
    "          ${externalIcon()} ${sourceLabel}\n"
    "        </a>\n"
    "      </div>\n"
    "    </div>`;\n"
    "}\n"
    "\n"
    "(function () {\n"
    "  const grid = document.getElementById('spotlight-grid');\n"
    "  if (!grid) return;\n"
    "  if (visibleSpotlights.length === 0) {\n"
    "    grid.innerHTML = `<div class=\"empty\">No spotlights for today.</div>`;\n"
    "  } else {\n"
    "    grid.innerHTML = visibleSpotlights.map(spotlightCard).join('');\n"
    "  }\n"
    "})();\n"
    "\n"
    "/* ── Stories ───────────────────────────────────────────────────────────── */\n"
    "function storyRow(s) {\n"
    "  const title = escapeHTML(s.title || s.headline || '(untitled)');\n"
    "  const summary = escapeHTML(s.summary || '');\n"
    "  const sourceLabel = escapeHTML(s.sourceLabel || 'Source');\n"
    "  const sourceUrl   = String(s.sourceUrl || '#');\n"
    "  const summaryHTML = summary ? `<div class=\"story-summary\">${summary}</div>` : '';\n"
    "  return `\n"
    "    <div class=\"story-item\">\n"
    "      <div class=\"story-pill\">${pill(s.tag)}</div>\n"
    "      <div class=\"story-body\">\n"
    "        <div class=\"story-title\">${title}</div>\n"
    "        ${summaryHTML}\n"
    "      </div>\n"
    "      <a class=\"story-source\" href=\"${sourceUrl}\" target=\"_blank\" rel=\"noopener\">\n"
    "        ${externalIcon()} ${sourceLabel}\n"
    "      </a>\n"
    "    </div>`;\n"
    "}\n"
    "\n"
    "(function () {\n"
    "  const list = document.getElementById('story-list');\n"
    "  if (!list) return;\n"
    "  const stories = (REPORT && Array.isArray(REPORT.stories)) ? REPORT.stories : [];\n"
    "  if (stories.length === 0) {\n"
    "    list.innerHTML = `<div class=\"empty\">No additional stories today.</div>`;\n"
    "  } else {\n"
    "    list.innerHTML = stories.map(storyRow).join('');\n"
    "  }\n"
    "})();\n"
    "\n"
    "/* ── Footer count ──────────────────────────────────────────────────────── */\n"
    "(function () {\n"
    "  const el = document.getElementById('footer-count');\n"
    "  if (!el) return;\n"
    "  const s = visibleSpotlights.length;\n"
    "  const t = (REPORT && Array.isArray(REPORT.stories)) ? REPORT.stories.length : 0;\n"
    "  el.textContent = `${s} spotlight${s !== 1 ? 's' : ''} · ${t} stories`;\n"
    "})();\n"
)

# CSS we add for spotlight bullets if not already present.
BULLETS_CSS_MARKER = "/* render-fix v1 bullets css */"
BULLETS_CSS = (
    "\n  " + BULLETS_CSS_MARKER + "\n"
    "  .card .bullets {\n"
    "    list-style: disc;\n"
    "    padding-left: 18px;\n"
    "    margin: 0;\n"
    "    color: #b0b4cc;\n"
    "    font-size: 13px;\n"
    "    line-height: 1.65;\n"
    "    display: flex;\n"
    "    flex-direction: column;\n"
    "    gap: 6px;\n"
    "  }\n"
    "  .card .bullets li {\n"
    "    margin-left: 0;\n"
    "  }\n"
)

# Regex to find the existing render <script>…</script> block.
# We anchor it to "function pill" because there is exactly one inline
# <script> per report file and it always defines pill().
SCRIPT_RE = re.compile(
    r"<script>\s*(?:/\*.*?\*/\s*)?const REPORT\s*=.*?</script>",
    re.DOTALL,
)


def patch_file(path: Path) -> str:
    """Return one of: 'patched', 'already-patched', 'skipped-no-match'."""
    text = path.read_text(encoding="utf-8")

    if FIX_MARKER in text:
        # Already patched.  Make sure CSS marker is also present.
        if BULLETS_CSS_MARKER not in text:
            text = inject_bullets_css(text)
            path.write_text(text, encoding="utf-8")
        return "already-patched"

    m = SCRIPT_RE.search(text)
    if not m:
        return "skipped-no-match"

    original_script = m.group(0)

    # Extract the REPORT = { ... }; literal verbatim.
    report_match = re.search(
        r"const REPORT\s*=\s*(\{.*?\})\s*;\s*\n",
        original_script,
        re.DOTALL,
    )
    if not report_match:
        return "skipped-no-match"
    report_literal = report_match.group(0)  # full "const REPORT = {...};\n"

    new_script = "<script>\n" + report_literal + "\n" + FIXED_RENDER_BLOCK + "</script>"

    text = text.replace(original_script, new_script)
    text = inject_bullets_css(text)
    path.write_text(text, encoding="utf-8")
    return "patched"


def inject_bullets_css(text: str) -> str:
    """Inject .card .bullets CSS just before </style> in <head>."""
    if BULLETS_CSS_MARKER in text:
        return text
    # Insert before the FIRST </style> we find (the page's main style block).
    idx = text.find("</style>")
    if idx == -1:
        return text
    return text[:idx] + BULLETS_CSS + text[idx:]


def main() -> int:
    targets = []
    if (HTML_DIR / "index.html").exists():
        targets.append(HTML_DIR / "index.html")
    for f in sorted(ARCHIVE_DIR.glob("*.html")):
        if re.match(r"^\d{4}-\d{2}-\d{2}\.html$", f.name):
            targets.append(f)

    counts = {"patched": 0, "already-patched": 0, "skipped-no-match": 0}
    for t in targets:
        result = patch_file(t)
        counts[result] += 1
        print(f"  {result:20s}  {t.relative_to(ROOT)}")

    print(f"\nSummary: {counts}")
    return 0 if counts["skipped-no-match"] == 0 else 2


if __name__ == "__main__":
    sys.exit(main())
