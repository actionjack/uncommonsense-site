# uncommonsense-uk.com

The Uncommon Sense website. Plain HTML and CSS, no build step, hosted free on GitHub Pages.

## Edit

- Words: `index.html`. If you change a service or an FAQ answer, change the matching text in the
  `application/ld+json` block at the top and in `llms.txt` too, so AI tools read the same thing.
- Colours, type and spacing: `styles.css` (tokens at the top).
- Client quotes: the "What people say" section is commented out in `index.html` until there are
  three real, agreed quotes.

## Writing pages

- Each post is a file in `posts/` (front-matter format at the top of `build.py`), with its image
  in `assets/writing/`. Run `python3 build.py` after any change: it rebuilds `writing/`, the three
  newest cards on the home page, `sitemap.xml` and the Writing list in `llms.txt`. Do not edit
  those generated parts by hand.
- Which posts go up is decided by the daily LinkedIn performance check: posts at least 7 days old
  with 200+ impressions and 2+ reactions and comments, or 100+ impressions at a 3.5%+ rate. It
  adds the files and builds, but never commits. Review with `git status`, then commit and push.
- The text is the post as published on LinkedIn, word for word, hashtags removed. The one
  exception: a joke or aside that could read as dismissive of a group when quoted out of context
  is cut (deletion only, never reworded) and recorded as `site_edit:` in the post's front matter.

## Publish on GitHub Pages

1. Create a public repo on GitHub and push this folder to `main`.
2. Repo Settings > Pages > Source: "Deploy from a branch", branch `main`, folder `/ (root)`.
3. Same page, Custom domain: `uncommonsense-uk.com`, then tick "Enforce HTTPS" once it is offered.
4. At the domain registrar, replace the current website records (they point at forwarding
   addresses today) with:
   - `A` records for `@`: `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
   - `CNAME` for `www`: `actionjack.github.io`
   - Leave the `MX` records alone. They carry your Google email.

## Get found by search and AI tools

- Add the site to Google Search Console and Bing Webmaster Tools and submit `sitemap.xml`.
  Bing matters for AI: ChatGPT search and Copilot draw on its index.
- Link the site from the LinkedIn profile (Contact info > Website) and the company page.
- Every post that gets its own page on the site later goes into `sitemap.xml` and `llms.txt`.
