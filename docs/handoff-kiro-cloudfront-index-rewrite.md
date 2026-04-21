# Hand-off: CloudFront index-document rewrite for `ai-news-dashboard`

**To:** Kiro / Seinfeld
**From:** Ron (via Computer)
**Date:** 2026-04-21
**Repo impacted:** `aws-master-tf` (Terraform module that provisions the `ai-news-dashboard` distribution)
**Related repo (FYI, no changes needed there):** [mojosailor/ai-news-dashboard](https://github.com/mojosailor/ai-news-dashboard)
**AWS account:** `992382519644` · **Region for bucket:** `us-east-1` · **CloudFront functions live in:** `us-east-1`

---

## Problem

After shipping the dated archive feature ([PR #3](https://github.com/mojosailor/ai-news-dashboard/pull/3), merged & deployed 2026-04-21 13:55 UTC), the site's CloudFront distribution returns `403 AccessDenied` for "directory" URLs because the distribution has no default root object and no viewer-request rewrite for subfolder `index.html` resolution.

### Current behavior (verified via `curl -sI`)

| URL | Status | Notes |
|---|---|---|
| `https://news.harmonygrid.ai/` | **403** | No default root object |
| `https://news.harmonygrid.ai/index.html` | 200 | File exists in S3 |
| `https://news.harmonygrid.ai/archive/` | **403** | No subfolder index rewrite |
| `https://news.harmonygrid.ai/archive/index.html` | 200 | File exists in S3 |
| `https://news.harmonygrid.ai/archive/manifest.json` | 200 | Works |
| `https://news.harmonygrid.ai/archive/2026-04-20.html` | 200 | Works |
| `https://news.groovegrid.ai/` (same distribution) | **403** | Same gaps |

Both apex-aliased domains (`news.harmonygrid.ai`, `news.groovegrid.ai`) point at the same distribution, so a single fix covers both.

---

## Required change (Terraform)

In whatever module defines `aws_cloudfront_distribution` for this site (likely under `aws-master-tf/modules/ai-news-dashboard/` or similar — confirm path before editing), make **two** additions:

### 1. Set the default root object

```hcl
resource "aws_cloudfront_distribution" "ai_news_dashboard" {
  # ... existing config ...

  default_root_object = "index.html"

  # ... rest unchanged ...
}
```

This fixes `https://news.harmonygrid.ai/` → serves `/index.html`.

### 2. Add a CloudFront Function for subfolder index rewrite

CloudFront Functions are cheaper and faster than Lambda@Edge and sufficient here (pure URI rewrite, no network calls, sub-ms latency, ~$0.10 per 1M invocations).

```hcl
resource "aws_cloudfront_function" "index_rewrite" {
  name    = "ai-news-dashboard-index-rewrite"
  runtime = "cloudfront-js-2.0"
  comment = "Rewrite / and /folder/ to /index.html so S3 origin serves directory indexes. See handoff-kiro-cloudfront-index-rewrite.md in mojosailor/ai-news-dashboard."
  publish = true
  code    = <<-EOT
    function handler(event) {
      var req = event.request;
      var uri = req.uri;

      // "/" -> "/index.html"  (redundant with default_root_object, but harmless
      // and makes the behavior explicit if default_root_object is ever removed)
      if (uri === "/") {
        req.uri = "/index.html";
        return req;
      }

      // "/archive/" or any "/folder/" -> "/folder/index.html"
      if (uri.endsWith("/")) {
        req.uri = uri + "index.html";
        return req;
      }

      // "/archive" (no trailing slash, no file extension) -> "/archive/index.html"
      // Only rewrite when there's no "." in the final segment (so .html/.json/.css pass through).
      var lastSegment = uri.substring(uri.lastIndexOf("/") + 1);
      if (lastSegment.length > 0 && lastSegment.indexOf(".") === -1) {
        req.uri = uri + "/index.html";
        return req;
      }

      return req;
    }
  EOT
}
```

### 3. Attach the function to the default cache behavior

Inside the existing `default_cache_behavior` block, add:

```hcl
default_cache_behavior {
  # ... existing target_origin_id, viewer_protocol_policy, etc. ...

  function_association {
    event_type   = "viewer-request"
    function_arn = aws_cloudfront_function.index_rewrite.arn
  }
}
```

> If there are additional `ordered_cache_behavior` blocks (e.g. one for `/archive/*`), attach the same `function_association` there too — otherwise the rewrite won't fire for paths matched by those behaviors.

---

## Out of scope but worth checking while you're in there

1. **Origin Access Control.** Confirm the S3 bucket policy only allows `GetObject` via the distribution's OAC (no public-read on the bucket itself). Not directly related to this fix, but worth a glance.
2. **Custom error responses.** Consider mapping 403/404 → `/index.html` with status 200 only if you ever add a SPA. For this static multi-page site, *don't* enable that — it would mask legitimate missing-file errors from the archive.
3. **Cache policy on `manifest.json`.** The archive page fetches it with `cache: 'no-cache'` on the client side, but CloudFront's default TTL may still serve stale manifests to first-time viewers in a region for up to the default TTL window. Consider a short max-age (e.g., 60s) or explicit cache headers on `manifest.json`. The deploy workflow invalidates `/*` after each sync, so this is mostly theoretical.

---

## Acceptance criteria

After `terraform apply` (and any required CF distribution propagation — typically 2–5 min, occasionally up to 15):

```bash
# All should return 200
curl -sI https://news.harmonygrid.ai/                          | head -1
curl -sI https://news.harmonygrid.ai/archive/                  | head -1
curl -sI https://news.groovegrid.ai/                           | head -1
curl -sI https://news.groovegrid.ai/archive/                   | head -1

# Should still return 200 (regression check)
curl -sI https://news.harmonygrid.ai/index.html                | head -1
curl -sI https://news.harmonygrid.ai/archive/index.html        | head -1
curl -sI https://news.harmonygrid.ai/archive/2026-04-20.html   | head -1
curl -sI https://news.harmonygrid.ai/archive/manifest.json     | head -1

# Should still 403 (file genuinely gone — do NOT add error-response masking)
curl -sI https://news.harmonygrid.ai/daily-intel-dashboard.html | head -1
```

End-to-end: clicking the "Archive" button on `https://news.harmonygrid.ai/` lands on a populated archive page with at least one entry (2026-04-20).

---

## Rollback

If anything misbehaves:

1. Dissociate the function by removing the `function_association` block and `terraform apply`.
2. Or, in the CloudFront console, edit the distribution's default cache behavior → Function associations → set viewer-request to **No association** → Save.

The function itself can live unused; it only executes when associated.

---

## Context / background

- The dashboard repo now has `html/index.html` (today), `html/archive/index.html` (searchable browser), `html/archive/YYYY-MM-DD.html` (dated snapshots), and `html/archive/manifest.json` (search index, rebuilt by CI on every deploy).
- Deploy workflow: [.github/workflows/deploy.yml](https://github.com/mojosailor/ai-news-dashboard/blob/main/.github/workflows/deploy.yml) — assumes role `arn:aws:iam::992382519644:role/ai-news-dashboard-deploy`, syncs `html/` to `s3://ai-news-dashboard-992382519644/`, invalidates `/*`.
- `CF_DISTRIBUTION_ID` is stored as a GitHub Actions secret on the repo — grab it from there (or from the Terraform output) if you need it for manual invalidation testing.
- Librarian daily workflow: edit `html/index.html`, `cp` it to `html/archive/$(date -u +%F).html`, commit, push. No Terraform changes needed per-day — this is a one-time infra fix.

---

## Task checklist for Kiro

- [ ] Locate `aws_cloudfront_distribution` resource for `ai-news-dashboard` in `aws-master-tf`
- [ ] Add `default_root_object = "index.html"` to that resource
- [ ] Add `aws_cloudfront_function.index_rewrite` resource (code above)
- [ ] Add `function_association` (viewer-request) to the default cache behavior
- [ ] `terraform plan` — confirm only the distribution is modified and one function is created
- [ ] `terraform apply`
- [ ] Wait for distribution status = `Deployed` (check `aws cloudfront get-distribution --id <id>` or the console)
- [ ] Run the acceptance `curl` commands above
- [ ] Post results in the PR / ticket and close
