# LLM Benchmark Design

## Purpose

This document describes how to design and run a large language model benchmark.
It also applies the method to LLM Transitivity.

A benchmark is not only a prompt collection. It is an experimental protocol.
The protocol defines the claim, test cases, tested system, execution settings,
scoring rules, and analysis method.

## Define the claim

Start with one claim that the benchmark can test. A suitable claim for this
project is:

> A model can apply hypothetical syllogism without support from semantic
> plausibility.

This claim has two parts:

- The model must identify valid and invalid logical forms.
- The result must not depend on whether the statements agree with world
  knowledge.

The benchmark must include controls for both parts. A set that contains only
valid arguments cannot show that the model detects validity. A model that
always answers `yes` will pass that set.

## Define the tested system

A result applies to the full tested system. The system can include these
components:

- Model and model version.
- Provider and API.
- System prompt and user prompt.
- Generation settings.
- Reasoning setting.
- Tool access.
- Retry policy.
- Output parser.

The current project tests a model through OpenRouter with a fixed system prompt.
It does not test the model independently from this configuration.

The evaluation report must identify each system component. It must also record
the test date. A provider can change a model alias or an inference service.

[HELM][1] uses a standard scenario, adaptation, and metric structure. This
structure makes results easier to compare. A 2026 evaluation guide also
recommends that reports identify the tested system, harness, budget,
elicitation method, and validity checks [OpenAI evaluation guide][2].

## Design the test set

### Use a factorial design

The test set must vary one controlled factor at a time. The core design for
LLM Transitivity is:

| Factor | Values |
| --- | --- |
| Logical validity | Valid, invalid |
| Content type | Plausible, implausible, abstract |
| Conclusion plausibility | Plausible, implausible |
| Prompt method | Zero-shot, reasoning prompt |

This design supports separate measurements for logic and semantic
plausibility. It also supports interaction analysis. For example, it can show
whether implausible content reduces accuracy only for valid arguments.

Do not mix prompt methods in one score. Treat each method as a separate test
condition.

### Use matched cases

Create a valid case and one or more invalid cases from the same terms. This
method reduces the effect of vocabulary and topic.

Valid form:

```text
A -> B
B -> C
Therefore, A -> C
```

Invalid form with an unrelated premise:

```text
A -> B
D -> C
Therefore, A -> C
```

Invalid converse:

```text
A -> B
B -> C
Therefore, C -> A
```

Invalid reversed chain:

```text
B -> A
C -> B
Therefore, A -> C
```

Other invalid forms can test an antecedent mismatch, a consequent mismatch, or
a missing link. Each invalid form must have a clear formal definition.

### Generate cases from symbolic forms

Use a symbolic representation as the source of truth. Generate the natural
language text from that representation. Calculate the expected answer from the
symbolic form.

This order prevents a text edit from silently changing the logical form. It
also makes it possible to create new private cases. Private or dynamic cases
reduce contamination risk. Public benchmark items can occur in model training
data. This overlap can increase a score without an increase in generalization
[Deng et al.][3]. Recent work recommends a move from fixed public sets to
dynamic evaluation when this risk is material [Chen et al.][4].

### Audit the test set

Review each case before use. The review must check:

- The formal label.
- The natural language realization.
- The identity of each predicate.
- Ambiguous grammar.
- Duplicate cases.
- Accidental clues in wording or answer order.
- Balance across all test conditions.

Use at least two reviewers for a final research dataset. Resolve each
disagreement and record the decision.

Keep development cases separate from final test cases. Do not tune prompts on
the final test set.

## Define the record format

Each case must include the factors that are required for analysis. A possible
format is:

```json
{
  "id": "hs-valid-abstract-001",
  "task": "hypothetical_syllogism",
  "valid": true,
  "content_type": "abstract",
  "conclusion_plausibility": "neutral",
  "logical_form": {
    "premises": ["A -> B", "B -> C"],
    "conclusion": "A -> C"
  },
  "expected_answer": "yes",
  "prompt": "..."
}
```

Store dataset and prompt versions with each result. Do not rely only on a file
name or the current Git state.

## Fix the execution protocol

Use the same execution conditions for each compared system. Record:

- Exact model identifier.
- Provider.
- Date and time.
- System and user prompts.
- Temperature, `top_p`, seed, and token limit.
- Reasoning effort, if available.
- Number of attempts.
- Retry and timeout rules.
- Raw response.
- Parsed answer.
- Input and output token counts.
- Latency and cost.
- Error status.

Randomize case order if the provider can keep state or if the test uses a
multi-turn session. Use an independent session for each case unless session
memory is part of the claim.

Run each case more than once when generation is stochastic. Report both average
accuracy and response consistency. A seed does not guarantee identical output
for all hosted systems.

The Language Model Evaluation Harness uses shareable task configuration files
and records task settings to support reproduction [task guide][5]. Its authors
also describe common reproduction problems in language model evaluation
[Biderman et al.][6].

