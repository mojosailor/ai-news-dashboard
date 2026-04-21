# ai-news-dashboard


---

## Section Definitions

### Flux Spotlights
- Always ≥1 Flux spotlight per day.
- Each tagged: `[GrooveGrid]`, `[HarmonyGrid]`, or `[GrooveGrid + HarmonyGrid]`.
- Dual tag allowed when a development clearly benefits both brands.
- Priority triggers: HEMS, VPP, DERMS, OpenADR, submetering, CalTRACK/M&V,
  property management AI, energy incentives, demand/solar/EV forecasting.

### Enterprise Spotlights
- Always ≥1 general spotlight (unless Flux fills all slots on a big Flux day).
- Rotates through 10 core use cases (customer support, sales copilots, doc processing,
  personalization, fraud/risk, agentic automation, knowledge mgmt, supply chain, IT ops,
  industry-specific assistants).
- Format: short title + 2–4 bullets (value, tech pattern, what to pilot next).

### Spotlight Count Rules
| Condition                | Count         |
|---|---|
| Default                  | 2 (1 Flux + 1 General) |
| Multiple strong items    | Expand up to 4 total   |
| Hard cap                 | 4 spotlights max       |

Ranking when >4 candidates: Flux impact → Enterprise impact → Researcher novelty.

### For AI Researchers
- New model/architecture releases, arXiv links, evals.
- Frameworks, orchestrators, agent frameworks, eval harnesses.
- Benchmarks, safety, multi-modal eval news.
- Dataset & synthetic data tooling.
- Research productivity tools (Elicit, SciSpace, Julius, ScholarAI, etc.).

### Free Tools
- 3–5 bullets/day; genuinely free or free-tier.
- Format: what it does + free-tier limits + architecture slot note.
- Bias: Project Flux dev, Proxmox homelab, worship/studio workflows.

### Self-Hosting Trend Watch
- 3–5 bullets/day, tagged [home-lab ready] / [SMB-friendly] / [enterprise-grade].
- Covers: Ollama, LM Studio, Jan, LocalAI, oobabooga, GPT4All, Open WebUI,
  self-hosted agent frameworks, cloud vs self-hosted trends, GPU templates.

### Creator Tools
- 3–5 bullets/day across music/audio, video, and design.
- Music: song generation, stem separation, mastering, vocal tools → worship/studio use.
- Video: AI generators, auto-caption, smart cut → lyric reels, event promos, recaps.
- Design: text-to-image, Canva AI, Firefly, SD → Sunday graphics, series key art.

---

### Completely Absent
- package.json / tsconfig.json — no Node.js/TypeScript setup
- pyproject.toml / requirements.txt — no Python package dependencies
- Makefile / Procfile — no task runners or process managers
- docker-compose.yml / Dockerfile — no containerization yet
- nv files — no environment variables defined
- te/Next.js/Nuxt configs — no frontend bundlers

## Delivery Architecture

**Current state:** static HTML served from S3 behind CloudFront. Deployed by a GitHub Action on every push to `main` that touches `html/**` or the manifest builder.

```
html/
├── index.html                   # today's dashboard (landing page)
└── archive/
    ├── index.html               # searchable prior-day browser
    ├── manifest.json            # auto-generated search index (do not edit by hand)
    ├── 2026-04-20.html          # snapshot per day, named YYYY-MM-DD.html
    └── …
```

URLs after deploy:
- `/`                           → today
- `/archive/`                   → searchable archive (text + date-range)
- `/archive/2026-04-20.html`    → a specific prior day
- `/archive/?q=HEMS&from=2026-04-01` → shareable pre-filtered search

### Daily update workflow (librarian)

Every day, produce the new dashboard then snapshot it:

1. Update the `REPORT` object inside `html/index.html` with today's content. Set `REPORT.date` to today in `YYYY-MM-DD` format.
2. Copy the updated file into the archive with today's date:
   ```bash
   cp html/index.html "html/archive/$(date -u +%F).html"
   ```
3. (Optional, done automatically by CI) Regenerate the manifest:
   ```bash
   python scripts/build_manifest.py
   ```
4. Commit and push to `main`. The deploy workflow will:
   - rebuild `html/archive/manifest.json`
   - `aws s3 sync` the whole `html/` tree (including archive)
   - invalidate CloudFront `/*`

The archive page is a pure client-side app: it fetches `manifest.json` and does substring search across each day's title, summary, tags, sources, and keywords (first spotlight + all stories). No server, no index service.

### Hosting Options (historical notes)

 This is a single static HTML file — a dark-themed dashboard with no build step, no framework, no backend. That makes
hosting dead simple. Here are your options from cheapest to most capable:

| Option | Cost | Effort | Best For |
|--------|------|--------|----------|
| here.now (Tailscale Funnel) | Free | Minimal — tailscale funnel /path/to/html | Private/team access via Tailscale, zero
config |
| GitHub Pages | Free | Push to repo, enable Pages | Public static site, auto-deploy on push |
| Cloudflare Pages | Free | Connect repo or wrangler pages deploy html/ | Public, global CDN, fast, custom domain |
| S3 + CloudFront | ~$0.50-1/mo | TF it — S3 bucket + CF distribution + Route53 | AWS-native, custom domain, you already
have the account |
| AWS Amplify Hosting | Free tier (5 GB/mo) | Connect repo or manual deploy | AWS-native, auto-builds on push, custom
domain, preview deploys |

### My recommendation

S3 + CloudFront if you want it in your AWS ecosystem — you already have account 332745420766 with Terraform, and it's a
single HTML file so the cost is essentially zero. I can write the TF module in aws-master-tf.

Cloudflare Pages if you want the fastest path with zero cost and don't care about AWS — npx wrangler pages deploy html/
and you're live.

Amplify is overkill for a single static HTML file with no build step, but makes sense if you plan to add a build
pipeline (e.g., a script that regenerates the dashboard daily and pushes to the repo).



---

## Related Files
- [[homelab-project-index.md]]
- [[projects/flux/architecture/multi-tenant-design.md]]
- [[projects/flux/research/2026-03-hems-market-landscape.md]]

---

## Change Log
| Date       | Version | Notes |
|---|---|---|
| 2026-04-20 | V1      | Initial brief. Task ID: 121fff15770d47d8840b57297aa1c509 |