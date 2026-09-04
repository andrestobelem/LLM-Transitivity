"""Generate controlled hypothetical syllogisms with NLTK WordNet."""

from __future__ import annotations

import argparse
import json
import random
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

import nltk
from nltk.corpus import brown
from nltk.corpus import wordnet as wn
from nltk.corpus.reader.wordnet import Synset

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = PROJECT_ROOT / "prompts" / "userPrompts" / "HS_NLTK.json"
DEFAULT_LABELS_OUTPUT = PROJECT_ROOT / "prompts" / "userPrompts" / "HS_NLTK_labels.json"
WORD_RE = re.compile(r"^[a-z]{3,16}$")
DEFAULT_MIN_FREQUENCY = 10
ALLOWED_LEXNAMES = {
    "noun.animal",
    "noun.artifact",
    "noun.body",
    "noun.food",
    "noun.group",
    "noun.location",
    "noun.object",
    "noun.person",
    "noun.plant",
}
EXCLUDED_WORDS = {
    "abstraction",
    "artifact",
    "being",
    "entity",
    "group",
    "matter",
    "object",
    "physical_entity",
    "physical_object",
    "thing",
    "whole",
}


@dataclass(frozen=True)
class Concept:
    synset: str
    word: str


@dataclass(frozen=True)
class Chain:
    general: Concept
    middle: Concept
    specific: Concept


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a WordNet-based HS prompt dataset."
    )
    parser.add_argument(
        "--count",
        type=int,
        default=100,
        help="Number of cases to generate (default: 100).",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed for reproducible output (default: 42).",
    )
    parser.add_argument(
        "--min-frequency",
        type=int,
        default=DEFAULT_MIN_FREQUENCY,
        help=(
            "Minimum Brown corpus frequency for each noun "
            f"(default: {DEFAULT_MIN_FREQUENCY})."
        ),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Path for the HS prompt file.",
    )
    parser.add_argument(
        "--labels-output",
        type=Path,
        default=DEFAULT_LABELS_OUTPUT,
        help="Path for the answer key and generation metadata.",
    )
    parser.add_argument(
        "--download-nltk-data",
        "--download-wordnet",
        dest="download_nltk_data",
        action="store_true",
        help="Download the NLTK WordNet and Brown data when they are missing.",
    )
    return parser.parse_args()


def project_path(path: Path) -> Path:
    if path.is_absolute():
        return path
    return PROJECT_ROOT / path


def ensure_nltk_data(download_nltk_data: bool) -> None:
    try:
        wn.synsets("dog")
        brown.words()
    except LookupError as error:
        if not download_nltk_data:
            raise SystemExit(
                "NLTK WordNet or Brown data is missing. "
                "Run again with --download-nltk-data."
            ) from error
        for package in ("wordnet", "brown"):
            if not nltk.download(package, quiet=True):
                raise RuntimeError(
                    f"NLTK could not download the {package} data."
                ) from error
        wn.synsets("dog")
        brown.words()


def concept_for(
    synset: Synset, frequencies: Counter[str], min_frequency: int
) -> Concept | None:
    if synset.lexname() not in ALLOWED_LEXNAMES:
        return None
    words = sorted({lemma.name() for lemma in synset.lemmas()})
    for raw_word in words:
        word = raw_word.lower()
        if raw_word != word:
            continue
        if word in EXCLUDED_WORDS:
            continue
        if not WORD_RE.fullmatch(word):
            continue
        if frequencies[word] < min_frequency:
            continue
        if wn.morphy(word, wn.NOUN) != word:
            continue
        return Concept(synset=synset.name(), word=word)
    return None


def build_chains(min_frequency: int) -> list[Chain]:
    frequencies = Counter(
        word.lower()
        for word, tag in brown.tagged_words()
        if tag == "NN" and word == word.lower() and WORD_RE.fullmatch(word.lower())
    )
    chains: dict[tuple[str, str, str], Chain] = {}
    for synset in wn.all_synsets(pos=wn.NOUN):
        for path in synset.hypernym_paths():
            start = max(0, len(path) - 7)
            for index in range(start, len(path) - 2):
                if len({item.lexname() for item in path[index : index + 3]}) != 1:
                    continue
                general = concept_for(path[index], frequencies, min_frequency)
                middle = concept_for(path[index + 1], frequencies, min_frequency)
                specific = concept_for(path[index + 2], frequencies, min_frequency)
                concepts = (general, middle, specific)
                if any(concept is None for concept in concepts):
                    continue
                words = tuple(concept.word for concept in concepts if concept)
                if len(set(words)) != 3:
                    continue
                chains.setdefault(
                    words,
                    Chain(general=general, middle=middle, specific=specific),
                )
    return sorted(
        chains.values(),
        key=lambda chain: (
            chain.general.word,
            chain.middle.word,
            chain.specific.word,
        ),
    )


