---
date: 2026-11-12
title: "How I Built a Multi-Agent AI Software Team with Claude Code"
description: "A practical multi-agent AI software development workflow: separate design, coding, review, and naive-user testing, with tasks and checkpoints that preserve project context."
tags:
  - AI
  - AI agents
  - Developer tools
  - Software engineering
layout: single
---

I’m building a café management product with AI agents involved in design, implementation, review, and usability testing. The useful change was not asking one model to write more code. It was giving different sessions clear jobs and building a workflow that carries decisions and evidence from one job to the next.

This is how the multi-agent software development setup works in my project. It uses Claude Code sessions, a task orchestrator, and the repository as persistent project memory. The exact tools can change; the underlying ideas are to bound each task, separate responsibilities, and make the result reviewable.

I wrote earlier about [using a long-running engineering harness around an AI coding assistant](/blog/what-happens-when-you-stop-using-claude). This article focuses on the team structure around the work: design, code, independent review, and testing as a first-time user.

## The agents have roles, not job titles

I don’t keep a room full of agents chatting to one another. The harness starts fresh sessions with narrow responsibilities. Each one gets the context and tools needed for its part of the work, then leaves durable notes for whatever comes next.

The main roles are:

- **Product owner and task author:** I set direction, clarify business rules, approve consequential design decisions, and keep tasks tied to the product roadmap.
- **Designer:** explores user flows and screen states, then records a design that implementation can follow.
- **Implementer:** changes the code for one scoped task and verifies it against acceptance criteria.
- **Reviewer:** inspects the completed work from a fresh context and looks for errors or missed requirements.
- **Naive usability tester:** opens the running application and tries to complete ordinary tasks without reading the product documentation or implementation.
- **Orchestrator:** chooses eligible work, starts sessions, preserves state, and hands results to the next stage.

These roles are prompts and responsibilities attached to separate sessions, not claims that the models have human job experience. The value comes from making the assignment specific enough that each session can succeed or fail on evidence.

## Give work a small, testable contract

The unit of work is a task, not an open-ended request like “build the inventory system.” A task describes a goal, scope, constraints, dependencies, acceptance criteria, and verification steps. It can also point to relevant product, architecture, or design documents without copying the entire repository into every prompt.

That changes how I ask for work. For example, a task can say which user problem a screen should solve, which design artifact is approved, which business rules cannot change, and which tests must pass. If an important product decision is missing, the agent should surface the question instead of inventing a rule.

The task graph also gives the orchestrator a way to order dependent work. A screen implementation can wait for its design; a usability round can wait until the screen exists. Small tasks are easier to review, retry, or hand to another session when a run is interrupted.

## Treat the repository as the team’s memory

Each implementation task gets a fresh Claude Code session. That keeps the context focused and makes it easier to tell what the session was asked to do. A new session does not need to reconstruct the whole project from a long chat transcript.

The durable context lives in the repository: product and architecture notes, decisions, the roadmap, task specifications, current state, and checkpoints. Before starting, a session reads the compact context for its task and opens deeper documents only when needed. At the end, it records what changed, what was verified, and the next action.

This makes session interruption manageable. If a process reaches a usage limit or stops unexpectedly, the orchestrator can resume from the task and checkpoint instead of asking a new session to infer what happened. Git commits provide additional recovery points.

## Separate design from implementation

For work that changes the user experience, I use a design stage before implementation. The designer considers the flow, screen hierarchy, responsive behavior, empty and error states, keyboard interaction, and the copy people will see. The approved design becomes an artifact that the implementation task can reference.

In my setup, design work and code work can run in separate lanes. That does not mean every agent edits the same files at once: each lane has clear ownership, and the task dependency controls when implementation is ready to proceed.

After implementation, a separate design-conformance reviewer captures the running application and compares it with the approved design at the relevant viewport sizes. The reviewer records gaps; a task is not considered complete just because the implementing session says it looks right.

This is useful because design quality has two separate questions: “Was the interaction thought through?” and “Did the code actually implement the approved interaction?” One session is not asked to be the only judge of its own work.

## Make review independent

The code review also runs in a fresh session. The reviewer checks the implementation against the task, reads the diff, and looks for correctness, security, regressions, and missing verification. If the review finds a problem, a new implementation session receives the concrete findings and fixes them.

The separation matters. A review prompt that merely asks an agent to praise or summarize the work is not a useful gate. The reviewer needs permission to disagree, access to the relevant evidence, and a clear way to report what blocks completion.

For user-facing work, code review and design review cover different risks. Automated tests can catch behavior regressions; a visual comparison can catch a missing control or broken layout; neither replaces the other.

## Use a naive-user agent to find friction

One of the more useful roles is a session that behaves like a first-time user. I call this the “naive user” round. It gets a goal—such as opening a table, adding an item, or finding a report—and tries to complete it in the running application without studying the docs or source code first.

The personas are concrete: a cashier on a busy shift, a waiter using a phone, or an owner working from a laptop. The tester is told to report where it hesitates, misreads a label, gets stuck, needs too many steps, or encounters a confusing empty or error state. It does not fix the code while testing. Findings become follow-up tasks for the designer or implementer.

This is a useful way to discover interface friction, but it is still a simulation. An AI session is not a substitute for watching real café staff use the product. I treat its findings as hypotheses and test them with people when I can.

## Let the orchestrator handle the repeatable work

The supervisor handles the routine state transitions: selecting a task whose dependencies are complete, preparing its context, starting a fresh session, tracking the result, retrying or pausing after interruptions, and scheduling review. For screen changes, it can queue a usability round after implementation.

The workflow is deliberately not a single giant concurrent swarm. In my current setup, the design and code lanes can work in parallel on eligible tasks, but each lane still handles bounded tasks and reviews happen at defined handoffs. The goal is coordinated responsibility, not maximizing the number of agents running at once.

Model choice and turn budgets can vary by task type. Routine implementation does not need the same reasoning budget as a security review or complex design task. A task-specific budget also makes the cost and expected scope more explicit.

## Keep autonomy inside a safe boundary

An autonomous coding harness can run commands and make local changes without an approval prompt for every routine action. That is convenient, but it makes the execution environment important. I run this kind of work in a controlled development setup, keep production credentials out of the agent environment, and do not let the harness push or deploy automatically.

When an agent can call application tools, the same boundary applies to those actions too. I cover that in a separate guide to [securing Spring AI tool calling](/blog/secure-spring-ai-tool-calling).

Tests, permissions, review gates, and deployment boundaries are part of the system around the agents. They are not optional cleanup after the agent can already change code. A task that affects a sensitive domain should carry the relevant security and audit requirements from the beginning.

## What changed in my engineering work

The main shift is from repeatedly prompting a model to designing a work system around it. I spend more time making tasks clear, preserving decisions, reviewing evidence, and deciding what should happen next. The agents can take on bounded implementation and evaluation work, while I remain responsible for product direction and decisions that need human judgment.

The setup is not magic, and adding more roles does not automatically improve results. Its benefits come from a few practical choices:

- Keep one task small enough to complete and review.
- Store durable context in versioned project files.
- Separate implementation from independent review.
- Treat design conformance and usability as explicit work.
- Make failures and handoffs visible to the next session.
- Keep autonomy away from production credentials and deployment.

The interesting question is not “How many agents can I run?” It is “Can each session make a useful contribution, and can the next person—or agent—verify what it did?” That is what turns a collection of coding sessions into a multi-agent engineering workflow.
