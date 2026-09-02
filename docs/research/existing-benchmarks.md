# Existing Benchmarks for LLM Transitivity

Research note for LLM Transitivity. Sources were checked on 2026-09-02.

## Executive conclusion

The core task already has direct precedents. LogicBench evaluates the same
hypothetical syllogism pattern:

```text
(p -> q) and (q -> r) therefore (p -> r)
```

CounterLogic is the closest precedent for the project idea of testing logic
when content conflicts with world knowledge. SemEval-2026 Task 11 also treats
formal validity and plausibility as separate factors.

LLM Transitivity can still be a useful benchmark. It should not claim to be
the first benchmark for hypothetical syllogism or transitivity. A stronger
claim is that it provides a focused and controlled test of transitivity under
semantic interference, with matched cases, explicit labels, and reproducible
scoring.

## Project baseline

The repository currently contains 57 hypothetical syllogism cases in
[`prompts/userPrompts/HS.json`](../../prompts/userPrompts/HS.json). The cases
ask whether a conclusion follows from two conditional statements. Some cases
use plausible content. Others use content that conflicts with world
knowledge.

The current data does not include expected answers, formal validity labels, or
content labels. Most cases, and possibly all intended cases, are affirmative
transitivity cases. The runner stores raw responses but does not calculate
accuracy. These limits make the current data useful for exploration, but not
yet sufficient for a controlled benchmark.

## Direct and related precedents

