+++
title = "The Local Angle"
description = "Surfacing national stories with local significance by linking articles to the places behind the people and organizations in them."
weight = 18
template = "page.html"
[taxonomies]
capabilities = ["Language & AI"]
settings = ["Academic"]

[extra]
image = "/images/projects/local-angle.webp"
print = "/images/projects/local-angle-print.webp"
tagline = "Finding local relevance in national news"
place = "Northwestern InfoLab"
year = 2012
+++

A national story can matter to a town it never mentions: the executive at its center
grew up there, or the company involved is headquartered down the road. Anyone
scanning by dateline misses that.

The Local Angle, released by the Knight Lab in 2012, found the people, companies,
and organizations in national news stories and tied them to places: a person's
birthplace or residence, a company's headquarters. Pick a state, and it listed the
stories with a tie to each of its cities, labeled with who the tie was and what kind.

{{ figure(src="/images/projects/local-angle-map.webp", alt="The Local Angle. Find locally relevant stories in national news. Below the title, a map of the United States with each state outlined, to pick a state from", caption="Home page map.") }}

{{ figure(src="/images/projects/local-angle-illinois.webp", alt="The Local Angle for cities in Illinois: a table of city, local angle, and the story it was mentioned in, from Blue Island and Curtis Granderson down to Eureka and Ben Zobrist", caption="Illinois page.") }}

{{ figure(src="/images/projects/local-angle-ties.webp", alt="A story titled 'What to expect from Intel at CES' tied to Cupertino through Apple's headquarters, to San Francisco through Paul Otellini's birthplace, and to Santa Clara through Intel's headquarters", caption="A story and its geographic ties, from the IUI 2013 paper.") }}

Stories came from the Google News Search API, AlchemyAPI found the entities, and
DBpedia supplied the places. Within a city the stories were ranked to favor entities
that were prominent in the story and less famous overall, so that a national story
about someone with an unobvious local tie rose above the daily Obama coverage under
Honolulu.

Published as
[Finding the Local Angle in National News](/publications/local-angle/) at IUI 2013,
with {{ person(id="obanion") }} and {{ person(id="birnbaum") }}.
