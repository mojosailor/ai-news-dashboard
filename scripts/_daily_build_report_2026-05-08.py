import json
from textwrap import dedent

date = "2026-05-08"

REPORT = {
  "date": date,
  "spotlights": [
    {
      "title": "New Jersey BPU opens a Virtual Power Plant (VPP) RFI tied to distributed storage incentives",
      "tag": "both",
      "bullets": [
        "RFI seeks input on VPP program design + Phase 2 of the Garden State Energy Storage Program (distributed storage segment).",
        "Defines Grid DERMS vs Edge DERMS, and asks about telemetry, dispatch, interoperability (e.g., OpenADR/IEEE 2030.5), and M&V for scalable VPP operations.",
        "Responses due May 20, 2026; filed under Docket No. QO26030099."
      ],
      "sourceLabel": "New Jersey Board of Public Utilities (PDF)",
      "sourceUrl": "https://www.nj.gov/bpu/pdf/publicnotice/VPP%20RFI_April%202026-05-6.pdf"
    },
    {
      "title": "ServiceNow extends AI Control Tower governance into Microsoft Agent 365 ecosystem",
      "tag": "enterprise",
      "bullets": [
        "Adds deeper integration so ServiceNow AI Control Tower can extend governance visibility and insights across Microsoft Agent 365.",
        "ServiceNow AI specialists are planned for the Microsoft Agent 365 Marketplace, acting as governed digital employees inside Microsoft 365 apps.",
        "Positioned as an answer to ‘agent sprawl’ with unified oversight across ServiceNow and Microsoft environments (preview)."
      ],
      "sourceLabel": "ServiceNow Newsroom",
      "sourceUrl": "https://newsroom.servicenow.com/press-releases/details/2026/ServiceNow-expands-AI-agent-governance-through-deeper-integration-with-Microsoft/default.aspx"
    },
    {
      "title": "OpenADR Alliance + DLMS UA sign liaison agreement to improve grid-edge interoperability",
      "tag": "bonus",
      "bonus": True,
      "bullets": [
        "Agreement targets seamless data exchange between DLMS/COSEM smart meter data and OpenADR signaling for demand response and DER flexibility services.",
        "Signal: standards bodies aligning for more interoperable telemetry + control at the grid edge."
      ],
      "sourceLabel": "OpenADR Alliance",
      "sourceUrl": "https://www.openadr.org/press-releases"
    },
    {
      "title": "Runway adds Seedance 2.0 video generation/editing (text, image, video, or audio inputs)",
      "tag": "bonus",
      "bonus": True,
      "bullets": [
        "Seedance 2.0 supports generating or editing video from multiple input modalities.",
        "Listed as available on Unlimited and Enterprise plans outside the US (Apr 7, 2026 changelog)."
      ],
      "sourceLabel": "Runway Changelog",
      "sourceUrl": "https://runwayml.com/changelog"
    }
  ],
  "stories": [
    {
      "title": "Microsoft Agent 365 (May 2026 update) highlights lifecycle actions + rules-based governance and Entra ID Governance for agents",
      "tag": "enterprise",
      "sourceLabel": "Microsoft Tech Community",
      "sourceUrl": "https://techcommunity.microsoft.com/blog/agent-365-blog/what%E2%80%99s-new-in-agent-365-may-2026/4516340"
    },
    {
      "title": "Microsoft Security Blog: Agent 365 GA expands cross-platform registry sync (preview) including AWS Bedrock + Google Cloud connections",
      "tag": "enterprise",
      "sourceLabel": "Microsoft Security Blog",
      "sourceUrl": "https://www.microsoft.com/en-us/security/blog/2026/05/01/microsoft-agent-365-now-generally-available-expands-capabilities-and-integrations/"
    },
    {
      "title": "BigID outlines a feature checklist for agentic AI governance platforms (data discovery + access intelligence + permissions governance)",
      "tag": "enterprise",
      "sourceLabel": "BigID",
      "sourceUrl": "https://bigid.com/blog/agentic-ai-governance-platform/"
    },
    {
      "title": "Buildium describes ‘Lumina AI’ agents embedded in property management workflows (accounting + ops automation)",
      "tag": "groove",
      "sourceLabel": "Buildium",
      "sourceUrl": "https://www.buildium.com/blog/best-ai-property-management-tools/"
    },
    {
      "title": "LM Studio publishes frequent local runtime updates in its changelog (latest April 2026 entry)",
      "tag": "harmony",
      "sourceLabel": "LM Studio",
      "sourceUrl": "https://lmstudio.ai/changelog"
    },
    {
      "title": "Ollama’s GitHub releases show ongoing local inference engine performance + tool-calling improvements (v0.22.1)",
      "tag": "harmony",
      "sourceLabel": "GitHub Releases (Ollama)",
      "sourceUrl": "https://github.com/ollama/ollama/releases"
    }
  ]
}

# Convert to JS object literal (double quotes, lowercase true)
report_json = json.dumps(REPORT, ensure_ascii=False, indent=2)
# json.dumps uses true/false/null already.
new_report_text = "const REPORT = " + report_json + ";\n"
print(new_report_text)