def ancestor_names(synset_name: str) -> set[str]:
    synset = wn.synset(synset_name)
    return {
        ancestor.name() for ancestor in synset.closure(lambda item: item.hypernyms())
    }


def choose_decoy(chain: Chain, pool: list[Concept], rng: random.Random) -> Concept:
    forbidden = {chain.general.word, chain.middle.word, chain.specific.word}
    ancestors = ancestor_names(chain.specific.synset)
    candidates = [
        concept
        for concept in pool
        if concept.word not in forbidden
        and concept.synset not in ancestors
        and concept.synset != chain.specific.synset
    ]
    if not candidates:
        raise RuntimeError("The WordNet vocabulary has no negative-control decoy.")
    return rng.choice(candidates)


def statement(antecedent: str, consequent: str) -> str:
    return (
        f'If something has the label "{antecedent}", '
        f'then it has the label "{consequent}"'
    )


def build_prompt(chain: Chain, conclusion: str) -> str:
    first = statement(chain.specific.word, chain.middle.word)
    second = statement(chain.middle.word, chain.general.word)
    final = statement(chain.specific.word, conclusion)
    return f"From '{first}' together with '{second}', can we infer '{final}'?"


def generate_cases(
    count: int, seed: int, min_frequency: int
) -> tuple[list[list[str | int]], list[dict[str, object]]]:
    if count < 1:
        raise ValueError("--count must be greater than zero.")
    if min_frequency < 1:
        raise ValueError("--min-frequency must be greater than zero.")

    chains = build_chains(min_frequency)
    if count > len(chains):
        raise ValueError(
            f"WordNet has only {len(chains)} usable chains; cannot create {count}."
        )

    rng = random.Random(seed)
    selected = rng.sample(chains, count)
    valid_count = (count + 1) // 2
    expected_answers = ["yes"] * valid_count + ["no"] * (count - valid_count)
    rng.shuffle(expected_answers)
    decoy_pool = sorted(
        {chain.general for chain in chains},
        key=lambda concept: (concept.word, concept.synset),
    )

    prompts: list[list[str | int]] = []
    labels: list[dict[str, object]] = []
    for case_id, (chain, expected_answer) in enumerate(
        zip(selected, expected_answers, strict=True),
        start=1,
    ):
        decoy = None
        conclusion = chain.general.word
        if expected_answer == "no":
            decoy = choose_decoy(chain, decoy_pool, rng)
            conclusion = decoy.word

        prompts.append(["HS", case_id, build_prompt(chain, conclusion)])
        labels.append(
            {
                "id": case_id,
                "expected_answer": expected_answer,
                "condition": "valid" if expected_answer == "yes" else "invalid",
                "general": chain.general.word,
                "middle": chain.middle.word,
                "specific": chain.specific.word,
                "decoy": decoy.word if decoy else None,
                "synsets": {
                    "general": chain.general.synset,
                    "middle": chain.middle.synset,
                    "specific": chain.specific.synset,
                },
            }
        )
    return prompts, labels


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=4) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    args = parse_args()
    ensure_nltk_data(args.download_nltk_data)
    prompts, labels = generate_cases(args.count, args.seed, args.min_frequency)

    output_path = project_path(args.output)
    labels_path = project_path(args.labels_output)
    write_json(output_path, prompts)
    write_json(
        labels_path,
        {
            "dataset": "HS_NLTK",
            "source": "NLTK WordNet",
            "nltk_version": nltk.__version__,
            "seed": args.seed,
            "min_frequency": args.min_frequency,
            "corpora": ["brown", "wordnet"],
            "count": len(prompts),
            "valid_count": sum(label["expected_answer"] == "yes" for label in labels),
            "invalid_count": sum(label["expected_answer"] == "no" for label in labels),
            "cases": labels,
        },
    )
    print(f"Generated {len(prompts)} cases.")
    print(f"Prompts: {output_path}")
    print(f"Labels: {labels_path}")


if __name__ == "__main__":
    main()
