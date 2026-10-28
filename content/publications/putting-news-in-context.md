+++
title = "Putting News in Context, Automatically"
description = "A general architecture and toolkit for systems that find and present the context a reader needs for a news story, with three browser extensions built on it."
weight = 2
template = "publication.html"
[extra]
authors = ["Larry Birnbaum", "Miriam Boon", "Scott Bradley", "Jennifer Wilson"]
venue = "Computation + Journalism Symposium, Columbia University"
venue_short = "C+J 2015"
year = 2015
pdf = "/artifacts/putting-news-in-context.pdf"
lab = "Northwestern University Intelligent Information Laboratory"
+++

Understanding a news story usually means knowing things the article does not
supply: its background, who the people and organizations in it are, how its events
compare with earlier ones, how it looks from other sides. The paper argues that much
of that context can be supplied automatically, and describes the architecture the
InfoLab abstracted from a decade of such systems, among them Tell Me More and
LocalSavvy.

The architecture has six phases: analyze the content, form queries from it, choose
which sources to ask, run the queries and collect the results, rank and extract from
them, and present them beside the original. A Python toolkit covers each phase, so a
new application is a matter of choosing components rather than starting over.

Three browser extensions were built on it. TweetTalk finds personal reactions to a
story on Twitter and filters out the news organizations. Stakeholder Tweetback finds
the verified accounts of the people and organizations in a story and shows what they
have posted about it. Readdit finds the Reddit threads discussing the story. The
paper closes with the next step, a platform that non-programmers could configure to
define the context they want, and the editorial transparency that would bring.

The same work was presented at [IUI 2015](/publications/news-context-project/), and
the toolkit was released as [NUinfolab/context](https://github.com/NUinfolab/context).
