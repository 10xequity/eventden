# Event-Den — event-den.com

Static HTML/CSS/JS site (11 pages + 404). No build step. Shared `assets/css/styles.css` + `assets/js/main.js`.
`build.py` is the generator used to produce the pages — you can delete it or keep it for regenerating; the HTML files are the deliverable.

## Deploy: GitHub Pages + Cloudflare

1. **Repo:** push this folder to a GitHub repo. Settings → Pages → Deploy from branch (`main`, root). `.nojekyll` is included.
2. **Custom domain:** add `event-den.com` in Pages settings; create a `CNAME` file if GitHub doesn't auto-add it.
3. **Cloudflare DNS:** apex `A` records → GitHub Pages IPs (185.199.108–111.153), `www` CNAME → `<user>.github.io`, both proxied (orange cloud).
4. **Canonical:** [TODO #7] confirm apex vs `www`; add a Cloudflare Redirect Rule to 301 the loser. Canonicals in HTML currently point to the apex.
5. **SSL/TLS:** mode **Full (strict)**. Edge Certificates → Always Use HTTPS = on, HSTS = on (start max-age 6 months; raise before any preload).
6. **Security headers:** Rules → Settings → Managed Transforms → enable **"Add security headers"** (X-Content-Type-Options, X-Frame-Options, Referrer-Policy). Target securityheaders.com **grade B** at launch.
7. **CSP plan (→ grade A):** deploy via a Cloudflare Response-Header Transform Rule as `Content-Security-Policy-Report-Only` first:
   `default-src 'self'; img-src 'self' https://images.unsplash.com data:; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src https://fonts.gstatic.com; script-src 'self'; frame-src https://maps.google.com https://www.google.com https://docs.google.com; base-uri 'self'; form-action 'self' https://docs.google.com`
   Watch reports, then switch header to enforcing `Content-Security-Policy`. (`unsafe-inline` for styles is needed by inline `style=` attributes; refactor later to drop it.)
8. **Search Console:** verify domain, submit `https://event-den.com/sitemap.xml`.

## Open items (TODO flags are visible in-page and in comments)

1. Bar/café name — "Oda Bar & Cafe" vs "Oda Up" — VERIFY before launch.
2. Real phone (placeholder must not ship).
3. Public email inbox.
4. Real social URLs or remove footer mention.
5. Capacities (full/half facility, event areas, court configs) — venue.html table + celebrations.html.
6. Google Form URL — paste iframe into `inquiry.html` (commented slot is ready).
7. Canonical domain decision + 301.
8. Outbound links for Oda / Social Den / FieldhouseUSA / Boomtown.
9. Published "starting at" figures per category, or inquiry-only.

## Post-launch backlog

- Replace Unsplash placeholders with real event photography (compress: <200KB content, <400KB hero; WebP with fallback).
- Add real `og:image` (1200×630) hosted on-domain.
- Enforce CSP (grade A); revisit HSTS max-age/preload.
- Add `BreadcrumbList` JSON-LD to deep pages; expand FAQ schema as FAQs grow.
- Populate `sameAs` socials in JSON-LD once accounts are confirmed.
- Add testimonials/reviews + `AggregateRating` once collected.
- Event-type × location long-tail pages (e.g. "quinceañera venue Aurora") after location pages index.

## Notes

- Pricing copy everywhere is "starting from / illustrative" and funnels to the inquiry form.
- Brokerage disclaimer (no guarantee of third parties) appears on rentals-brokerage.html and legal.html.
- Wedding/event *planning* is referred out; the internal events coordinator is offered at an additional fee — both stated on relevant pages.
- No PII is collected on-domain; the form is offloaded to Google Forms.


## Go-live checklist (current blockers)

**Must fix before DNS cutover:**
1. Phone & email — visible TODO badges ship on contact/footer/inquiry.
2. Google Form URL → paste into inquiry.html (commented slot ready).
3. **Testimonials are PLACEHOLDERS (fictional).** Publishing invented reviews violates FTC endorsement rules — replace all 6 with real, permissioned client quotes (or remove the section) before launch.
4. Verify "Oda Bar & Cafe" vs "Oda Up".
5. Champagne hero images are Unsplash placeholders — verify both load (graceful-hide fallback included) and replace with owned bottle photography.
6. Court count + finished-area details on venue table.
7. Social links: add real or delete footer mention.
8. CNAME file included (event-den.com apex) — confirm apex vs www, 301 the other in Cloudflare.

**Recommended at launch:** Search Console verification + sitemap submit; Cloudflare Web Analytics (cookieless); favicon.svg included; 404.html included; run securityheaders.com after enabling Managed Transforms; Lighthouse mobile pass (target 90+); legal page counsel review.
