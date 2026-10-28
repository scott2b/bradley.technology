+++
title = "City Hall Monitor"
description = "A searchable index of Chicago City Council records, built so an investigator can find the documents worth reading."
weight = 15
template = "page.html"
[taxonomies]
capabilities = ["Applications & data"]
settings = ["Academic"]

[extra]
tagline = "Smart search for city documents"
place = "Knight Lab"
year = "2015–2016"
image = "/images/projects/cityhallmonitor.webp"
print = "/images/projects/cityhallmonitor-print.webp"
+++

Chicago City Council publishes thousands of records a year, and most of them are
routine: permits, sidewalk cafés, awnings, congratulations. City Hall Monitor was a
searchable index of all of them, built at the Knight Lab in 2015 and 2016 so that a
reporter could find the few that are news.

Council matters and their attachments were pulled from the council's Legistar
system. Each document went to DocumentCloud for its text and page images, and
PostgreSQL full-text search indexed the result, weighted toward titles and sponsors.
A search could be limited to the last thirty days, the past year, or all time, and a
subscription saved a search and sent an email when a new document matched it.

{{ figure(src="/images/projects/cityhallmonitor.png", alt="The City Hall Monitor search page") }}

## Ignore the boring stuff

A checkbox, on by default, excluded the routine categories: congratulations,
gratitude, and recognitions; sign permits; sidewalk cafés, canopies, and awnings;
parking permits; condominium claims; sewer refunds; oaths of office. Turning it off
brought them back.

A glossary grouped the records into the categories an investigator works in: claims,
developments, exemptions, licenses, parking, permits, proceedings, public use,
recognition, services and budgets, tax, and traffic, each with example titles.

I built it with {{ person(id="germuska") }} and {{ person(id="wilson") }}, with
{{ person(id="billings") }} on the interface. Student fellows
{{ person(id="mcclendon") }}, {{ person(id="martinez") }}, and {{ person(id="din") }}
contributed to the project.

## Built with

Django and PostgreSQL, [DocumentCloud](https://www.documentcloud.org/), and the
Legistar web API.
