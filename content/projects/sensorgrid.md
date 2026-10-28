+++
title = "SensorGrid"
description = "A low-cost, solar-powered, wireless network of air quality sensors built at Northwestern's Knight Lab: the hardware, firmware, and radio networking, and the API and dashboard on top."
weight = 6
template = "page.html"
[taxonomies]
capabilities = ["Embedded & hardware", "Systems"]
settings = ["Academic"]

[extra]
image = "/images/projects/sensorgrid.webp"
print = "/images/projects/sensorgrid-print.webp"
tagline = "Democratizing environmental data"
place = "Knight Lab"
year = "2017–2018"
+++

{{ mark(src="/images/projects/sensorgrid-logo.png", alt="SensorGrid") }}

SensorGrid is an open-source network of air quality sensors built at Northwestern
University's [Knight Lab](/experience/knightlab/), for communities, journalists,
and citizen scientists who want to measure the air where they live.

Official monitoring is sparse. The EPA's stations sit far apart, and readings for
everywhere in between are estimated, while pollutant concentrations vary block by
block with traffic, construction, factories, and power plants. Many cities have no
monitoring at all, because of the cost of the equipment and its upkeep. SensorGrid
measures at the resolution pollution varies at, from a single street to a whole
city.

- **Low cost** — about $200 per device
- **Solar powered** — no mains connection at the site
- **Wireless** — readings transmitted over radio
- **Open source** — the technology and architecture are free to use
- **Dense coverage** — the networking is designed for many nodes close together

{{ figure(src="/images/projects/sensorgrid-node-prototype.jpg", alt="A SensorGrid node prototype", caption="A node prototype.") }}

A node is a stack of Adafruit Feather boards with a LoRa radio, a particulate
sensor for PM2.5 and PM10, a solar panel, and a weather shield, and the nodes send
their readings to a collector over the LoRa network. A web API and dashboard take in
the readings and chart them.

I was the senior engineer on it, with {{ person(id="wise") }} as faculty lead.
{{ person(id="calagna") }} managed its research and development, and
{{ person(id="friedman") }} worked on it as a Knight Lab fellow. Students in the
Knight Lab Studio contributed to the project: Holly Kane, {{ person(id="cabales") }},
{{ person(id="wallach") }}, and {{ person(id="inderhees") }} built the first dust
sensor nodes in
[spring 2017](https://studio.knightlab.com/projects/environmental-reporting-with-sensors/),
and {{ person(id="cahana") }}, Alex Cohen, {{ person(id="martinez") }},
{{ person(id="ywang") }}, and {{ person(id="whitely") }} built out the API and
dashboard in
[winter 2018](https://studio.knightlab.com/projects/sensorgrid-api-dashboard/).
Kelly and Jordan presented the project at Northwestern's
[TEACHx](https://teachx2018.sched.com/event/Edr5/sensorgrid-a-tool-for-learning-teaching-exploration)
conference in May 2018.

{{ figure(src="/images/projects/sensorgrid-node.jpg", alt="A SensorGrid node on the bench: the stacked Feather boards with their OLED, the particulate sensor, and the dust sensor adapter board wired between them", caption="A node on the bench.") }}

The project site is [sensorgrid.knightlab.com](https://sensorgrid.knightlab.com/).

*Prototype photograph by {{ person(id="calagna") }}, Northwestern University Knight Lab.*
