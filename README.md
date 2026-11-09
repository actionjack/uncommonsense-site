# uncommonsense-uk.com

The Uncommon Sense website. Plain HTML and CSS, no build step, hosted free on GitHub Pages.

## Edit

- Words: `index.html`. If you change a service or an FAQ answer, change the matching text in the
  `application/ld+json` block at the top and in `llms.txt` too, so AI tools read the same thing.
- Colours, type and spacing: `styles.css` (tokens at the top).
- Client quotes: the "What people say" section is commented out in `index.html` until there are
  three real, agreed quotes.

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
