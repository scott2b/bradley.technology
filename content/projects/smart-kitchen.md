+++
title = "Smart Kitchen Central System"
description = "An object-oriented design for a kitchen controller over grocery, recipe, and appliance subsystems, from one use case down to a class model."
weight = 24
template = "page.html"
[taxonomies]
capabilities = ["Systems"]
settings = ["Academic"]

[extra]
image = "/images/projects/smart-kitchen.webp"
print = "/images/projects/smart-kitchen-print.webp"
tagline = "Object-oriented modeling"
place = "DePaul SE 430"
year = "Winter 2005"
+++

The Smart Kitchen Central System was a design for a controller over a kitchen's
groceries, recipes, and appliances. Groceries are scanned in and out, so the
inventory and the shopping list keep themselves. Recipes are suggested from what
is in stock. Appliances report their state and take instructions remotely. It was
a design document, not a build.

It was a team project for DePaul's object-oriented modeling course, taught by
{{ person(id="streeter") }}, with Haunani Soares-Pollack, Larisa Bednyak-Kaykov, and
Chang Kim. The team's report is [here](/artifacts/smart-kitchen-report.pdf) (PDF,
29 pages). My parts were the domain model, the design class diagram, and the
use-case realization.

{{ figure(src="/images/projects/smart-kitchen-domain-model.webp", alt="The domain model: grocery, recipe, and appliance management subsystems around the central system, with the scanner, grocery items, shopping list, recipes, appliances, and the user", caption="Domain model.") }}

The design took one use case, *find a recipe for a desired meal*, through two
passes. A GRASP analysis (General Responsibility Assignment Software Patterns)
walked the event flow step by step, assigning each responsibility to an
abstraction: factories for the objects, a dispatcher per subsystem, an information
expert for data, with the database deferred. A second pass refactored those
against design patterns: a mediator per use case, factory interfaces for list and
text data, and a data-source façade with pull filters.

{{ figure(src="/images/projects/smart-kitchen-design-classes.webp", alt="The design class diagram: UI widgets and listener interfaces above a use-case mediator, the dispatchers, list and text factories, and the data-source interface, filters, and façade", caption="Design class diagram.") }}
