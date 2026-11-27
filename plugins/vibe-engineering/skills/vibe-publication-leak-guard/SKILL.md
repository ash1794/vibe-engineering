---
name: vibe-publication-leak-guard
description: Keeps private and unapproved material out of a public build. Scans the built output (HTML, serialized component payloads, client JS and CSS chunks, static data routes, public files) against a private tier that always applies and a draft tier that applies in production. Gates work-in-progress so it shows in preview and is absent from production, and keeps sign-off in a ledger only the human writes. Use when a site or app publishes content that agents drafted or that came from private sources.
user-invocable: true
---

# vibe-publication-leak-guard

A source-diff scan catches a secret in a commit. It doesn't catch a private field that a server component serializes into the client payload, a draft line that ships in a static JSON route, or a file in `public/` that never went through the build. Agents that work from private notes, or draft text in someone's voice, need a guard on what actually ships, plus a way to keep drafts visible for review without ever publishing them.

## When to Use This Skill

- Content comes from private sources (notes, journals, internal documents, exports)
- Agents draft copy in the owner's voice, or quote material that needs the owner's sign-off
- Setting up a preview build that shows drafts and a production build that must not
- Before the first production deploy of a content site

## When NOT to Use This Skill

- Secret scanning of staged code (use `vibe-pre-commit-audit`)
- A site with no private inputs and no draft content
- Access control for authenticated content (that's an authorization problem, not a build scan)

## Steps

1. **Keep raw private context out of git.** Raw notes and exports live in a gitignored directory; only distilled, public-safe facts enter the repo. A force-push doesn't purge old commits from a hosted PR, so if something private was ever pushed, plan a squash-merge or a history purge.

2. **Gate drafts with a flag, not a comment.** Give every item that needs sign-off a stable id and a `needsOk`-style flag in the content data. Preview builds render it with a visible WIP marker; production builds drop it. A missing input becomes a pending id, not a blocker. A code comment saying "approved" is not approval, and the guard should fail on it.

3. **The human owns the approval ledger.** Approvals live in a sign-off sheet or file the human edits, with one record per item id. Agents read it before copy work and never write approval states, even when the human says yes in chat. In that case, tell them which item id to mark, and keep the content gated until they do.

4. **Build the guard over emitted output.** After the production build, scan every artifact the server or CDN can serve:
   - rendered HTML and serialized component payloads, including segment files
   - feeds, sitemaps, robots files, and static data routes
   - first-party JS and CSS chunks
   - everything in the public or static directory, which ships verbatim

5. **Use two tiers.**
   - **Private (always, including preview):** private source paths, denylist terms, hashes of sentences the owner rejected.
   - **Draft (production only):** WIP markers, prompt leftovers, placeholder slots, and every string from items still flagged `needsOk`.

6. **Hold the denylist outside the repo.** Read it from a CI secret plus an untracked local file. Warn locally when it's missing, and fail in CI on the release branch. Suggest categories to fill it with (names, internal program terms, private places, hostnames), because "what goes in the denylist?" is hard to answer cold.

7. **Test the guard.** A self-test plants a known leak in each artifact type, plus a known false positive. The guard must catch the first and pass the second.

8. **Run it in CI on every push**, after the build and before any deploy step. A leak fails the job. Never allowlist a finding to get to green without writing down why.

## Output Format

### Leak Guard Report
**Build**: [sha] · **Mode**: production | preview · **Denylist**: present (N terms) | missing

| Tier | Artifact | Match | Source item | Action |
|------|----------|-------|-------------|--------|
| draft | about.rsc | WIP marker | q.about.intro | keep gated; awaiting sign-off |
| private | chunks/123.js | denylist term #4 | content/people.ts | remove field from client props |

**Pending sign-off**: [item ids the human needs to mark]
**Result**: PASS | FAIL (N private, M draft)
