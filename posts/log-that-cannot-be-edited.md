---
title: The log that cannot be edited afterwards
date: 2026-10-08
tag: AI assurance
description: When AI writes code no human will read, review stops being a control. What survives is evidence of behaviour. I posted that three weeks ago.
image: log-that-cannot-be-edited.jpg
alt: A stack of white printed pages with rows of timestamped log lines sits inside a clear plastic bag on a steel table, its red strip labelled SEALED with the number 0047283.
---
When AI writes code no human will read, review stops being a control. What survives is evidence of behaviour.

I posted that three weeks ago. Then a Hacker News thread from June landed in my inbox. Someone had already built the plumbing for exactly that, and it got four upvotes.

It is a plugin for an AI coding agent. It writes every prompt, tool call, result and refused action into a local database, then hashes them into a tree so editing or deleting any event afterwards is detectable. One command checks the trail and tells you whether it has been touched.

Not a changelog. A changelog is what someone says happened. This is what happened, with a check on whether anyone rewrote it afterwards.

I have not run it. I read the README and the thread, so treat these as reviewer's notes, not a verdict.

The first auditor to sit down with it would ask three things.

It fails open. If the database is unavailable, events are dropped silently and the agent carries on. An audit trail that goes quiet without saying so is a diary. The gap has to be recorded, or the agent has to stop.

It proves consistency, not time. The hashes catch an edit to the trail. They do not catch someone rebuilding the trail and the hashes together, and they say nothing about when any of it was written. Only anchoring those hashes somewhere outside the machine does that, and in this design that step is optional. The link an auditor needs most is the easiest one to skip.

It records the agent, not the release. The trail says what the agent did. It does not say that the code now running in production is what the trail describes. Every commit that reaches main should carry the hash of the trail that produced it. Without that, the two are just neighbours.

None of this is a knock on someone who built the thing and put it in front of strangers. It is the first time I have seen anyone build the "prove it" half of this rather than talk about it.

What has your team kept as proof of what its coding agents did, if anything?

Hey, let's be careful out there.
