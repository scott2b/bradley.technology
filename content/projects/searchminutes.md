+++
title = "SearchMinutes"
description = "Transcribing and indexing local government meetings so the public record is searchable. A Michigan Radio project, later an Associated Press one; I rebuilt its transcription pipeline on Whisper."
weight = 4
template = "page.html"
[taxonomies]
capabilities = ["Language & AI", "Systems"]
settings = ["Academic"]

[extra]
tagline = "Making public meetings searchable"
image = "/images/projects/searchminutes.webp"
print = "/images/projects/searchminutes-print.webp"
+++

SearchMinutes made the public record of civic meetings searchable by transcribing the
meetings themselves. Local government business is largely conducted in recorded
public meetings, and the recordings are hours of video with no transcript or index.

The project was shut down in 2026 and is no longer active.

{{ figure(src='/images/projects/searchminutes-home.png', alt='The SearchMinutes home page: "An easier way to find the information you need on local government meetings"') }}

## My part

SearchMinutes was a Michigan Radio (NPR) project. I came in as a consultant late in
its life, as it was being prepared for transfer to the Associated Press. The main job
was rebuilding the transcription pipeline: the existing design sent recordings to a
transcription service, and I replaced that with OpenAI's Whisper running inside the
pipeline. Alongside that were the application changes needed for the handover to AP.

## How it works

The Minutes pipeline ran on Google Cloud Platform, driven by a suite of
configurations for monitoring civic media feeds. Newly discovered media were injected
into a pipeline of queued processing stages that registered the media with the
system, then downloaded and transcribed it. Transcripts were written to a search
index used by the SearchMinutes website.

The registry and queues were handled by Redis. The system was written in Python, with
Whisper providing the transcripts.