## Score the responses

Use deterministic scoring when the expected answer has a closed form. For this
project, the scorer can normalize the response, extract `yes` or `no`, and
compare it with `expected_answer`.

Record format compliance as a separate metric. Do not count a correct label and
an invalid format as the same type of failure.

Use an LLM judge only when a deterministic rule is not sufficient. First
compare the judge with human labels on a representative sample. LLM judges can
have position, verbosity, and self-preference biases [Zheng et al.][7]. Reverse
the candidate order in pairwise evaluation and measure position consistency.

## Report metrics

Report results for each test condition. Do not report only total accuracy.

The minimum report for this project must include:

- Accuracy for valid cases.
- Accuracy for invalid cases.
- Accuracy for each content type.
- Macro accuracy across the six validity and content cells.
- Format compliance rate.
- Consistency across repeated runs.
- Token use, latency, and cost.
- Number of test cases.
- A 95% confidence interval.

Use macro accuracy so that a large test condition does not hide a weak small
condition:

```text
macro accuracy = mean(accuracy for each validity-content cell)
```

Define a semantic plausibility effect:

```text
plausibility effect = accuracy on abstract cases
                    - accuracy on conflicting cases
```

Use a Wilson interval or a bootstrap interval for one accuracy estimate. Use a
paired bootstrap test or McNemar's test to compare two systems on the same
cases. Report the effect size with the test result.

For a detailed experiment, use a logistic mixed-effects model. Include system,
validity, content type, and their interactions as fixed effects. Include case as
a random effect.

[HELM][1] reports more than accuracy. Its dimensions include calibration,
robustness, fairness, bias, toxicity, and efficiency. Not all dimensions apply
to this small logic benchmark. Robustness and efficiency do apply.

## Check validity

Inspect a sample of raw responses after every run. Check for these hazards:

- The model uses a wording shortcut.
- The model repeats a memorized answer.
- The parser changes the meaning of a response.
- A case has no unique correct answer.
- A refusal is scored as a logical error without a separate record.
- A prompt format gives one system an avoidable disadvantage.
- A retry policy gives systems different compute budgets.
- A model gets the answer through a tool instead of the tested capability.

Report known hazards with the score. A score does not support a capability
claim if the test permits a simpler shortcut.

## Current project assessment

The current dataset has 57 cases. It has no expected answer field. Most cases,
and possibly all intended cases, use an affirmative hypothetical syllogism. A
system that always answers `yes` can therefore obtain a high score.

The current data also has these issues:

- Cases 9 through 13 repeat the second premise as the conclusion. They do not
  directly test the `A -> C` inference.
- Some cases have typographical or grammatical errors.
- Small predicate changes can change the formal argument. For example, `closed`
  and `close` are not the same predicate.
- The dataset does not identify content type or logical validity.
- There is no development and test split.

The current runner stores raw responses but does not calculate a score. It also
replaces a prior result with the same case identifier. It does not record all
settings that are required to reproduce a run.

These limits mean that current outputs are exploratory data. They are not yet
evidence for the benchmark claim.

## Recommended implementation order

1. Define valid and invalid symbolic templates.
2. Add expected answers and test condition fields.
3. Correct and audit the current cases.
4. Balance the dataset across validity and content type.
5. Add deterministic answer parsing and scoring.
6. Store immutable run metadata and raw responses.
7. Add per-condition metrics and confidence intervals.
8. Run a small pilot and inspect all failures.
9. Freeze a private final test set.
10. Compare systems with the same execution budget.

## References

1. Stanford CRFM. [Holistic Evaluation of Language Models][1]. 2022.
2. OpenAI. [A shared playbook for trustworthy third-party evaluations][2].
   2026.
3. Deng et al. [Investigating Data Contamination in Modern Benchmarks for Large
   Language Models][3]. NAACL 2024.
4. Chen et al. [Benchmarking Large Language Models Under Data Contamination:
   A Survey from Static to Dynamic Evaluation][4]. EMNLP 2025.
5. EleutherAI. [Language Model Evaluation Harness task guide][5].
6. Biderman et al. [Lessons from the Trenches on Reproducible Evaluation of
   Language Models][6]. 2024.
7. Zheng et al. [Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena][7].
   2023.
8. OpenAI. [Evaluation best practices][8].

[1]: https://arxiv.org/abs/2211.09110
[2]: https://openai.com/index/trustworthy-third-party-evaluations-foundations/
[3]: https://aclanthology.org/2024.naacl-long.482/
[4]: https://aclanthology.org/2025.emnlp-main.511/
[5]: https://github.com/EleutherAI/lm-evaluation-harness/blob/main/docs/task_guide.md
[6]: https://arxiv.org/abs/2405.14782
[7]: https://arxiv.org/abs/2306.05685
[8]: https://platform.openai.com/docs/guides/evaluation-best-practices
