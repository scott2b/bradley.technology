+++
title = "Muster"
description = "Terminal session group management built on tmux: a Rust library and CLI that organizes terminals into named, color-coded groups with saved profiles and push-based state sync."
weight = 3
template = "page.html"
[taxonomies]
capabilities = ["Tools"]
settings = ["Independent"]

[extra]
image = "/images/projects/muster.webp"
print = "/images/projects/muster-print.webp"
tagline = "Terminal session groups, built on tmux"
place = "Rust, open source"
year = 2026
+++

Working across several projects at once means keeping a lot of terminals alive:
development servers, test runners, build watchers, agent sessions. They pile up
across windows and tabs with no structure.

[Muster](https://github.com/scott2b/muster) is a Rust library and CLI that organizes
them into named, color-coded groups. A group is a set of tabs, each with a working
directory and an optional startup command, saved as a profile and brought up or torn
down with one command.

```
muster profile save myproject --tab 'Shell:~/work/myproject' --color '#f97316'
muster up myproject        # create or reattach
muster status              # what's running
muster down myproject      # tear it down
```

{{ figure(src="/images/projects/muster-demo.webp", alt="A run: muster list shows four saved profiles in their colors and the running science session; muster up science attaches to it, and the status bar carries the group name, its color, and its four tabs", caption="A run, assembled from captures of a live session: the profiles and the running group, then muster up science and its first two tabs.") }}

## State lives in tmux

There is no application cache and no runtime state file. tmux owns all running state
(windows, working directories, the active window) and the config directory holds
only saved profiles and settings. The group metadata that would normally need a
state file (display name, color, profile reference) is stored as tmux user options
on the session, so it is created and destroyed with the session. When muster needs
to know what a group looks like, it asks tmux.

Changes arrive from tmux as they happen, over control mode, rather than being
polled for.

## Library first

The tmux bindings (command execution, output parsing, control mode event streaming)
are written in-house. Control mode streaming is the part that matters most here,
and the one existing Rust tmux crate calls itself experimental and does not provide
it.

The workspace is three crates: `muster`, the library; `muster-cli`, the binary; and
`muster-notify`, a small macOS helper that lives inside an app bundle so
Notification Center will talk to it. The CLI is a thin consumer of the library, and
the library has no dependency on any GUI framework, so the same core can back a
desktop application later.

{{ figure(src="/images/projects/muster-docsrs.webp", alt="The muster crate on docs.rs: Rust bindings for tmux command execution, control mode event streaming, profile management, session lifecycle, and runtime theming", caption="The library's API reference on docs.rs.") }}

## Availability

Published on crates.io as [`muster-cli`](https://crates.io/crates/muster-cli) and
[`muster`](https://crates.io/crates/muster), dual-licensed MIT/Apache-2.0, with
[documentation](https://scott2b.github.io/muster/) covering the user guide, CLI
reference, and architecture.

{{ figure(src="/images/projects/muster-crates.webp", alt="muster-cli on crates.io: the crate page with its description, versions, license, and install command", caption="muster-cli on crates.io.") }}
