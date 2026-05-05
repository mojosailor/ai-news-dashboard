import re, json

DATE = '2026-04-29'

REPORT = {
  "date": DATE,
  "spotlights": [
    {
      "title": "Ping Identity makes 'Identity for AI' generally available for runtime agent IAM",
      "tag": "enterprise",
      "bullets": [
        "Agent IAM Core + Agent Gateway + Agent Detection aim to treat agents as first-class identities with delegated, scoped authorization.",
        "Positioned for securing MCP-style integrations with runtime policy enforcement and monitoring.",
        "Pilot: inventory your top 10 agent tool calls and enforce least-privilege scopes + audit logging at the gateway layer."
      ],
      "sourceLabel": "Ping Identity press release",
      "sourceUrl": "https://press.pingidentity.com/2026-03-24-Ping-Identity-Defines-the-Runtime-Identity-Standard-for-Autonomous-AI"
    },
    {
      "title": "Identity Digital launches DNSid, a DNS-anchored identity standard for AI agents",
      "tag": "enterprise",
      "bullets": [
        "Proposes a persistent identifier that binds each agent to verifiable ownership and lifecycle events (ownership, transfer, revocation).",
        "Uses DNS infrastructure plus PKI + blockchain concepts for cross-org interoperability.",
        "Pilot: decide whether your org needs a durable agent identifier separate from runtime auth tokens."
      ],
      "sourceLabel": "GlobeNewswire via FinancialContent",
      "sourceUrl": "https://www.financialcontent.com/article/gnwcq-2026-4-27-identity-digital-launches-neutral-dns-anchored-identity-standard-for-ai-agents"
    },
    {
      "title": "OpenADR webinar spotlights AI + OpenADR 3 for autonomous local demand flexibility",
      "tag": "harmony",
      "bullets": [
        "OpenADR Alliance highlights a path where standards handle signaling/communication while AI optimizes device-level control.",
        "Reinforces a 'grid-signal in, outcome out' pattern for building + home flexibility without waiting for new device standards.",
        "Pilot: map your VTN/VEN plan and where an AI layer could sit (forecasting, constraint solving, verification)."
      ],
      "sourceLabel": "OpenADR Alliance webinar series",
      "sourceUrl": "https://www.openadr.org/webinar-series"
    },
    {
      "title": "Adobe unveils Firefly AI Assistant, a creative agent spanning Creative Cloud workflows",
      "tag": "bonus",
      "bonus": True,
      "bullets": [
        "Firefly AI Assistant is positioned as a conversational interface that orchestrates multi-step workflows across Creative Cloud apps.",
        "Firefly expands video/image editing controls and emphasizes model choice (multiple third-party models in roster).",
        "Pilot: test a single 'brief → assets' workflow for sermon series graphics or event promos, then codify prompts + review steps."
      ],
      "sourceLabel": "Adobe Newsroom",
      "sourceUrl": "https://news.adobe.com/news/2026/04/adobe-new-creative-agent"
    }
  ],
  "stories": [
    {
      "title": "Meta, Google, and Microsoft are leaning on new natural gas plants to power AI data centers",
      "tag": "both",
      "summary": "A TechCrunch analysis frames the near-term AI power crunch as pushing major AI companies toward large new gas generation projects, raising reliability and climate tradeoffs.",
      "sourceLabel": "TechCrunch",
      "sourceUrl": "https://techcrunch.com/2026/04/03/ai-companies-are-building-huge-natural-gas-plants-to-power-data-centers-what-could-go-wrong/"
    },
    {
      "title": "LM Studio 0.4.12 adds Qwen 3.6 support and fixes MCP OAuth issues on some Windows setups",
      "tag": "harmony",
      "summary": "LM Studio's latest changelog highlights Qwen 3.6 support plus an MCP OAuth fix, keeping the local-model desktop stack moving fast.",
      "sourceLabel": "LM Studio changelog",
      "sourceUrl": "https://lmstudio.ai/changelog/lmstudio-v0.4.12"
    },
    {
      "title": "Ollama update leverages Apple's MLX framework for major speedups on Apple silicon Macs",
      "tag": "harmony",
      "summary": "MacRumors reports Ollama shipped an update using Apple's MLX to speed up prefill and decode on Apple silicon, making local assistants feel snappier.",
      "sourceLabel": "MacRumors",
      "sourceUrl": "https://www.macrumors.com/2026/03/31/ollama-now-runs-faster-apple-silicon-macs/"
    },
    {
      "title": "Rechat adds AI Memo for real-time conversation capture and structured follow-up in real estate workflows",
      "tag": "groove",
      "summary": "RISMedia reports Rechat launched AI Memo to capture, transcribe, and structure client conversations, aiming to improve follow-up and reduce dropped balls.",
      "sourceLabel": "RISMedia",
      "sourceUrl": "https://www.rismedia.com/2026/04/08/rechat-launches-ai-memo-to-capture-agent-conversations-in-real-time/"
    },
    {
      "title": "Buildium highlights embedded 'Lumina AI' workflows for billing, comms, leasing, and maintenance",
      "tag": "groove",
      "summary": "Buildium's 2026 overview outlines AI-assisted invoice extraction and message drafting as part of property management workflows, with higher-end 'AI Workforce' agents.",
      "sourceLabel": "Buildium",
      "sourceUrl": "https://www.buildium.com/blog/best-ai-property-management-tools/"
    },
    {
      "title": "Google expands Lyria 3 Pro music generation across Gemini, Vertex AI, AI Studio, and Vids",
      "tag": "bonus",
      "bonus": True,
      "summary": "Google says Lyria 3 Pro can generate longer, structured tracks (up to 3 minutes) and is rolling into multiple products and APIs with SynthID watermarking.",
      "sourceLabel": "Google blog",
      "sourceUrl": "https://blog.google/innovation-and-ai/technology/ai/lyria-3-pro/"
    }
  ]
}

with open('html/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Match the REPORT object literal from `const REPORT = {` through the closing `};` line.
pattern = re.compile(r'const REPORT = \{.*?\n\};\n', re.DOTALL)
matches = pattern.findall(html)

# Hard guards — fail the run, do NOT fall back to a textual diff.
assert len(matches) == 1, f'expected 1 REPORT block, found {len(matches)}'

new_report_text = 'const REPORT = ' + json.dumps(REPORT, indent=2, ensure_ascii=False) + '\n;\n'
new_html = html.replace(matches[0], new_report_text, 1)

# Update visible dateline text (best-effort; keep existing format)
new_html = re.sub(r'(id="report-date"[^>]*>)([^<]*)(</)', r'\g<1>' + DATE + r'\g<3>', new_html)

with open('html/index.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

print('OK: updated REPORT and date')
