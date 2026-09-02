# LLM Transitivity

LLM Transitivity is a benchmark for hypothetical syllogism tasks. It tests if a
language model can infer `A -> C` from `A -> B` and `B -> C`.

The prompts use different subjects. Some statements agree with real-world
knowledge, and some statements do not. This variation helps identify when a
model uses semantic plausibility instead of the stated logical form.

## Repository structure

- `prompts/systemPrompts/` contains system prompts for each test method.
- `prompts/userPrompts/HS.json` contains the hypothetical syllogism cases.
- `runBenchmark.py` sends each case to the model through OpenRouter.
- `data/` contains one JSON result file for each completed case.
- `docs/` contains project documentation.

Each prompt entry has this format:

```json
["HS", 1, "Question text"]
```

The fields are the task category, the case ID, and the question.

## Setup

Create and activate a Python virtual environment. Then install the two runtime
dependencies:

```shell
python -m pip install openai python-dotenv
```

Create a `.env` file in the repository root:

```dotenv
OPENROUTER_API_KEY=your-api-key
```

The `.gitignore` file excludes `.env` from version control.

## Run the benchmark

Run this command from the repository root:

```shell
python runBenchmark.py
```

The runner processes all entries in `prompts/userPrompts/HS.json`. It prints
each response and its token usage. It writes each response to
`data/<case-id>_HS.json`.

The current runner uses these fixed settings:

- Model: `openai/gpt-5.4-mini`
- System prompt: `zeroShot`
- Maximum completion tokens: `300`

A new run replaces any result file that has the same case ID.

## Documentation

See the [documentation index](docs/README.md) for detailed project documents.

## Current limitations

- The prompt data does not include expected answers.
- The runner does not calculate accuracy.
- The model and system prompt are not command-line options.
- The runner does not retry failed requests.
- Existing result files cover only part of the prompt data.

## Contributors

- Pablo Vazquez Soldano
- Lourdes De Carolis
- Tomas Gomez Ansede
- Guadalupe Fernández Fagioli
- Nadia Belén Martínez Szego
- Sofia de Arias Vargas
- Lourdes Nazarena Toneatti
