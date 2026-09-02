# Repository Guidelines

These rules apply to the entire repository.

## Writing

- Use ASD-STE100 Simplified Technical English for documentation, comments, commit messages, and other project text.
- Use short, direct sentences.
- Use one term for one concept. Do not use synonyms only for variety.
- Avoid filler, vague claims, repeated information, and unnecessary headings.
- Do not add obvious comments or documentation that only restates the code.

## Changes

- Keep changes focused on the requested task.
- Do not add speculative features, abstractions, dependencies, or unrelated cleanup.
- Follow the existing project structure unless the task requires a change.
- Remove generated files and temporary artifacts before completion.

## Commits

- Use Conventional Commits.
- A scope is required. Use the form `type(scope): description`.
- Use a short, imperative description in ASD-STE100 Simplified Technical English.
- Make atomic commits. Each commit must contain one complete logical change.
- Do not mix refactors, formatting, fixes, and features in one commit unless they are inseparable.
- Never add a `Co-authored-by` trailer or any equivalent co-author attribution.

Examples:

```text
docs(readme): add setup instructions
fix(runner): validate model responses
test(prompts): add invalid syllogism cases
```
