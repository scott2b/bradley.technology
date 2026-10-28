+++
title = "Knight Lab Tools"
description = "Internal tools and services built for Knight Lab — deployment and provisioning, content extraction, hashtag recommendation, and Twitter curation."
weight = 16
template = "page.html"
[taxonomies]
capabilities = ["Tools"]
settings = ["Academic"]

[extra]
image = "/images/projects/knight-lab-tools.webp"
print = "/images/projects/knight-lab-tools-print.webp"
tagline = "Deployment, extraction, and curation services"
place = "Knight Lab"
year = "2012–2025"
+++

A lab that ships many small applications needs a different set of tools than one
shipping a single product. These are the ones I built for the Knight Lab.

## git-deploy

Deployment as git subcommands. `git deploy` sends a project to an
environment-specific Ansible configuration; `git secrets` manages its ansible-vault
secrets. Underneath is opinionated scaffolding over Ansible: Ansible knowledge helps
when debugging but is not needed to deploy.

[Source on GitHub](https://github.com/NUKnightLab/git-deploy)

## Provisioning

Provisioning and configuration management for the lab's AWS infrastructure, so that
standing up a new project's environment is a documented process: CloudFormation
templates from 2013, SaltStack from 2014, and Packer and Terraform later.

## Textractor

A service for extracting the content of a web page: the article, without the
navigation, promotions, and boilerplate around it. Nearly everything downstream that
reads the web needs this first.

## Hash#Tagger

{{ mark(src="/images/projects/hashtagger-logo.png", alt="Hash#Tagger") }}

Hashtag recommendation for tweets, from 2012, when reach on Twitter depended heavily
on the tags a message carried. Compose a tweet with a link to a news story, and it
pulled the story's keywords, found the hashtags in use for them, and offered them to
add to the tweet.

## Bonfire

Twitter-based content curation for a circle of users: what the people around you are
reading, in place of an undifferentiated timeline. Seeded with up to fourteen
accounts, it expanded that universe, collected what they tweeted, and ranked the
linked content. A 2014 collaboration between the Knight Lab and Nieman Lab, after
Nieman's Fuego, built with {{ person(id="andrew") }}.

[Source on GitHub](https://github.com/NUKnightLab/bonfire)
