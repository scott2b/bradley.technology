# bradley.technology

Engineering portfolio site for Scott Bradley

## About

This is a static site built with [Zola](https://www.getzola.org/), a fast static site generator written in Rust. The site showcases engineering projects, credentials, publications, and professional experience.

## Prerequisites

- [Zola](https://www.getzola.org/) (v0.17.0 or later recommended)

## Installation

### Installing Zola

**macOS:**
```bash
brew install zola
```

**Linux:**
```bash
# Debian/Ubuntu
sudo snap install zola --edge

# Or download the latest release from GitHub
wget https://github.com/getzola/zola/releases/download/v0.18.0/zola-v0.18.0-x86_64-unknown-linux-gnu.tar.gz
tar xzf zola-v0.18.0-x86_64-unknown-linux-gnu.tar.gz
sudo mv zola /usr/local/bin/
```

**Windows:**
```bash
# Using Chocolatey
choco install zola

# Using Scoop
scoop install zola
```

Alternatively, download pre-built binaries from the [Zola releases page](https://github.com/getzola/zola/releases).

## Local Development

### Running the Development Server

Start the local development server with live reload:

```bash
zola serve
```

The site will be available at `http://127.0.0.1:1111`

The development server will automatically:
- Rebuild the site when files change
- Reload your browser
- Compile Sass stylesheets
- Generate search index

### Building for Production

To build the site for production:

```bash
zola build
```

The compiled site will be output to the `public/` directory, ready for deployment.

### Building with Draft Content

To include draft posts in your build:

```bash
zola build --drafts
```

## Project Structure

```
bradley.technology/
├── config.toml          # Site configuration
├── content/             # Markdown content files
│   ├── _index.md       # Homepage content
│   ├── projects/       # Project pages
│   ├── portfolio/      # Portfolio items
│   ├── credentials/    # Education & certifications
│   ├── publications/   # Research publications
│   └── ...
├── templates/           # HTML templates
│   ├── base.html       # Base template
│   ├── index.html      # Homepage template
│   └── ...
├── sass/               # Sass stylesheets
├── static/             # Static assets; project plates in static/images/projects
├── image-src/          # Original screenshots and photographs, never edited
├── data/               # marks.toml and shots.toml drive tools/images.py
├── tools/              # images.py and the site checkers
└── public/             # Generated site (not in git)
```

## Content Management

Content is written in Markdown and stored in the `content/` directory. Each section can have:
- `_index.md` - Section index page
- Individual `.md` files for pages

### Front Matter Example

```markdown
+++
title = "Project Name"
date = 2024-01-01
[extra]
description = "Project description"
+++

Content goes here...
```

## Images

Every project page has an `image` in its front matter, and it is always the same
object: a 1200×600 WebP at `static/images/projects/<slug>.webp`. The templates draw one
frame around every image and never ask what kind of picture it is. Two things produce
those files, both through `tools/images.py`.

- **Shots** are screenshots and photographs. They are evidence and never go through a
  model. Originals live in `image-src/projects/` and are never edited;
  `data/shots.toml` says how each one becomes a plate.
- **Marks** are generated drawings for work that has no picture worth showing, or whose
  only capture is a thumbnail. One art direction and a one-line subject per project live
  in `data/marks.toml`. An image model draws them through OpenRouter.

Requirements: Python 3 with Pillow, and for marks an `OPENROUTER_API_KEY` in `.env`
(gitignored). Load it before running anything that generates:

```bash
set -a; source .env; set +a
```

### Adding or updating a screenshot

1. Put the original in `image-src/projects/`.
2. Add an entry to `data/shots.toml`. `fit = "crop"` fills the plate and takes the 2:1
   window `anchor` of the way down the source (0.0 top, 1.0 bottom; screenshots use 0
   so the product's own headline survives). `fit = "matte"` places the image on the
   off-white ground at its own size, never enlarged, with a hairline round it.
3. Run `python3 tools/images.py frame <slug>`. It writes the plate and points the
   page's front matter at it. Free and instant; `frame` with no slug rebuilds all of
   them.

If a page also shows the full screenshot as a figure in its body, serve that from
`static/images/projects/` under its original name; the plate is only ever the crop.

### Making or iterating on a mark

1. Write or edit the project's subject in `data/marks.toml` under `[projects.<slug>]`.
   Say what the picture is about in a sentence or two. The direction under
   `[styles.blueprint]` says how it should look, and it is shared by the whole set, so
   do not restate style in a subject and do not ask for text in the image.
2. Generate candidates. Each costs about $0.13 and takes about 90 seconds:

   ```bash
   python3 tools/images.py marks <slug> --style blueprint --n 3 --budget 1.00
   ```

   `--budget` stops the run when the session's cost reaches that figure. Candidates
   land in the gitignored `image-work/<slug>/` as `blueprint-1.png`, `blueprint-2.png`
   and so on, and every call is logged with its cost in `image-work/log.jsonl`.
3. Compare them. `python3 tools/images.py sheet <slug>` lays the candidates out in
   one image at `image-work/<slug>/sheet.png`. Judge them as pictures on the site, not
   on how closely they followed the brief.
4. Promote the one you want: `python3 tools/images.py promote <slug> blueprint-2`.
   This writes the plate and points the page at it.
5. Run `python3 tools/images.py check`. It fails if any project image is missing or
   is not 1200×600.

The other directions in `data/marks.toml` (isometric, editorial, render) were tried
and set aside; `--all-styles` draws one of each if you want to revisit that. Mixing
directions across projects breaks the set, so if a direction changes, it changes for
every mark.

### Site plates

A drawing that belongs to the site rather than to a project lives under `[site.<name>]`
in `data/marks.toml` and goes through the same `marks`, `sheet` and `promote` steps.
`promote` writes it to `static/images/<name>.webp` and touches no page; a template
references it directly. There is one so far: `sheet-00`, the general-arrangement
drawing under the headline on the home page, whose subject describes the themes the
work runs across rather than any project, so it does not go stale as the project set
changes.

## Configuration

Site-wide settings are in `config.toml`:
- `base_url` - Production URL
- `title` - Site title
- `compile_sass` - Enable Sass compilation
- `build_search_index` - Enable search functionality
- `minify_html` - Minify output HTML

## Deployment

The site is configured to build to the `public/` directory. Deploy this directory to your hosting provider of choice (Netlify, Vercel, GitHub Pages, etc.).

## Learn More

- [Zola Documentation](https://www.getzola.org/documentation/)
- [Zola Templates](https://www.getzola.org/documentation/templates/overview/)
- [Markdown Syntax](https://www.markdownguide.org/basic-syntax/)
