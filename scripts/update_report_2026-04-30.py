import re, json, datetime

today = '2026-04-30'

def js(obj):
    return json.dumps(obj, ensure_ascii=False)

REPORT = {
  "date": today,
  "dateline": "Thu, Apr 30, 2026",
  "spotlights": [
    {
      "title": "Google Cloud launches Gemini Enterprise Agent Platform",
      "tag": "enterprise",
      "bullets": [
        "New ‘Gemini Enterprise Agent Platform’ positions as the new home for Vertex AI agent development.",
        "Governance primitives include Agent Identity (cryptographic IDs), Agent Registry, and Agent Gateway.",
        "Also adds security monitoring like anomaly/threat detection and an agent security dashboard."
      ],
      "sourceLabel": "Google Cloud Blog",
      "sourceUrl": "https://cloud.google.com/blog/products/ai-machine-learning/introducing-gemini-enterprise-agent-platform"
    },
    {
      "title": "Microsoft open-sources Agent Governance Toolkit (runtime policy + identity)",
      "tag": "enterprise",
      "bullets": [
        "MIT-licensed toolkit for runtime governance of autonomous agents across common frameworks.",
        "Includes a policy engine (YAML/OPA Rego/Cedar) and DID-based agent identity (Ed25519).",
        "Packaged as a monorepo with components for compliance evidence, SRE patterns, and plugin signing."
      ],
      "sourceLabel": "Microsoft Open Source Blog",
      "sourceUrl": "https://opensource.microsoft.com/blog/2026/04/02/introducing-the-agent-governance-toolkit-open-source-runtime-security-for-ai-agents/"
    },
    {
      "title": "Self-hosting gets easier: OpenAI’s gpt-oss models land in Ollama",
      "tag": "harmony",
      "bullets": [
        "Ollama lists OpenAI ‘gpt-oss’ open-weight models (20B and 120B) under Apache 2.0.",
        "Claims MXFP4 quantization support and the ability to run the smaller model on ~16GB RAM.",
        "Good fit for local reasoning + agentic workflows where data can’t leave the box."
      ],
      "sourceLabel": "Ollama Library",
      "sourceUrl": "https://ollama.com/library/gpt-oss",
      "bonus": True
    },
    {
      "title": "Adobe expands Firefly’s browser video editor + adds Kling 3.0 models",
      "tag": "bonus",
      "bullets": [
        "Firefly Video Editor adds audio cleanup (Enhance Speech) and tighter Adobe Stock integration.",
        "Adobe says Kling 3.0 and Kling 3.0 Omni are now available as Firefly video models.",
        "Premiere gets a new Color Mode (beta); After Effects adds an AI Object Matte workflow."
      ],
      "sourceLabel": "Adobe Blog",
      "sourceUrl": "https://blog.adobe.com/en/publish/2026/04/15/adobe-extends-leadership-video-unleashing-new-ai-powered-creation-firefly-reinventing-color-editors-in-premiere",
      "bonus": True
    }
  ],
  "stories": [
    {
      "title": "Grid edge: AI data centers are forcing utilities to rethink load planning",
      "tag": "both",
      "summary": "Utility Dive reports data-center demand volatility is breaking legacy planning assumptions and pushing utilities toward more dynamic forecasting and flexibility programs.",
      "sourceLabel": "Utility Dive",
      "sourceUrl": "https://www.utilitydive.com/news/ai-data-centers-utility-load-planning/816806/"
    },
    {
      "title": "Real estate ops: Entrata debuts an ‘agentic’ property management system with 100+ AI agents",
      "tag": "groove",
      "summary": "Entrata says its OXP platform now embeds 100+ AI agents across leasing, maintenance, accounting, and resident workflows, plus an orchestration workspace (OXP Studio).",
      "sourceLabel": "GlobeNewswire",
      "sourceUrl": "https://www.globenewswire.com/news-release/2026/03/24/3261761/0/en/entrata-introduces-the-multifamily-industry-s-first-agentic-property-management-system-with-100-embedded-ai-agents.html"
    },
    {
      "title": "Property managers: DoorLoop launches AI Inspections to turn photos into reports + work orders",
      "tag": "groove",
      "summary": "DoorLoop says its AI Inspections feature can generate structured inspection reports from guided photo capture and automatically create follow-up work orders.",
      "sourceLabel": "DoorLoop Blog",
      "sourceUrl": "https://www.doorloop.com/blog/doorloop-launches-ai-inspections"
    },
    {
      "title": "Creators: Google Vids adds free Veo 3.1 video generations for anyone with a Google account",
      "tag": "bonus",
      "summary": "Google says Vids now offers 10 free Veo 3.1 generations monthly, with higher limits for AI Ultra/Workspace tiers and music via Lyria for paid plans.",
      "sourceLabel": "Google Blog",
      "sourceUrl": "https://blog.google/products-and-platforms/products/workspace/google-vids-updates-lyria-veo/"
    },
    {
      "title": "Open models: Google releases Gemma 4 under Apache 2.0",
      "tag": "harmony",
      "summary": "Google’s open-source team says Gemma 4 is the first Gemma family released under Apache 2.0, aiming to broaden commercial and research use.",
      "sourceLabel": "Google Open Source Blog",
      "sourceUrl": "https://opensource.googleblog.com/2026/03/gemma-4-expanding-the-gemmaverse-with-apache-20.html"
    },
    {
      "title": "Identity for agents: why IAM becomes the control plane for autonomous workflows",
      "tag": "enterprise",
      "summary": "Strata argues agentic AI needs runtime identity governance (ephemeral credentials, observability, and delegation controls) rather than periodic access reviews.",
      "sourceLabel": "Strata Identity",
      "sourceUrl": "https://www.strata.io/blog/agentic-identity/agentic-ai-governance-how-to-approach-it/"
    }
  ]
}

new_report_text = 'const REPORT = ' + js(REPORT) + '\n;\n'

with open('html/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

pattern = re.compile(r'const REPORT = \{.*?\n\};\n', re.DOTALL)
matches = pattern.findall(html)
assert len(matches) == 1, f'expected 1 REPORT block, found {len(matches)}'
assert 'TAG_META' not in matches[0], 'pattern over-matched into TAG_META'

new_html = html.replace(matches[0], new_report_text, 1)

# Update visible date in header if present
new_html = re.sub(r'(<div id="report-date">)(.*?)(</div>)', r'\1' + REPORT['dateline'] + r'\3', new_html)

with open('html/index.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

print('updated REPORT + dateline')
