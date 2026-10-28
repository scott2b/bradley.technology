+++
title = "Center for Applied Requirements Engineering"
description = "DePaul's requirements engineering research center. Built the testing framework for Poirot TraceMaker, a Siemens Corporate Research pilot in automated requirements trace retrieval."
weight = 10
template = "page.html"
[extra]
role = "Developer"
place = "DePaul University"
start = 2007
end = 2008
+++

The Center for Applied Requirements Engineering at DePaul worked on requirements
traceability: knowing which design documents, code, and tests correspond to which
requirement, on systems too large for anyone to keep that in their head.

The usual answer is a trace matrix maintained by hand, which goes out of date as soon
as the system changes. The center's research direction was to retrieve links instead
of maintaining them: treat a requirement as a query, run it against the project's
other artifacts, and rank what comes back.

The center was {{ person(id="cleland-huang", text="Jane Cleland-Huang's") }}. I worked
alongside {{ person(id="duan") }} and {{ person(id="antos") }}.

## Poirot TraceMaker

I worked on **Poirot TraceMaker**, a Java and Struts pilot for Siemens Corporate
Research that put dynamic trace retrieval behind a web application. I built the
testing framework the pilot was developed against.

A retrieval-based tracer returns a ranked list, so testing it means fixing a set of
reference traces, running the retrieval, and scoring the ranking against them. That
is how a change in ranking quality gets told apart from a change in the surrounding
code.
