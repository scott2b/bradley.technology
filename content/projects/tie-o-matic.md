+++
title = "Tie-O-Matic"
description = "A computational model of tie selection, built from color theory and then corrected against four hundred human choices."
weight = 23
template = "page.html"
[taxonomies]
capabilities = ["Language & AI"]
settings = ["Academic"]

[extra]
image = "/images/projects/tie-o-matic.webp"
print = "/images/projects/tie-o-matic-print.webp"
tagline = "Modeling a cognitive task"
place = "DePaul CSC 587"
year = "Winter 2007"
+++

The Tie-O-Matic was a model of how people pick a tie to go with a shirt. It began
with color theory, which offers five schemes, and then corrected that theory against
what people actually chose.

It was a team project for DePaul's cognitive science course, taught by
{{ person(id="hastings") }}, with Daniel Watters, {{ person(id="piane") }}, and
Brandon McWilliams. The team's report is [here](/artifacts/tie-o-matic-report.pdf)
(PDF, 21 pages).

A web application showed ten shirts and asked people to pick the best tie for each,
and to give a reason. By the end of February 2007 it had over four hundred choices.
People chose monochrome far more than anything else, rarely chose analogous or
complementary, and never chose the other two schemes, so those two came out of the
model. People also paired red with grey more often than theory predicts, so the
model got a rule for it. And a tie already picked is rated a little lower the next
time, because people like variety.

{{ figure(src="/images/projects/tie-o-matic-results.webp", alt="Nine shirt and tie pairings chosen by the model: a red tie on olive, light blue on blue stripes, a red stripe on red, black on dark pinstripes, and others", caption="Nine of the model's picks, from the report.") }}

The model gave each shirt one color and had no notion of pattern, so a grey shirt
with green in it was simply grey, and nothing stopped a stripe being paired with a
plaid. Reading color pixel by pixel would have fixed both; the course ended first.
