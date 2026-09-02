# Benchmarks for Abstraction

Research note. Sources were checked on 2026-09-02.

## Summary

Several benchmarks evaluate abstraction. They do not all measure the same
ability. The main groups are:

- Linguistic abstraction and conceptualization.
- Concept learning across different examples.
- Symbolic abstraction across changed representations.
- Visual abstraction and perception.

There is no single standard benchmark for abstraction.

## Linguistic abstraction

### AbsPyramid

[AbsPyramid](https://aclanthology.org/2024.findings-naacl.252/) is the most
direct benchmark for abstraction in language models. It contains 221K textual
descriptions of abstraction knowledge. The data covers three components of
events: nouns, verbs, and complete events.

It provides two tasks:

- Abstraction detection: decide whether a candidate concept is an abstraction
  of a textual description.
- Abstraction generation: produce abstract concepts for a description.

The authors evaluate zero-shot, few-shot, and fine-tuned language models. The
paper reports that models have difficulty with abstraction knowledge in
zero-shot and few-shot settings. The official repository is available at
[HKUST-KnowComp/AbsPyramid](https://github.com/hkust-knowcomp/abspyramid).

### AbstractATOMIC

[AbstractATOMIC](https://arxiv.org/abs/2206.01532) is a large resource for
conceptualizing commonsense events. It links concrete events and situations to
more general concepts. The work annotates valid and invalid conceptualizations
and builds abstract commonsense knowledge from the ATOMIC knowledge base.

The resource supports evaluation of whether a model can move from a specific
event to an appropriate abstract concept. It is also used as a source for
other abstraction benchmarks.

### IOLBENCH

[IOLBENCH](https://arxiv.org/abs/2501.04249) uses self-contained problems from
the International Linguistics Olympiad. The tasks cover syntax, morphology,
phonology, and semantics. They use small sets of examples and do not require
external knowledge.

The benchmark tests whether a model can identify linguistic patterns and apply
them to new cases. It is a benchmark for linguistic abstraction rather than
for abstract concepts in the taxonomy sense.

## Concept learning and generalization

### ConceptARC

[ConceptARC](https://arxiv.org/abs/2305.07141) organizes visual tasks into
groups that focus on specific concepts. The problems vary in complexity and
level of abstraction.

The benchmark evaluates whether a system uses a concept across many different
instances. This approach is designed to reveal failures that a conventional
random train-test split can hide.

### Bongard-LOGO

[Bongard-LOGO](https://papers.nips.cc/paper/2020/hash/bf15e9bbff22c7719020f9df4badc20a-Abstract.html)
is a visual concept-learning benchmark. A system receives a small number of
positive and negative examples and must identify the concept that separates
them.

The benchmark includes context-dependent perception, analogy-making
perception, and concept learning with a broad vocabulary. Its abstract-shape
problems use large visual variation so that a system cannot rely on a small set
of memorized shapes.

### KANDY

[KANDY](https://arxiv.org/abs/2402.17431) is a framework for generating
curricula of visual concept-learning tasks. It uses compositional symbols,
sparse supervision, and increasing task complexity.

The benchmark includes symbolic representations and ground-truth rules. This
supports analysis of whether a model has learned a concept and how it combines
previous concepts.

## Symbolic abstraction

### Symbol remapping benchmark

[Benchmarking Abstract and Reasoning Abilities Through A Theoretical
Perspective](https://arxiv.org/abs/2505.23833) defines abstraction as finding
patterns that are independent of surface representations and applying the same
rules to those patterns.

Its central test changes the symbols in rule-based tasks. The benchmark
compares performance before and after systematic symbol remapping. The authors
use one score for task accuracy and another score for dependence on the
original symbols.

This design treats a performance drop after remapping as evidence that a model
may rely on memorized surface patterns.

## Visual abstraction and perception

### ARC-AGI

[ARC-AGI](https://github.com/fchollet/arc-agi) presents small input-output grid
examples. A system must identify the transformation shared by the examples and
produce the correct output for a new input.

The official ARC-AGI-1 repository contains 400 training tasks and 400
evaluation tasks. Each task usually provides a small number of demonstrations.
The benchmark is designed to test rapid acquisition of new abstractions with
limited examples.

### SEVA

[SEVA](https://seva-benchmark.github.io/) contains more than 90,000 human-made
sketches across 128 object concepts. The sketches vary in sparsity and detail.

It evaluates both concept recognition and similarity between machine and human
responses. It therefore studies visual abstraction and the alignment of model
perception with human perception.

## Comparison

| Benchmark | Modality | Main abstraction unit | Main task |
| --- | --- | --- | --- |
| AbsPyramid | Text | Noun, verb, or event concept | Detect or generate an abstraction |
| AbstractATOMIC | Text | Commonsense event concept | Build and validate conceptualizations |
| IOLBENCH | Text | Linguistic rule or pattern | Infer a pattern from examples |
| ConceptARC | Visual | Spatial or semantic concept | Apply a concept across varied instances |
| Bongard-LOGO | Visual | Visual concept | Separate positive and negative examples |
| KANDY | Visual and symbolic | Composed visual concept | Learn concepts in a curriculum |
| Symbol remapping benchmark | Symbolic text | Representation-independent rule | Transfer a rule after symbol changes |
| ARC-AGI | Visual | Grid transformation | Infer and apply a new transformation |
| SEVA | Visual | Object concept and visual abstraction | Match concepts and human responses |

## Sources

- [AbsPyramid: Benchmarking the Abstraction Ability of Language Models with a Unified Entailment Graph](https://aclanthology.org/2024.findings-naacl.252/)
- [AbsPyramid official repository](https://github.com/hkust-knowcomp/abspyramid)
- [Acquiring and Modelling Abstract Commonsense Knowledge via Conceptualization](https://arxiv.org/abs/2206.01532)
- [IOLBENCH: Benchmarking LLMs on Linguistic Reasoning](https://arxiv.org/abs/2501.04249)
- [ConceptARC: Evaluating Understanding and Generalization in the ARC Domain](https://arxiv.org/abs/2305.07141)
- [Bongard-LOGO: A New Benchmark for Human-Level Concept Learning and Reasoning](https://papers.nips.cc/paper/2020/hash/bf15e9bbff22c7719020f9df4badc20a-Abstract.html)
- [The KANDY Benchmark](https://arxiv.org/abs/2402.17431)
- [Benchmarking Abstract and Reasoning Abilities Through A Theoretical Perspective](https://arxiv.org/abs/2505.23833)
- [ARC-AGI official repository](https://github.com/fchollet/arc-agi)
- [SEVA benchmark](https://seva-benchmark.github.io/)
