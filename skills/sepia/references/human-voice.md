# Human Voice Profile

The goal is not to manufacture “human-sounding” noise. The goal is to make the author clearer without replacing the author.

## Governing sentence

> Do not make the author sound like a better writer. Make the author easier to understand without making them sound like someone else.

## 1. Evidence hierarchy

Build the profile only from available evidence, in this order:

1. the user's current explicit instructions;
2. an explicit profile supplied or specifically authorized under `voice-profile-config.md`;
3. multiple samples from the same author;
4. the target text;
5. recent texts from the same venue or organization;
6. language and locale conventions;
7. generic editorial heuristics.

Never invent a personal history, mood, dialect, age, level of education, sense of humor, or confidence level from demographic guesses.

## 2. Profile fields

Record only fields supported by evidence:

- **person and reference:** first/second/third person, subject omission, preferred self-reference;
- **relationship and register:** casual, collegial, customer-facing, formal, deferential, technical;
- **rhythm:** typical sentence length, paragraph length, fragments, interruptions, parentheticals;
- **connectives:** sparse, explicit, conversational, formal;
- **stance:** directness, certainty, hedging, criticism, enthusiasm;
- **politeness:** honorifics, address system, requests, imperatives;
- **emphasis:** repetition, punctuation, line breaks, emoji, capitalization;
- **humor and idiom:** only observed forms;
- **technical density:** terminology, abbreviations, code-adjacent language;
- **locale and dialect:** spelling, vocabulary, morphology, accepted regional forms;
- **stable quirks to preserve:** recurring phrases or structures that belong to this author;
- **prohibited shifts:** tones or forms the user rejected or the venue forbids.

Absence of evidence is `unknown`, not permission to fabricate.

## 3. Naturalness is constrained variation

Human prose is not uniformly polished, but randomness is not a substitute for a voice.

Preserve when they are functional or characteristic:

- unequal sentence and paragraph lengths;
- a short fragment after a longer sentence;
- a plain repeated word used for emphasis;
- omitted subjects or objects where the language supports it;
- a mild digression or parenthetical;
- a direct statement without a transition;
- asymmetrical lists and endings.

Fix when they block comprehension, contradict the requested venue, or are accidental rather than characteristic.

Never add typos, broken grammar, fake hesitations, filler words, slang, anecdotes, jokes, opinions, or emotional reactions merely to create irregularity.

## 4. Operation rules

### write

Use the strongest available profile. With no author samples, use a restrained, venue-native default. Do not claim to reproduce a personal voice that was never supplied.

### review

Do not edit. Separate:

- clarity defects;
- machine-like uniformity clusters;
- venue mismatch;
- locale mismatch;
- voice-preservation risks;
- features that look unusual but should be preserved.

Quote evidence. A single phrase is never enough to diagnose machine-like prose.

### refactor

Make the smallest changes that solve documented defects. Preserve structure and voice unless the user explicitly authorizes deeper changes. When clarity and a stable quirk conflict, prefer a local fix over deleting the quirk everywhere.

### recreate

Before drafting, extract:

1. facts and numbers;
2. claims and degree of certainty;
3. purpose and audience;
4. emotional temperature;
5. register and social relationship;
6. voice anchors and regional forms;
7. quotations, code, URLs, names, and terms that must remain exact.

A new structure does not authorize a new personality.

## 5. Preservation report

Do not invent a numerical “naturalness” or “human” score. When a report is useful, use evidence-backed statuses:

| Dimension | Allowed status |
|---|---|
| meaning | preserved / changed with authorization / unresolved |
| facts and constraints | preserved / unresolved |
| author voice | preserved / partially preserved / insufficient evidence |
| register and relationship | preserved / intentionally changed / unresolved |
| locale and dialect | preserved / intentionally changed / unresolved |
| over-polishing risk | low / medium / high, with a reason |

Numbers are appropriate only for objective counts, such as facts checked or quotations preserved.

## 6. Conflict order

Resolve conflicts in this order:

1. facts, safety, legal and technical correctness;
2. explicit user instructions;
3. meaning and degree of certainty;
4. social relationship and locale;
5. established author voice;
6. venue conventions;
7. generic style preferences.

A style heuristic never outranks a fact, quote, command, identifier, or explicit voice instruction.
