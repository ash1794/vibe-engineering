---
name: vibe-slop-filter
description: Strips AI-generation "smell" from prose before it ships (READMEs, docs, release notes, PR descriptions, posts, emails). Counts measurable tells first (keyword saturation, tricolons and anaphora, the "not X, it's Y" reflex, fragment-for-emphasis, bolded thesis lines, listicle-ization, signpost phrases, filler vocabulary, em-dashes, engineered-quotable closers), then applies a "doing work or reflex?" test to each instance so genuine voice survives. Use when asked to de-slop text or make it sound human, when text reads as machine-written, and as the final pass on prose the agent drafted.
user-invocable: true
---

# vibe-slop-filter

A pass for removing the texture that makes prose read as machine-assembled rather than written by a specific person. It is a filter, not a generator: it finds and flags the tells and informs the rewrite. The rewrite is a separate act.

It matters most for writing about AI, where the slop reads as self-refuting, and for AI-literate readers, who reject prose on smell before they reach the argument. It applies to any prose read by someone who can choose to stop reading.

Every tell below is also legitimate writing in moderation. One deliberate tricolon, one earned fragment, one antithesis at the pivot of the argument: that is craft. The tell is the reflexive overuse, the same rhythm firing because it is the model's default rather than because the sentence needed it. So the filter has two jobs, and the second matters as much as the first:
1. Catch the device used as a reflex.
2. Don't sand genuine voice into choppy, variation-for-its-own-sake prose. Over-applying the filter is its own failure.

For every flag the test is the same: **is this doing work, or is it reflex?** Keep what does work. Cut the rest.

## When to Use This Skill

- Asked to de-slop text, remove the AI smell, or make it sound human
- Asked whether something reads as AI-generated
- Final pass on prose the agent drafted that a person will read: README sections, docs, release notes, PR descriptions, announcements, emails
- Text you've been given pattern-matches generic LLM writing

## When NOT to Use This Skill

- Code, config, and structured data
- Reference material that is meant to be scanned (API tables, command lists, changelogs written as bullet lists)
- Checking a technical document's structure and accuracy (use `vibe-doc-quality-gate`)
- Critiquing whether the argument is right (use `vibe-devil-advocate-review`); this skill fixes how prose reads, not what it claims
- Text the user wrote in their own voice and didn't ask you to change

## Steps

### 1. Count before you read

A read-through normalizes tics: by the third "It is not X, it is Y" you have stopped hearing it. Counts don't normalize. Run them first so you know where to look. Replace the filename and the keyword:

```bash
f="draft.md"

# Keyword saturation: run once per thesis word you suspect is overused.
# A content keyword appearing more than once per ~300-400 words is worth examining.
echo "words:"; wc -w < "$f"
echo "keyword:"; grep -oiE "theater" "$f" | wc -l

# Em-dashes (a default LLM punctuation pattern; usually want few or none).
grep -o "—" "$f" | wc -l

# Bolded segments (free-standing thesis lines and bolded list-leads).
grep -oE "\*\*[^*]+\*\*" "$f" | wc -l

# Numbered-list items (the listicle reflex).
grep -cE "^[0-9]+\. " "$f"

# "not X, it's Y" antithesis density.
grep -oiE "is not |are not |not just |not only |it'?s not |rather than" "$f" | wc -l

# Filler intensifiers and house-LLM vocabulary.
grep -noiE "\b(genuinely|truly|simply|actually|really|incredibly|seamless|robust|crucial|pivotal|delve|leverage|myriad|plethora|tapestry|landscape|realm|testament)\b" "$f"

# Anaphora: runs of 3+ consecutive sentences opening with the same word.
grep -oE "(^|\. )[A-Z][a-z]+" "$f" | sed -E 's/^\. //' | uniq -c | awk '$1>=3'
```

The counts point at suspects. The judgment is still yours.

### 2. Fix the worst offender first

Read once for the biggest problem the counts named, usually keyword saturation or stacked tricolons. Fixing it often removes others with it.

### 3. Walk the tells

Apply "work or reflex?" to each instance rather than deleting by category.