| Resource | Relation to this project | Main difference | Use for this project |
| --- | --- | --- | --- |
| [LogicBench](https://aclanthology.org/2024.acl-long.739/) | Direct match. It includes hypothetical syllogism as one of 25 reasoning patterns across propositional, first-order, and non-monotonic logic. | It covers many inference rules and supports binary and multiple-choice question formats. | Use it as the main direct baseline. Do not claim that the logical pattern is new. |
| [CounterLogic](https://arxiv.org/html/2505.22318) | Very close conceptual match. It includes the same transitivity schema and tests reasoning in counterfactual worlds. | It uses nine schemas, one to nine reasoning steps, and a larger balanced dataset. | Use it as the closest comparison for plausibility and knowledge conflict. |
| [LogicAsker](https://aclanthology.org/2024.emnlp-main.128/) | Related rule-based natural-language reasoning benchmark. | It generates inference, contradiction, and unrelated questions with configurable rule chains. | Use it as a reference for generation and negative outcomes. |
| [Bertolazzi et al.](https://aclanthology.org/2024.emnlp-main.769/) | Studies how believable and unbelievable content affects LLM syllogistic reasoning. | It uses categorical syllogisms, not only propositional conditional chains. It also studies three- and four-premise arguments. | Use it to justify a matched plausibility design and content-effect metrics. |
| [SylloBase](https://aclanthology.org/2023.findings-acl.148/) | Large natural-language syllogism resource with generated and manually rewritten data. | It covers broad syllogistic reasoning and has a larger scale than the current repository. | Use it as a reference for dataset scale and manual test-set review. |
| [SemEval-2026 Task 11](https://sites.google.com/view/semeval-2026-task-11) | Direct design precedent for separating formal validity from plausibility. | It focuses on categorical syllogisms, irrelevant premises, content-effect scores, and multilingual evaluation. | Use its validity, plausibility, and irrelevant-premise factors as design references. |
| [ConsistencyBench](https://github.com/aayambansal/ConsistencyBench) | Includes transitivity questions with the same `A -> B`, `B -> C`, therefore `A -> C` structure. | Its unit of evaluation is cross-query consistency. It tests whether related answers remain mutually consistent, not only whether one conclusion follows. | Use it if the project adds repeated or linked cases and a consistency score. |
| [RuleTaker](https://github.com/allenai/ruletaker) | Related natural-language multi-hop rule reasoning benchmark. | It uses facts and rules over entities rather than a focused hypothetical syllogism task. | Use it as background for rule-chain generation and multi-hop evaluation. |

## What the literature shows

### The logical form is established

LogicBench is the clearest direct precedent. It evaluates a single inference
rule at a time and includes hypothetical syllogism in its rule set. The form
is therefore a known evaluation target.

The contribution cannot be the use of the form alone. A contribution may come
from a narrower protocol, a new language, a new source of controlled content,
or a new analysis of failure modes. The protocol must state which of these is
new.

### Semantic interference is an established problem

Several works report that models can use world knowledge when they should use
only the statements in the prompt. This can create two errors:

- A model rejects a formally valid argument because its content seems false.
- A model accepts an invalid argument because its conclusion seems plausible.

CounterLogic, Bertolazzi et al., and SemEval-2026 Task 11 all support a design
that keeps logical form constant while changing content plausibility. This is
the strongest research direction for LLM Transitivity.

### Negative controls are required

A dataset with only valid chains cannot show that a model checks the logical
form. A model that always answers `yes` can obtain a high score. The benchmark
needs matched invalid cases, such as:

```text
A -> B
D -> C
therefore A -> C
```

Other useful controls include the converse, a reversed chain, a missing link,
and a changed antecedent or consequent. Each control needs a symbolic label.

### Public data creates contamination risk

The central calendar example in case 2 of the current dataset appears verbatim
in an instructional PDF from Florida State University:
[`UNIT2MODULE1.pdf`](https://www.math.fsu.edu/~wooland/hm/Unit2Module1/UNIT2MODULE1.pdf).
This finding does not prove that a model saw the example during training. It
does show that public examples can have a different status from newly written
test items.

Use public data for development and comparison. Use private, held-out, or
dynamically generated items for the final claim.

### Evaluation should include more than total accuracy

The closest precedents report condition-level results or content-effect
measures. A single total score can hide a strong answer bias or a large drop on
implausible content.

At minimum, report:

- Accuracy on valid cases.
- Accuracy on invalid cases.
- Accuracy by plausibility condition.
- Yes-answer rate.
- Format compliance.
- Consistency across repeated runs.

For matched cases, report a plausibility effect. One simple definition is:

```text
plausibility effect = accuracy on plausible cases
                     - accuracy on implausible cases
```

Use the same cases for every compared model. Report confidence intervals for
accuracy and uncertainty for every condition.

## Gap between the repository and existing benchmarks

The repository has a clear research question, but its current implementation
does not yet support a benchmark claim.

| Requirement | Current state | Impact |
| --- | --- | --- |
| Formal labels | Missing | The runner cannot score validity. |
| Invalid cases | Not balanced | The runner cannot measure logical discrimination. |
| Plausibility labels | Missing | The runner cannot measure semantic interference. |
| Matched item pairs | Not defined | Vocabulary can confound comparisons. |
| Deterministic scoring | Missing | Results require manual interpretation. |
| Run metadata | Incomplete | Results are hard to reproduce. |
| Development and test split | Missing | Prompt tuning can overfit the test set. |
| Contamination review | Not complete | A public example may inflate apparent performance. |

The current research file, [`llm-benchmarking.md`](llm-benchmarking.md),
contains the broader benchmark design requirements and implementation order.

## Recommended positioning

Use a claim such as:

> LLM Transitivity is a controlled benchmark for testing hypothetical
> syllogism under semantic interference. It compares formal validity with
> content plausibility using matched natural-language cases.

Avoid claims such as:

- The first benchmark for transitivity.
- The first benchmark for hypothetical syllogism.
- A direct measure of general reasoning ability.

These claims are too broad given LogicBench and the related work.

## Recommended next version

1. Define symbolic templates for valid and invalid arguments.
2. Generate the natural-language cases from the symbolic templates.
3. Add `expected_answer`, `validity`, `content_type`, and `plausibility` fields.
4. Create matched cases with a balanced validity by plausibility design.
5. Add abstract or nonce content to reduce world-knowledge effects.
6. Add a deterministic parser and a score for format compliance.
7. Record the model, provider, prompt version, settings, timestamp, raw answer,
   parsed answer, token use, latency, and errors.
8. Add private or dynamic final items and review them for contamination.
9. Compare results with LogicBench and CounterLogic under the same execution
   budget.

## Sources

- Parmar et al. (ACL 2024), [LogicBench: Towards Systematic Evaluation of
  Logical Reasoning Ability of Large Language Models](https://aclanthology.org/2024.acl-long.739/).
- Parmar et al., [LogicBench source code](https://github.com/Mihir3009/LogicBench).
- [CounterLogic: Flying Pigs, FaR and Beyond](https://arxiv.org/html/2505.22318).
- Wan et al. (EMNLP 2024), [LogicAsker](https://aclanthology.org/2024.emnlp-main.128/).
- Wan et al., [LogicAsker source code](https://github.com/yxwan123/LogicAsker).
- Bertolazzi et al. (EMNLP 2024), [A Systematic Analysis of Large Language
  Models as Soft Reasoners](https://aclanthology.org/2024.emnlp-main.769/).
- [SylloBase](https://aclanthology.org/2023.findings-acl.148/).
- [SemEval-2026 Task 11](https://sites.google.com/view/semeval-2026-task-11) and
  its [source repository](https://github.com/neuro-symbolic-ai/semeval_2026_task_11).
- Bansal (ICLR 2026 Workshop), [ConsistencyBench](https://github.com/aayambansal/ConsistencyBench).
- Saxton et al. (2020), [RuleTaker](https://arxiv.org/abs/2002.05867).
- Florida State University, [logic instructional example](https://www.math.fsu.edu/~wooland/hm/Unit2Module1/UNIT2MODULE1.pdf).
