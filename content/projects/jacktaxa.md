+++
title = "JackTaxa"
description = "A Java desktop application for jackknifed phylogenetic analysis, built for a Field Museum curator as my DePaul master's research."
weight = 8
template = "page.html"
[taxonomies]
capabilities = ["Applications & data", "Tools"]
settings = ["Academic"]

[extra]
tagline = "Rebuilding a curator's analysis tool"
place = "Field Museum of Natural History"
image = "/images/projects/jacktaxa.webp"
print = "/images/projects/jacktaxa-print.webp"
+++

{{ mark(src="/images/projects/jacktaxa-chrome.png", alt="The JackTaxa window: its title bar, menu, and the Simulation and Analysis tabs", strip=true) }}

Phylogenetics infers evolutionary trees from taxonomic data, and every tree it
produces is a hypothesis. Jackknifing is one way to test one: leave some of the taxa
out at random, rebuild the tree, and do it again many times over. The groupings that
hold up across the runs are the ones the evidence supports. The idea goes back to
Scott Lanyon's 1985 paper on [detecting internal inconsistencies in distance
data](https://doi.org/10.1093/sysbio/34.4.397), and Cicero and Johnson's [2001
vireo phylogeny](https://doi.org/10.1006/mpev.2001.0944) is the worked example
the project proposal pointed to. A single analysis produces something like ten
thousand trees, and someone has to sort through them.

{{ person(id="westneat") }}, then Associate Curator of Zoology at the Field Museum of
Natural History, had written JackTaxa in Pascal to do this for his coral reef fishes.
It was the only tool anyone knew of for automated jackknifing of phylogenetic data. He
wanted it in Java so it would run on his Mac and could be shared with other
biologists. I built that version from scratch, with Dr. Westneat as the client.

## What it does

The window has two tabs, in the order the work goes, and a settings dialog for the
PAUP script that wraps each run: its header, its footer, and how taxa are named.

**Simulation** loads the taxa from a NEXUS file, sorts them into included, excluded,
and jackknifed, and takes the number of iterations. Pressing the button writes a
command file with every run in it. JackTaxa does not build trees itself: that file
goes to PAUP, which produces a tree file.

{{ figure(src="/images/projects/jacktaxa-simulation.png", alt="The Simulation view: a hundred fish taxa sorted into included, jackknifed, and unincluded, set for a hundred iterations") }}

**Analysis** loads the tree files that come back. Pick a tree and a clade in it, and
Find Clade splits every tree into those that contain the clade and those that do not.
Find Resolved Clade also requires the same topology inside it. Calculate Distances
gives the Robinson-Foulds distance from the selected tree to each of the others, and
any of the lists can be written back out as a NEXUS file for the next step.

{{ figure(src="/images/projects/jacktaxa-analysis.png", alt="The Analysis view: 331 trees loaded, one selected, its clades listed as sets of taxa IDs") }}

## Two courses of research

JackTaxa was two courses of graduate research for my [master's at
DePaul](/credentials/depaul-mscs/), from September 2006 to November 2008. The first,
a research practicum in computational biology, produced the first working version
and a design paper. The second, the computer science research option, carried it
toward a finished, distributable application. {{ person(id="angulo") }} and
{{ person(id="phillips") }} advised the research; Dr. Westneat set the requirements.

## Built with

Java Swing, on Java 1.5 and then 1.6, built in NetBeans with Ant and kept in
Subversion. The phylogenetics libraries were PAL, BioJava, and PhyloNet, with SwingX
and Spring Rich Client for the interface. The engineering documents, a proposal, a
requirements specification, a feature set, use cases, CRC cards, and a class diagram,
follow the ReadySet templates.
