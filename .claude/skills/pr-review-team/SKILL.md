---
name: pr-review-team
description: Runs a simulated internal review team (product owner, scrum leader, two junior devs) over a draft PR before handing it to a real human for external review. Use when a feature branch is ready to be PR'd and the user wants an internal quality gate first — not a substitute for human review, a filter before it.
---

# PR Review Team Workflow

This skill drives the fork/draft-PR/simulated-team-review workflow for this
repo. It exists so that "PR this and get it reviewed" means something
specific and repeatable, not an ad-hoc one-off each time.

## When to use this

The user asks to PR a completed piece of work and have it internally
reviewed before a human looks at it — phrasing like "PR the MVP and review
it," "run it through the team," "get sign-off before external review."

## The workflow

1. **Confirm the branch is pushed.** `git status`, `git log`, confirm the
   feature branch is up to date with origin.

2. **Open the PR as a draft.** Prefer `gh pr create --draft` if the `gh` CLI
   and credentials are available in this environment. If not, say so plainly
   — do not silently skip PR creation or fabricate a PR link. A draft PR
   signals "not yet ready for a human" while the internal review runs.

3. **Spawn the review team in parallel**, in a single message with multiple
   `Agent` tool calls so they run concurrently, each in the foreground
   (`run_in_background: false`) since their output needs to be synthesized
   before the next step:
   - `product-owner` — spec/scope match against the relevant design doc.
   - `scrum-leader` — build/run/testability/process readiness.
   - `junior-dev` (instance 1) — line-level review, focus area A (e.g. core
     game logic / combat / inventory).
   - `junior-dev` (instance 2) — line-level review, focus area B (e.g. file
     I/O / data loading / save-load).

   Give each agent the PR diff or changed-file list and enough context to
   act (what the change is for, where the design doc lives, what to run to
   verify it). Do not just say "review this" — brief them the way the
   Agent-tool guidance describes: what changed, what to check, what "done"
   looks like.

4. **Synthesize.** Collect all four verdicts. If any reviewer says REQUEST
   CHANGES / NOT READY, do not treat the PR as internally approved — report
   the blockers to the user and stop; fixing them is a separate step the
   user should confirm, not something to charge ahead on unprompted.

5. **Post the summary**, if `gh` is available, as a single PR comment (not
   four separate ones) combining all four verdicts with clear attribution
   per section, via `gh pr comment`.

6. **Hold for external review.** This is the stopping point:
   - If all four reviewers approved, mark the PR ready for review (undraft
     it, e.g. `gh pr ready`) so a human knows it's been through the internal
     gate.
   - **Never** run `gh pr review --approve` on this PR yourself. Self-approval
     on your own PR is both meaningless (most platforms block it for the
     PR's own author) and not the point — actual approval is a human
     reviewer's call, full stop.
   - **Never** merge. That is exclusively a human decision on this repo's
     workflow.
   - Report back to the user with the PR link, the four verdicts, and
     nothing further in motion — the ball is in the human reviewer's court.

## What this skill is not

It is not a way to get a PR auto-approved and merged by proxy through
simulated personas. The simulated team's job is to catch obvious problems
*before* a human's time gets spent — a quality gate, not a rubber stamp, and
never a replacement for the actual external reviewer.
