# Shared multilingual editorial rules

These rules apply to Japanese, English, and Spanish. They are editorial heuristics, not authorship tests.

## Diagnose clusters, not tokens

Do not flag a word merely because language models often use it. Flag a pattern only when several features combine and harm the piece: repeated signposting, uniform paragraph logic, generic uplift, empty abstraction, excessive hedging, symmetrical lists, canned conclusions, or a register that ignores the audience.

For every finding, identify:

1. the exact passage;
2. the repeated or structural pattern;
3. why it hurts this language, voice, or venue;
4. the smallest safe correction;
5. what must be preserved.

## Preserve load-bearing material

Keep exact unless the user authorizes a change:

- facts, quantities, dates, versions, units, and degrees of certainty;
- quotations and dialogue;
- URLs, email addresses, filenames, paths, commands, code, identifiers, and UI labels;
- legal, medical, scientific, and domain terms;
- personal and organization names;
- official product spellings;
- regional language choices and forms of address.

## Common cross-language defects

Check for clusters of:

- an opening that announces the topic instead of beginning it;
- paragraphs with identical claim → explanation → summary shapes;
- unnecessary summaries that repeat the immediately preceding text;
- every transition being explicit;
- abstract nouns where a direct verb would be clearer;
- claims inflated beyond the evidence;
- equal-length paragraphs or mechanically balanced three-part lists;
- generic benefits without actors, conditions, or consequences;
- headings that repeat the first sentence;
- a conclusion that merely restates the introduction;
- abrupt shifts into corporate, academic, intimate, or promotional register.

## What to preserve

Do not “fix” these by default:

- formal prose in a formal venue;
- ordinary connectives used sparingly;
- repeated terminology needed for precision;
- a short sentence, fragment, or aside that matches the author;
- a conventional template required by a venue;
- accepted spelling and regional variants;
- code-adjacent English inside Japanese or Spanish technical writing;
- deliberate repetition for rhythm or emphasis.

## Naturalness without performance

Natural prose is aligned with a real speaker, audience, purpose, and language convention. It is not automatically casual, emotional, witty, fragmented, or full of contractions. Never add human “tells” as decoration.

## Final scan

Before returning an edit:

- compare every factual token and quotation with the source;
- verify the selected language and locale remain stable;
- check that sentence variation emerged from meaning, not randomness;
- remove only defects that were actually diagnosed;
- ensure the author's stance, warmth, directness, and uncertainty did not drift;
- ensure no sentence claims detector evasion or human authorship certainty.
