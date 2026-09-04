# Multilingual voice acceptance fixtures

`cases.json` defines preservation-first cases for Japanese, English, Spanish, and mixed technical prose. They are specification fixtures, not deterministic proof that a model will always produce a good edit.

A behavioral runner should evaluate each case against the four graders in `graders/` and record the executing model and version. The suite also includes an explicit-profile case so inferred style never silently outranks user-owned settings. Review cases must not contain an edited replacement. Refactor and recreate cases must preserve every `must_preserve` item and avoid every `forbidden_changes` item.
