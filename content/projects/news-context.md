+++
title = "The News Context Project"
description = "An open-source toolkit for assembling the context around a news article — related discussion, circulating quotations, and what the people named in it are saying elsewhere."
weight = 17
template = "page.html"
[taxonomies]
capabilities = ["Language & AI"]
settings = ["Academic"]

[extra]
image = "/images/projects/news-context.webp"
print = "/images/projects/news-context-print.webp"
tagline = "Context for news articles"
place = "Northwestern InfoLab"
year = 2015
+++

A news story is rarely self-contained. Understanding one usually means knowing what
else has been written on the subject, what the people named in it have said
elsewhere, and how the discussion around it has moved since.

The News Context Project was an open-source toolkit, built at Northwestern's
InfoLab in 2015, for assembling that material automatically and presenting it next
to the story. It analyzed the page a reader was on, formed queries from its terms and
named entities, sent them to the right sources, and ranked and presented what came
back. Each application built on it was a different choice of source and of what
counted as relevant.

**TweetTalk** found personal comments on a story on Twitter, filtering out the news
organizations to favor individual reactions. **Stakeholder Tweetback** identified the
people and organizations in a story, found their verified accounts, and showed what
they had posted about it. **readdit** found the Reddit discussion threads about it.
Each ran as a browser extension or through a web interface.

{{ figure(src="/images/projects/news-context-tweettalk.webp", alt="TweetTalk: four tweets reacting to the January 2015 Paris march, in a pop-up beside the article", caption="TweetTalk on a January 2015 New York Times story about the Paris march, from the IUI paper.") }}

{{ figure(src="/images/projects/news-context-readdit.webp", alt="readdit: the keywords drawn from a BBC story on the Paris attacks, and fourteen related Reddit threads", caption="readdit on a BBC story about the Paris attacks: the extracted keywords and the threads found for them.") }}

The work was published as
[The News Context Project](/publications/news-context-project/) at IUI 2015, with
{{ person(id="birnbaum") }}, {{ person(id="boon") }}, and {{ person(id="wilson") }}.
The source was released as
[NUinfolab/context](https://github.com/NUinfolab/context), MIT licensed.

## Built with

Python, with NLTK for the text analysis and Flask for the web application; the
browser extensions were built with Kango.
