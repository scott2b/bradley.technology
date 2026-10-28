+++
title = "Narrative Science"
description = "One of the first engineers, turning Northwestern research into production natural language generation in 2010."
weight = 7
template = "page.html"
[extra]
role = "Lead developer, founding engineering team"
start = 2010
end = 2012
+++

<img class="org-logo" src="/images/organizations/narrative-science.jpg" alt="Narrative Science">

I was one of the first engineers at Narrative Science, joining as it incubated out of
Northwestern's [Intelligent Information Laboratory](/experience/infolab/). I had been
working in the lab with {{ person(id="hammond") }} and {{ person(id="birnbaum") }}, who co-founded the
company to commercialize research into systems that turn structured data into
written narrative.

I was there for the transition from research project to software company.

## From research prototype to production

The technology grew out of StatsMonkey, a Northwestern system that generated
baseball stories from game data. The engineering problem was making it run reliably
against real-world data in domains well beyond baseball.

The system did more than fill values into prose templates. Structured input had to
be interpreted into facts: changes, comparisons, rankings, trends, notable events.
Those facts had to be weighed in context to decide which mattered and what role each
played, and only then organized into a narrative structure and written out as text.

Doing that across increasingly different domains meant replacing assumptions built
into individual applications with reusable mechanisms for representing domain
knowledge, analyzing data, deciding what was significant, and constructing narrative
from it.

## Early production applications

**Big Ten Network** — one of the earliest customers: automatically generated
coverage of college sport from structured game data. It was the first production
test of the research, with stories generated reliably and fast from incoming data.

**GameChanger** — stories generated at scale from amateur and youth baseball
scorekeeping, where the audience for any one story might be a handful of families.

**Forbes** and **The Motley Fool** — automated financial and earnings coverage. The
system analyzed corporate results, historical performance, and analyst expectations
to find noteworthy outcomes and write earnings narratives. This was the move from
sport into finance.

**Hanley Wood** — recurring analysis of hundreds of individual U.S. housing markets,
with a localized narrative about conditions in each one.

**A national restaurant operator** — operational reports from location-level sales
and performance data, comparing each restaurant against its peers, with individual
narrative reports and recommendations for franchise owners and managers.

## Two problems at once

The work combined AI research, data processing, architecture, language generation
and production application work, and it had two parts.

**Reasoning about data:** turning raw structured information into facts and
higher-level observations.

**Reasoning about narrative:** deciding which observations mattered, how they
related, what emphasis suited a particular audience, and how the result should be
organized and expressed.

A baseball game, an earnings report, a housing market, and a restaurant's operating
results share no data and no domain knowledge, and all of them went through the same
process.
