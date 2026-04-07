"""
Inference Script: IAM Privilege Reducer (SAFE VERSION)
"""

import os
import re
import json
import textwrap
from typing import List, Dict, Any

# Try importing OpenAI safely
try:
    from openai import OpenAI
except Exception:
    OpenAI = None

# Environment Variables
API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
API_KEY = os.getenv("HF_TOKEN") or os.getenv("API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "meta-llama/Llama-3-70b-chat-hf")

MAX_STEPS = 3
TEMPERATURE = 0.2
MAX_TOKENS = 1000

# Initialize client safely
client = None
if OpenAI and API_KEY:
    try:
        client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)
    except Exception:
        client = None

# System Prompt
SYSTEM_PROMPT = """You are an AWS security expert.
Return ONLY valid IAM JSON policy.
No explanations."""


def build_user_prompt(step: int, observation: Dict[str, Any], history: List[str]) -> str:
    try:
        return textwrap.dedent(f"""
        Step: {step}
        Goal: {observation.get("goal", "")}
        CURRENT POLICY:
        {json.dumps(observation.get("current_policy", {}), indent=2)}
        ACCESS LOGS:
        {json.dumps(observation.get("access_logs", []), indent=2)}
        HISTORY:
        {history[-2:] if history else "None"}
        Rewrite secure IAM policy JSON.
        """)
    except Exception:
        return "Return valid JSON policy."


def extract_json(text: str) -> str:
    try:
        match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
        if match:
            return match.group(1)

        match = re.search(r"(\{.*\})", text, re.DOTALL)
        if match:
            return match.group(1)

        return "{}"
    except Exception:
        return "{}"


def call_llm(system: str, user: str) -> str:
    try:
        if not client:
            return "{}"

        response = client.chat.completions.create(
            model=MODEL_NAME,
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user}
            ],
        )

        return response.choices[0].message.content or "{}"

    except Exception:
        return "{}"


def run_inference(observation: Dict[str, Any]) -> Dict[str, Any]:
    history = []

    for step in range(1, MAX_STEPS + 1):
        try:
            prompt = build_user_prompt(step, observation, history)
            raw = call_llm(SYSTEM_PROMPT, prompt)
            cleaned = extract_json(raw)

            try:
                parsed = json.loads(cleaned)
                if isinstance(parsed, dict):
                    return parsed
            except Exception:
                history.append(cleaned)

        except Exception as e:
            history.append(str(e))

    return {
        "Version": "2012-10-17",
        "Statement": []
    }


def inference(observation: Dict[str, Any]) -> Dict[str, Any]:
    try:
        result = run_inference(observation)

        if not isinstance(result, dict):
            return {"error": "Invalid output format"}

        return result

    except Exception as e:
        return {
            "error": "Unhandled exception",
            "message": str(e)
        }


# ✅ Local test block (safe to keep)
if __name__ == "__main__":
    sample_input = {
        "current_policy": {},
        "access_logs": []
    }
    print(json.dumps(inference(sample_input), indent=2))
