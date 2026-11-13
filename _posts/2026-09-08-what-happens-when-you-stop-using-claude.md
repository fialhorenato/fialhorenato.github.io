---
title: "What Happens When You Stop Using Claude as a Coding Assistant—and Start Treating It Like an Engineer?"
description: "A long-running engineering harness changed how I use Claude: small scoped tasks, durable project memory, model routing, and validation built into the workflow."
date: 2026-09-08
layout: single
tags:
  - AI
  - Software engineering
  - Developer tools
  - AI agents
source_url: https://www.linkedin.com/pulse/what-happens-when-you-stop-using-claude-coding-assistant-fialho-os7ce/
---

While building a product, I tried a different way of working with Claude. Instead of keeping it in a chat loop, I built a small autonomous engineering harness around it.

The goal wasn’t to generate more code. It was to make the agent work reliably for long periods of time.

## Treat context as a filesystem

The project’s `.ai/` directory became its persistent memory. It held product context, architectural decisions, a task graph, current state, design artifacts, checkpoints, and execution history.

A new Claude session didn’t need to remember everything. It read only the context relevant to its task.

## Give the agent small, defined tasks

I wanted to model the work the way a software team does. A product manager wouldn’t ask a team to “build the entire product.” The work would be broken into features, improvements, bugs, and smaller tasks, each with the context needed to complete it.

I applied the same idea to Claude. The project was divided into explicit tasks with dependencies, acceptance criteria, scope, constraints, and budgets. Instead of “build the product,” Claude received a specific task and the information needed to complete it.

Smaller tasks kept context focused and made the work easier to validate.

## Separate planning from execution

I didn’t delegate every step to Claude. I used ChatGPT to help generate and structure the task breakdown. That way, Claude didn’t need to spend tokens discovering the whole roadmap before implementing a task.

One model helped define the work; another carried it out. The separation made planning and execution more deliberate.

I separated design from implementation too. Claude Design helped explore the product and its design, and Claude handled implementation. The process looked more like:

**Product thinking → task breakdown → design → implementation → validation**

Each stage produced artifacts that could inform the next one, rather than trying to solve everything in a single conversation.

## Make token efficiency an engineering concern

The most useful principle was simple: don’t read what you don’t need.

The harness didn’t load the entire project into context, reread unchanged documentation, or carry a whole conversation into every task. Each task started with a deliberately small context window. Because the work was already decomposed, Claude could spend more of its available context on execution.

## Route work to the right model

I didn’t want the most expensive model doing every job. Mechanical work could go to a smaller, faster model; routine implementation to a general-purpose model; and difficult architectural or debugging work to a stronger reasoning model.

Each task carried its own model, reasoning effort, and turn budget.

## Persist state and validate the result

The agent wrote progress to .ai/STATE.json. If a session reached a turn or usage limit, or failed temporarily, the runner could resume the task instead of starting from zero.

A task also wasn’t complete just because Claude said it was. It had to meet its acceptance criteria, pass the relevant checks, stay within scope, and stop when it needed a human decision.

## Let the workflow run

The harness/ directory became a small control plane:

**Task selection → context assembly → model routing → execution → validation → state persistence → retry or checkpoint → next task**

Claude could keep working without me sitting in front of the terminal.

That was the most interesting part of the experiment. The hard problem isn’t getting an LLM to write code; we already know it can. The interesting work is engineering the system around the models: context management, task decomposition, model routing, budgets, design artifacts, validation, retries, and human checkpoints.

At that point, you’re no longer just asking an LLM to help you code. You’re designing an autonomous software delivery system around LLMs. I think that’s where much of the interesting engineering work on AI agents will happen.

I also put together a generic example of the architecture, with nothing from the actual product—just the pattern. Read the [original LinkedIn article](https://www.linkedin.com/pulse/what-happens-when-you-stop-using-claude-coding-assistant-fialho-os7ce/) for the original discussion and sharing context.
