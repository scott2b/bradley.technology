+++
title = "ADAMA"
description = "ADAMA, an IARPA-funded effort to detect and interpret metaphor automatically across four languages, at IIT's Linguistic Cognition Laboratory."
weight = 7
template = "page.html"
[taxonomies]
capabilities = ["Language & AI"]
settings = ["Academic"]

[extra]
tagline = "Scalable Cross-Lingual Metaphor Identification and Conceptual Analysis"
image = "/images/projects/adama.webp"
print = "/images/projects/adama-print.webp"
+++

ADAMA stands for Autonomous Dynamic Analysis of Metaphor and Analogy. It was a
system for finding metaphors in large amounts of text, in four languages, and
working out what they meant.

The idea came from IARPA's Metaphor program. People show how they think about a
subject in the metaphors they use for it, and so does a culture. If a system could
find those metaphors in the text a population writes online, analysts could read
them for the beliefs underneath. The four languages were American English, Iranian
Farsi, Mexican Spanish, and Russian.

## Approach

The system read very large amounts of online text and pulled out the metaphors in
it. Psychologists and cultural experts reviewed what it found, and the results went
into a repository of the metaphors each language uses. The software did the part
that only works at scale. The experts decided what a metaphor said about the people
who used it.

The intended users were in forensics, intelligence analysis, business analysis,
sociological research and communication studies.

## The project

Led by {{ person(id="argamon") }} at the Illinois Institute of Technology, with the
Massachusetts Institute of Technology, Georgetown University, Ben-Gurion University
of the Negev, Bar-Ilan University, and the Center for Advanced Defense Studies.

{{ person(id="ortony") }} of Northwestern University, a psychologist whose work is on metaphor
and on emotion, consulted to the project in 2013 and 2014. He is a co-author of the
team's 2014 paper on
[language-independent ensemble approaches to metaphor identification](https://cdn.aaai.org/ocs/ws/ws1202/8784-38080-1-PB.pdf).
Illinois Tech also
[announced](https://www.iit.edu/news/renowned-artificial-intelligence-pioneer-marvin-minsky-joins-illinois-institute-technology-metaphor)
{{ person(id="minsky") }} joining the project in December 2012.

The work ran under IARPA — the Intelligence Advanced Research Projects Activity —
through the U.S. Army Research Laboratory, from January 2012 to January 2014.
Illinois Tech announced it in
[April](https://www.iit.edu/news/argamon-team-receives-iarpa-grant) and
[May](https://www.iit.edu/news/illinois-institute-technology-leading-international-project-automatically-understand-metaphors-large)
of 2012.

## Role

Contract programmer, 2012 to January 2014 — NLP development at the Linguistic
Cognition Laboratory, building the affect classification subsystem within the Java
system that detected and extracted metaphor from text.

Worked alongside {{ person(id="argamon") }}, {{ person(id="kanareykin") }},
{{ person(id="taylor") }}, {{ person(id="rasooli") }}, and {{ person(id="gandy") }}.

{{ mark(src="/images/projects/lingcog-logo.png", alt="Linguistic Cognition Laboratory") }}

The lab worked where machine learning meets computational linguistics. Its subject
was the non-referential side of text: how a document is organized and styled, apart
from what it is about, and how that style varies between individuals and groups.

## Further reading

Argamon's group published this research while the system was being built.

- [Automatic Identification of Conceptual Metaphors with Limited Knowledge](https://ojs.aaai.org/index.php/AAAI/article/view/8648) — Gandy et al., AAAI 2013
- [Language-Independent Ensemble Approaches to Metaphor Identification](https://cdn.aaai.org/ocs/ws/ws1202/8784-38080-1-PB.pdf) — Dunn et al., AAAI 2014 workshop on Cognitive Computing
- [Metaphor Identification in Large Texts Corpora](https://doi.org/10.1371/journal.pone.0062343) — Neuman et al., PLOS ONE, 2013
