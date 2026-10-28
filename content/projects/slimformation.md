+++
title = "Slimformation"
description = "A browser extension that measured what you read: time by content category, the sources behind it, and whether you met the goals you set."
weight = 21
template = "page.html"
[taxonomies]
capabilities = ["Applications & data", "Language & AI"]
settings = ["Academic"]

[extra]
image = "/images/projects/slimformation.webp"
print = "/images/projects/slimformation-print.webp"
tagline = "Measuring an information diet"
place = "Knight Lab"
year = "2013"
+++

Slimformation was a browser extension that tracked what you read. After a week of
normal reading it showed how much time you had spent on politics, business,
technology, science, sports, and entertainment, and the top sources in each. A
reader could set a goal for each category, and it tracked whether the goal was met.
It also estimated the reading level of the sources.

{{ figure(src="/images/projects/slimformation.png", alt="The Slimformation panel: reading activity broken down by category, with top sources per category") }}

{{ figure(src="/images/projects/slimformation-goals.webp", alt="The Goals tab: for each category, a bar of actual reading time against the goal") }}

Every page was sorted into a topic in the browser and the record stayed in local
storage, so nothing was sent anywhere.

The idea came out of the election-hacking session at the 2012 Mozilla Festival, from
a group that included {{ person(id="birnbaum") }} and {{ person(id="germuska") }}. The
first version was a Chrome extension built in spring 2013 by {{ person(id="zhu") }},
Basil Huang, Amelia Kaufman, and {{ person(id="singh") }} in Northwestern's joint class
in journalism and technology; [their code](https://github.com/Slimformation/slimformation)
is on GitHub. I refactored the prototype at the Lab that autumn and added a Firefox
add-on alongside the Chrome extension, released in
[October 2013](https://knightlab.northwestern.edu/2013/10/24/slimfo-gets-a-new-name-and-adds-firefox-compatablity/).

{{ figure(src="/images/projects/slimformation-download.webp", alt="The Knight Lab's Slimformation page: the name, Read Smarter, and download buttons for Chrome and Firefox", caption="The Knight Lab's download page, October 2013.") }}
