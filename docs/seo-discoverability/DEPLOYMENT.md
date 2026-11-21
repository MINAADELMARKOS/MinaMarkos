# Verified public deployment — 22 November 2026

- Site: https://minaadelmarkos.github.io/MinaMarkos/
- Implementation commit: `24b7719a2fa56af1179e39de76069403b504bb09`.
- GitHub Pages: matching commit **built**, legacy build from `main` at `/`; no build error. Exact API evidence: [pages-build.json](pages-build.json).
- Public HTTPS verification: **82 checked site responses, zero failures**; every checked resource returned HTTP 200 and matched the validated source bytes. TLS verification remained enabled. See [public-after.json](public-after.json).
- Coverage includes all 35 canonical HTML pages, the explicit `/index.html` alias, both noindex legacy templates, sitemap, project-level robots file, social/visible images, page-linked styles/scripts and the original CV PDF. No checked response carried an X-Robots-Tag exclusion; canonical HTML and page-level indexing directives match source.
- Origin-root `/robots.txt` returned 404, as documented in the audit; it is not an exclusion. Search indexing, rankings and account-side sitemap acceptance are not inferred from HTTP success.

This record and the HTTP evidence are committed after the implementation deployment. The follow-up documentation commit does not change public page or asset bytes; the final Pages build and public-byte check are repeated before handoff.
