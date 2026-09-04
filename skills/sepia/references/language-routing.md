# Language routing

This file decides which language layer Sepia loads. It does not translate text and it does not identify whether a human or a model wrote it.

## 1. Resolution order

Use the first reliable signal:

1. **Explicit output instruction.** A requested language or locale wins.
2. **Explicit audience or publication variety.** Examples: Japanese customers, a UK changelog, a Mexican support reply.
3. **Source evidence.** Preserve the dominant language, spelling system, forms of address, punctuation, terminology, and regional vocabulary already present.
4. **Conversation language.** Use the user's current language only when writing new material and no stronger signal exists.
5. **Conservative fallback.** Keep the source as-is. For new content with no usable signal, use the user's language and a neutral venue-appropriate register.

Do not use names, URLs, code, product names, quoted strings, or isolated borrowed words as language evidence.

## 2. Supported routes

| Route | Load | Locale policy |
|---|---|---|
| Japanese | `languages/ja-JP.md` | `ja-JP`; preserve register, orthography, and established terminology |
| English | `languages/en.md` | preserve observed variety such as en-US, en-GB, en-AU, en-CA; never normalize by default |
| Spanish | `languages/es.md` | preserve observed country/region, address system, and lexicon; broad-audience fallback may use restrained neutral Spanish |

Always load `languages/shared.md` and `human-voice.md` alongside the selected route.

## 3. Mixed-language material

A document is mixed-language only when complete clauses or audience-facing segments genuinely use different languages. Brand names, code, commands, UI labels, quotations, and accepted loanwords do not create a second route.

- Keep each segment in its source language unless translation was explicitly requested.
- Apply each language layer only to its own segment.
- Preserve cross-language technical terminology when that is normal for the venue.
- Do not harmonize punctuation or capitalization across languages when each segment follows its own convention.
- When a quoted passage is in another language, treat it as quoted material and leave it unchanged.

## 4. Locale evidence

### English

Look for spelling (`colour`/`color`, `organise`/`organize`), quotation style, date format, vocabulary, institutional names, and author samples. One spelling alone is weak evidence; several consistent cues are strong evidence.

### Spanish

Look for `tú`, `usted`, or `vos`; `vosotros` or `ustedes`; verb morphology; regional vocabulary; punctuation; institutional names; and author samples. Do not infer a country from one word when several regions share it.

### Japanese

The language route is normally `ja-JP`, but register is still a locale-like choice: casual, `です・ます`, `だ・である`, customer-service polite, or formal institutional prose. Preserve established orthography, full-/half-width conventions, product spellings, and domain terminology.

## 5. Low-confidence behavior

- **review:** state the ambiguity and diagnose only patterns that do not depend on guessing the locale.
- **refactor:** preserve source forms; do not normalize.
- **recreate:** carry forward the source's strongest cues. When no source exists, use a restrained broad-audience default.
- **write:** use explicit audience information; otherwise use the user's language and venue-appropriate register without fabricated regional color.

## 6. Reporting

For review, report:

- selected language layer;
- locale or regional variety, or `unknown/preserved`;
- confidence: high, medium, or low;
- evidence used;
- any locale-sensitive changes that would require user authorization.

Do not report a “human probability” or an AI-detector score.