**Lexical**
- **Keyword saturation.** The thesis word repeated far past what a person would tolerate (one real essay used "theater" 23 times in 2,900 words). A writer reaches for paraphrase and concrete description; a model hammers the one word. *Fix:* name the concept two or three times and describe it concretely the rest of the time.
- **Filler intensifiers and house vocabulary.** "genuinely," "truly," "simply," "really," "delve," "leverage," "robust," "seamless," "crucial," "navigate the landscape," "a testament to," "tapestry." *Fix:* cut the adverb, or replace the cliché with the specific thing it gestures at.

**Rhythm**
- **Full-sentence tricolon and anaphora.** Three or more consecutive sentences in the same shape for cadence ("The dashboard... The velocity chart... The readiness report..."). The most recognizable machine-essay rhythm. *Fix:* vary openers and structures, fold the three into one sentence, or cut to two.
- **The "it is not X, it is Y" reflex.** Antithesis used as a beat rather than to mark a real distinction. *Fix:* keep only the ones at a genuine pivot; state the rest plainly.
- **Fragment-for-emphasis on a loop.** Beat after beat ending on a clipped fragment ("The opposite." "Zero progress."). *Fix:* a couple at most, each earned by what precedes it.
- **Rule-of-three noun lists.** "faster, cheaper, and better" by default. *Fix:* use two, or four, or an uneven list.
- **Uniform aphorism cadence.** Every paragraph landing on a punchy one-liner until the emphasis stops registering. *Fix:* let most paragraphs end plainly and keep the sharp line for where it's earned.

**Structure and format**
- **Bolded thesis sentences and bolded list-leads.** Free-standing bold declaratives; the carousel-post smell. *Fix:* cut the bold and let the sentence carry itself.
- **Listicle-ization.** An argument turned into a numbered list of named principles. Arguments live in prose; checklists are for procedures. *Fix:* dissolve into prose and let each point come out of the concrete case that earns it.
- **Mechanical symmetry.** Every section the same length, "First / Second / Finally" scaffolding showing. *Fix:* let section weight follow the content.

**Stance**
- **Signpost phrases.** "Here's the thing," "It's worth noting that," "Make no mistake," "At the end of the day." Announcing that something important is coming instead of saying it. *Fix:* delete the signpost, keep the content.
- **Engineered-quotable closers.** Lines built to be screenshotted rather than to be true. *Fix:* keep the claim, drop the polish.
- **Hedge-then-assert and false balance.** "While it's true that X, ultimately Y." *Fix:* make the claim.
- **Vague universal openers.** "In today's fast-paced world," "As AI continues to evolve." *Fix:* open on something only this piece could open on.

### 4. Re-run the counts

Confirm the tells dropped, and check you didn't over-correct.

### 5. Read once more for rhythm

The prose should sound like one person who was in the work, not an assembly of devices. If it has become choppy, evenly clipped, or self-consciously varied, the filter was over-applied; restore the rhythm.

## What Is NOT Slop

Don't flag these. Sanding them out is how the filter ruins good prose:
- A single tricolon or fragment used deliberately for a real effect.
- One antithesis at the pivot of the argument.
- A list that is genuinely list-shaped (steps, options, a comparison) when the reader needs to scan it.
- Specifics, names, and numbers. They are the opposite of slop and the best defense against it. When a piece over-explains, the fix is usually more specificity, not less.
- A long sentence next to a short one. Variation is the goal, not a target length.

## Output Format

### Slop Filter: [document]

| Tell | Before | After | Note |
|------|--------|-------|------|
| Keyword "[word]" | 23 | 3 | |
| Em-dashes | 14 | 2 | |
| Antithesis | 9 | 2 | kept the two at real pivots |
| ... | | | |

**Rewrites**: [the changed passages, or the revised text if asked to apply]
**Kept on purpose**: [devices left in because they do work, one line each]

## Example

Before (keyword "theater" 23 times; a stacked tricolon):
> This is not a bug. This is theater. ... A pass must be distinguishable from a pass-by-accident. A defer must be distinguishable from a spin loop. A green light must be distinguishable from "nobody checked."

After (keyword down to 2 across the piece; tricolon folded into one concrete sentence):
> This is not a failure you debug. The code did exactly what it was told. What it was told to do was produce a green light with no way to tell working apart from merely running.

The argument is unchanged. The drumbeat and the mechanical parallel are gone, and the concrete sentence does the work the rhythm was faking.
