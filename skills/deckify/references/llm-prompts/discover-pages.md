# Phase 1a guideline — pick which subpages to fetch

You are running the `web-to-design-system` skill. Phase 1a (`fetch_sitemap.sh`) has dumped a few discovery files into `$WS/recon/`:

- `home.html` — the brand's home page DOM (post-hydration)
- `home.png` — desktop screenshot of the home page
- `nav-links.json` — every `<a>` in `<header>`/`<nav>`/`<footer>` with text, aria, and href
- `sitemap-urls.txt` — flat URL list from sitemap.xml (may be empty if no sitemap)
- `jsonld.json` — JSON-LD blocks from the home page (often contains official logo URL + organization metadata)

Your job: read these, **think like a brand researcher**, and write `$WS/pages.txt` — one URL per line — listing the **5–8 most likely-to-be-rich subpages**. The next script (`fetch_pages.sh`) will batch-fetch every URL in your list.

## What "rich" means here

We are building a Design System. Rich pages are ones likely to expose:

- The **real wordmark** (often shown bigger / cleaner on `/about`, `/brand`, press kits, media kits than on the home header)
- The **brand color palette** (brand-asset / brand-guidelines pages literally list it)
- **Real typography in long-form** (long articles, press releases, product overview pages)
- **The brand's voice and copy register** (about / mission / leadership / case studies)
- **Visual mood** (campaign / featured-work / showcase pages)

## Heuristics, not rules

These are starting hints, not exhaustive. Use judgment based on what this specific site actually shows.

- Look for paths or link text containing: `brand`, `design`, `press`, `media`, `newsroom`, `about`, `who-we-are`, `our-company`, `our-values`, `mission`, `leadership`, `assets`, `style`, `visual-identity`, `careers`, `case-studies`, `customers`, `showcase`, `work`, `campaigns`. (English keywords; equivalent words in the site's language are equally valid.)
- A page in nav with text "Brand" / "Press" / "About" is a near-guaranteed pick.
- The **home page itself** is already fetched by step 1a — do **not** put it back in `pages.txt`.
- Long article-style URLs (`/blog/long-thing-here`) are usually less interesting for visual identity.
- If the site has a brand subdomain visible in nav-links (e.g. `brand.foo.com`, `press.foo.com`), include its index too.
- 5 URLs is a good lower bound, 8 a soft upper. Don't pad.

## What to do when nav-links is sparse

Some sites hide everything behind a hamburger / mega-menu rendered late. Look at:

- **JSON-LD `sameAs` / `url` fields** in `jsonld.json` — sometimes points to brand sub-pages
- **Sitemap depth-1 paths** in `sitemap-urls.txt` — pick top-level paths only (`/about`, not `/about/leadership/john-doe`)
- **Common conventions**: if nothing else works, try direct paths like `<root>/about`, `<root>/press`, `<root>/brand` — fetch_pages.sh will skip ones that 404

## Output format

Plain text file at `$WS/pages.txt`, one absolute URL per line. `#` lines are ignored. Example:

```
# Picked because nav has "About" and JSON-LD declared logo on homepage
https://www.example.com/about
https://www.example.com/about/leadership
https://www.example.com/our-brand
https://www.example.com/press
https://www.example.com/case-studies
```

After writing it, run `bash scripts/fetch_pages.sh $WS/pages.txt $WS` to pull all the pages.
