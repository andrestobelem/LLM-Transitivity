import json
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

PROJECT_ROOT = Path(__file__).resolve().parent
SYSTEM_PROMPTS_DIR = PROJECT_ROOT / "prompts" / "systemPrompts"
USER_PROMPTS_DIR = PROJECT_ROOT / "prompts" / "userPrompts"
DATA_DIR = PROJECT_ROOT / "data"

SYSTEM_PROMPT_FILES = {
    "zeroShot": SYSTEM_PROMPTS_DIR / "zeroShot.json",
    "chainOfThought": SYSTEM_PROMPTS_DIR / "chainOfThought.json",
}

USER_PROMPT_FILES = {
    "HS": USER_PROMPTS_DIR / "HS.json",
}


def load_system_prompt(name: str) -> str:
    path = SYSTEM_PROMPT_FILES[name]
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    return data["system_prompt"]

    # def load_user_prompts(name: str) -> str:
    #     path = SYSTEM_PROMPT_FILES[name]
    #     data = json.loads(path.read_text(encoding="utf-8-sig"))
    #     prompts = []
    #     for entry in data:
    #         category, prompt_id, text = entry[0], entry[1], entry[2]
    #         prompts.append({"category": category, "id": prompt_id, "text": text})
    #     return prompts


def main() -> None:
    load_dotenv()

    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("Set OPENROUTER_API_KEY before running this script.")

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    with open(USER_PROMPTS_DIR / "HS.json") as file:
        promts = json.load(file)

    client = OpenAI(
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1",
        timeout=60.0,
    )
    system_prompt = load_system_prompt("zeroShot")

    for prompt in promts:
        response = client.chat.completions.create(
            model="openai/gpt-5.4-mini",
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": prompt[2],
                },
            ],
            max_completion_tokens=300,
        )

        if not response.choices:
            raise RuntimeError(
                f"OpenRouter returned no choices for prompt {prompt[1]}."
            )

        answer = response.choices[0].message.content
        if not answer:
            raise RuntimeError(
                f"OpenRouter returned empty content for prompt {prompt[1]}."
            )

        print(answer)

        data = {
            "user_prompt": prompt[2],
            "system_prompt": system_prompt,
            "model": "openai/gpt-5.4-mini",
            "responses": answer,
        }

        out_file = DATA_DIR / f"{prompt[1]}_{prompt[0]}.json"
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        if response.usage:
            print(
                f"\nTokens used - Input: {response.usage.prompt_tokens}, "
                f"Output: {response.usage.completion_tokens}, "
                f"Total: {response.usage.total_tokens}"
            )


if __name__ == "__main__":
    main()
