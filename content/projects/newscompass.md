+++
title = "News Compass"
description = "Harvests science journalism from the GDELT Global Knowledge Graph, extracts the citations inside it, and enriches the cited papers against Crossref, arXiv, NCBI and OpenAlex."
weight = 1
template = "page.html"
[taxonomies]
capabilities = ["Applications & data", "Systems"]
settings = ["Academic"]

[extra]
image = "/images/projects/newscompass.webp"
print = "/images/projects/newscompass-print.webp"
tagline = "Tracing science reporting back to its sources"
place = "Knight Lab"
year = "2026"
+++

News Compass is a continuous harvester that pulls science articles from the
[GDELT Global Knowledge Graph](https://www.gdeltproject.org/), extracts the
citations embedded in them, and enriches the cited papers against Crossref, arXiv,
NCBI, and OpenAlex. The results are served through a read-only JSON API backed by
Meilisearch, with a Vue single-page front end.

Science journalism routinely refers to research without linking to it. News Compass
reconstructs the path from a story back to the paper, automatically and at scale.

## Technical notes

Python harvesting pipeline with a durable filesystem document store that the search
indexes are rebuilt from. Meilisearch is the engine the application reads; the
search layer was selected through a benchmark harness that also evaluated Typesense,
Weaviate, and Qdrant.

## Collaboration

Built at Northwestern University's Knight Lab, in connection with {{ person(id="nishal", text="Sachita Nishal's") }} research in the Northwestern Computational Journalism Lab. The system is described
in [Designing for Field Awareness in Science Journalism](https://nishalsach.github.io/pdfs/2026-news-compass-cscw.pdf)
({{ person(id="nishal", text="Nishal") }}, {{ person(id="horvat", text="Horvát") }}, and {{ person(id="diakopoulos", text="Diakopoulos") }}), in the companion proceedings of CSCW 2026,
doi 10.1145/3785651.3831513.

News Compass was an invited demo at the
[Computation + Journalism 2026 Symposium](https://www.cj2026.northwestern.edu/schedule/#demos)
at Northwestern, presented by {{ person(id="nishal") }} on 2 October 2026.
