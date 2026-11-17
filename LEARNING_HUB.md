# Engineering learning hub

The site is static HTML, CSS and vanilla JavaScript, compatible with the existing GitHub Pages publication path. No runtime framework, CDN highlighting library, or client-side content fetch is required.

## Editing

- `content/hub_articles.py`: original article titles, categories, summaries, section prose, conceptual diagrams and discussion questions.
- `content/existing_articles.json`: preserved source prose from all six earlier articles. Overlapping topics reuse those URLs, and the earlier useful text is retained under project/operating context.
- `tools/build_learning_hub.py`: shared template, server-rendered syntax highlighting, TOC, metadata, related links, blog cards/category directory, sitemap and distribution drafts.
- `css/home-blog-navigation.css`: scoped homepage navigation sizing for the longer blog label.
- `css/learning-hub.css`, `js/learning-hub.js`: responsive reading layout and progressive enhancement.
- `examples/`: independently runnable Kafka Java and PySpark labs with versions, prerequisites, expected results, troubleshooting and validation boundaries.
- `distribution/`: 12 manual-review LinkedIn posts, video scripts, and three discussion questions per tutorial. Nothing is automatically posted externally.

Run `python3 tools/build_learning_hub.py` after editing source, then `python3 tools/validate_learning_hub.py`. Commit both source and generated pages. The builder is deterministic and runs from any working directory using Python's standard library. Article dates are the editorial publication date, not the machine build time; update dates deliberately when revising content.

There are 21 article URLs: twelve tutorials, six Engineering Perspectives (three expand existing URLs), and three preserved project/architecture articles. Categories may overlap; the directory has eight requested categories. The library and static topic anchors work without JavaScript; search, filtering and clipboard controls enhance them when available.

The Kafka CLI repository and Spark lecture materials informed topic selection, but the Java/PySpark labs and teaching diagrams are original. Old ZooKeeper-era commands, absolute action-to-job assumptions, and Colab-specific notebook setup were not reproduced as current instructions. See `examples/VALIDATION.md` for reviewed revisions and actual test results.

## Validation and publication

See `examples/VALIDATION.md` and each lab README. Browser checks require Playwright and Chromium and run against a local HTTP server. The website itself has no npm dependency.

Use the repository's existing Pages publishing configuration; do not create a second deployment workflow. After pushing, inspect the Pages build and check the public blog plus representative article, stylesheet, script, code and sitemap URLs. A push is not proof of deployment. The current environment blocks the public Pages host and GitHub API, so live deployment verification remains an external prerequisite until those destinations are allowed.
