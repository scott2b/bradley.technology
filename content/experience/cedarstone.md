+++
title = "Cedarstone Partners"
description = "Technology lead at an accounting firm serving nonprofits — extending QuickBooks through its SDK to generate donor receipting and nonprofit-specific reporting."
weight = 11
template = "page.html"
[extra]
role = "Technology lead"
place = "Wheaton, Illinois"
start = 2004
end = 2007
+++

Cedarstone Partners is an accounting and business-services firm that provides
outsourced financial and administrative services to nonprofits. I was its technology
lead, working with the business-services side on the systems behind its client work.

## Donor receipting

The main project was an overhaul of donor receipting and reporting.

Cedarstone kept the books for a portfolio of mostly small and midsized nonprofit and
ministry organizations, Global Family Rescue, RCE International, and Josiah Venture
among them, with all client activity entered and maintained in QuickBooks. Nonprofit
clients need reports QuickBooks does not produce, donor receipts in particular, and
the data to produce them was already in QuickBooks. A separate system with its own
data entry would have meant duplicate entry and two sources of truth, so the aim was
to build on the QuickBooks data directly.

I started with a
[feasibility study](/artifacts/quickbooks-sdk-feasibility-study.pdf) for the
partners in June 2004, showing sales receipts being created inside QuickBooks from
Access VBA through the QuickBooks SDK, with the code that did it. The application
that followed was a database-driven reporting system integrated with QuickBooks
through its SDK. QuickBooks stayed the accounting system and the staff's workflow;
the new software read what was there and generated the receipts and client reports.

The work needed two things understood together: the structure the QuickBooks SDK
exposes, and the particular way Cedarstone represented fund accounting and donor
activity inside a product built for ordinary businesses. Translating between those
into the reports a nonprofit's board and donors need was most of the job.
