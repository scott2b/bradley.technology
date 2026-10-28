+++
title = "Buzz.com"
description = "An AT&T-funded news aggregator that had 3D virtual characters perform blog stories aloud. I worked on the web application."
weight = 20
template = "page.html"
[taxonomies]
capabilities = ["Language & AI"]
settings = ["Academic"]

[extra]
image = "/images/projects/buzz.webp"
print = "/images/projects/buzz-print.webp"
tagline = "Stories performed by virtual characters"
place = "InfoLab / AT&T"
year = "2007–2008"
+++

{{ mark(src="/images/projects/buzz-beta-banner.webp", alt="buzz.com welcomes you to its closed beta", strip=true) }}

Buzz.com grew out of earlier InfoLab research by {{ person(id="owsley", text="Sara Owsley") }}:
finding the compelling personal stories in blogs automatically and having virtual
characters perform them. That research prototype was published as
[Buzz](https://doi.org/10.1145/1180639.1180705) at ACM Multimedia in 2006. The AT&T
product that followed was a separate build on that research, and I worked on the
team that built its web application. It shipped in December 2007, and AT&T opened it
to the public in 2008.

## What it did

Buzz.com gathered the hot topics of the day and what bloggers were saying about them,
in categories across the top: technology, sports, celebrity, and the rest. Each topic
had a news summary, then the blogs sorted two ways, "Blogs that Make a Point" and
"Blogs that Make You Feel," and a place to leave a comment.

Each story also had a buzzcast. Click the buzz icon and a 3D character performed
the story aloud, by speech synthesis, while you read on or did something else. The characters were designed by Chicago 3D artist {{ person(id="kash") }}.

{{ figure(src="/images/projects/buzz-buzzcaster.webp", alt="One of the buzzcasters: a 3D-rendered young man with curly hair and a red shirt, smiling, against a blue ground", caption="One of the buzzcasters, from the site's closed beta in August 2007.") }}

{{ figure(src="/images/projects/buzz-story-2008.webp", alt="A Buzz.com story page in March 2008: the beta logo, category tabs, a Windows Vista story with its blog reactions, and a Watch Summary panel at the right", caption="A story page in March 2008, from a review at Digital Inspiration.") }}
