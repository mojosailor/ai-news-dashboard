import re
from datetime import date

REPORT_TEXT = """const REPORT = {
  date: '2026-05-04',

  spotlights: [
    {
      title: 'Grid-edge AI goes from pilot to tickets: Sense Waveform AI flags transformer-level faults',
      tag: 'both',
      bullets: [
        'Sense published results from its fault-detection pilot with Southern Company (Georgia Power + Alabama Power), using waveform AI to localize distribution issues at the transformer level.',
        'As of Oct 2025, the pilot confirmed 19 detected events that turned into utility tickets; Georgia Power validated 15 as vegetation-related, 2 as squirrel-caused, with 0 false negatives reported.',
        'Signal: utilities can treat edge analytics as an operational system (work orders), not just a dashboard — a prerequisite for DERMS/VPP scaling and faster outage prevention.'
      ],
      sourceLabel: 'Sense',
      sourceUrl: 'https://sense.com/resources/before-the-outage-grid-edge-insights-real-results/',
      keywords: ['grid-edge', 'fault detection', 'waveform AI', 'distribution'],
      relevance: 'Turns distribution analytics into actionable tickets — a concrete pattern for scaling AI ops in utility environments.'
    },
    {
      title: 'Know-Your-Agent comes to regulated finance: MetaComp launches the StableX KYA framework',
      tag: 'enterprise',
      bullets: [
        'MetaComp announced the StableX “Know Your Agent” (KYA) Framework for AI agents operating in regulated financial services (payments, compliance, wealth).',
        'The framework centers on verified agent identity + registration, permission control, behavior monitoring/risk intelligence, and ecosystem interaction governance (including agent-to-agent rules).',
        'Pilot pattern: treat agents like regulated actors — identity, least-privilege, human escalation, continuous monitoring, and end-to-end audit trails as first-class primitives.'
      ],
      sourceLabel: 'PR Newswire',
      sourceUrl: 'https://www.prnewswire.com/news-releases/metacomp-launches-the-worlds-first-ai-agent-governance-framework-for-regulated-financial-services-302748416.html',
      keywords: ['agent governance', 'identity', 'audit trails', 'regulated workflows'],
      relevance: 'A concrete governance architecture for agent identity and controls in high-compliance environments.'
    },
    {
      title: 'VPPs meet grid-enhancing tech: Reuters highlights TVA scaling demand response and dynamic line ratings',
      tag: 'bonus',
      bonus: true,
      bullets: [
        'Reuters reports TVA runs ~2 GW of demand response that qualifies as VPPs and expects >50% growth, alongside grid-enhancing tech like dynamic line ratings and advanced conductors.',
        'Sunrun forecasts a growing network of battery + solar homes (dispatchable storage) as utilities lean on flexible, behind-the-meter capacity during peaks.',
        'Why it matters: the winning playbook is “VPP + grid-enhancing tech” to add capacity faster than new transmission buildouts.'
      ],
      sourceLabel: 'Reuters',
      sourceUrl: 'https://www.reuters.com/business/energy/us-utilities-scale-up-grid-boosting-tech-meet-surging-demand--reeii-2026-03-09/',
      keywords: ['VPP', 'demand response', 'dynamic line rating', 'TVA'],
      relevance: 'Pairs flexible load with faster capacity upgrades — a pragmatic scaling path for reliability.'
    },
    {
      title: 'ElevenLabs ships ElevenMusic: an iOS AI music generator with 7 free songs/day',
      tag: 'bonus',
      bonus: true,
      bullets: [
        'TechCrunch reports ElevenLabs quietly released an iOS app, ElevenMusic, for generating and discovering AI music via natural-language prompts.',
        'The free tier allows up to seven generated songs per day; remixes count toward the daily limit.',
        'Signal: AI audio vendors are pushing into consumer creative apps (not just APIs) to compete with Suno/Udio and build distribution.'
      ],
      sourceLabel: 'TechCrunch',
      sourceUrl: 'https://techcrunch.com/2026/04/02/elevenlabs-releases-a-new-ai-powered-music-generation-app/',
      keywords: ['AI music', 'ElevenLabs', 'consumer app'],
      relevance: 'Consumer distribution + daily free quota is a playbook to build a creator ecosystem.'
    }
  ],

  stories: [
    {
      title: 'OpenADR Alliance growth points to expanding VPP interoperability demand',
      tag: 'harmony',
      sourceLabel: 'Yahoo Finance',
      sourceUrl: 'https://finance.yahoo.com/news/openadr-alliance-reports-unprecedented-growth-130000564.html'
    },
    {
      title: 'Yield Energy launches Yield Edge, a farm-based DERMS backed by California Energy Commission funding',
      tag: 'both',
      sourceLabel: 'PV Tech',
      sourceUrl: 'https://www.pv-tech.org/yield-energy-launches-farm-based-grid-flexibility-platform/'
    },
    {
      title: 'Aembit adds IAM for agentic AI, including an MCP Identity Gateway for tool access control',
      tag: 'enterprise',
      sourceLabel: 'Aembit',
      sourceUrl: 'https://aembit.io/press-release/aembit-introduces-identity-and-access-management-for-agentic-ai/'
    },
    {
      title: 'Ollama previews MLX-powered engine on Apple Silicon for faster local model runs',
      tag: 'harmony',
      sourceLabel: 'Ollama',
      sourceUrl: 'https://ollama.com/blog'
    },
    {
      title: 'Zillow launches AI Assist (powered by EliseAI) for 24/7 renter engagement in multifamily listings',
      tag: 'groove',
      sourceLabel: 'Zillow',
      sourceUrl: 'https://www.zillow.com/news/zillow-launches-ai-assist/'
    },
    {
      title: 'Utility Dive: VPPs must scale in 2026 or risk being sidelined by the AI data center load boom',
      tag: 'both',
      sourceLabel: 'Utility Dive',
      sourceUrl: 'https://www.utilitydive.com/news/in-2026-virtual-power-plants-must-scale-or-risk-being-left-behind/810321/'
    }
  ]
};
"""


def main():
    with open('html/index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    pattern = re.compile(r"const REPORT = \{.*?\n\};\n", re.DOTALL)
    matches = pattern.findall(html)
    assert len(matches) == 1, f'expected 1 REPORT block, found {len(matches)}'
    assert 'TAG_META' not in matches[0], 'pattern over-matched into TAG_META'

    new_html = html.replace(matches[0], REPORT_TEXT, 1)

    # Update dateline (human-readable)
    new_html = re.sub(
        r"(<span id=\"report-date\">)(.*?)(</span>)",
        r"\1May 04, 2026\3",
        new_html,
        count=1,
        flags=re.DOTALL,
    )

    with open('html/index.html', 'w', encoding='utf-8') as f:
        f.write(new_html)


if __name__ == '__main__':
    main()
