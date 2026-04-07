"""
Inference Script: IAM Privilege Reducer
"""

import os
import re
import json
import textwrap
from typing import List, Dict, Any
from openai import OpenAI

# Environment Variables
API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
API_KEY = os.getenv("HF_TOKEN") or os.getenv("API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "meta-llama/Llama-3-70b-chat-hf")

MAX_STEPS = 5
TEMPERATURE = 0.2
MAX_TOKENS = 1500

# OpenAI Client
client = OpenAI(
    base_url=API_BASE_URL,
    api_key=API_KEY
)

# System Prompt
SYSTEM_PROMPT = textwrap.dedent("""
You are an expert AWS Cloud Security Engineer. 
Your task is to analyze an overly permissive IAM JSON policy and access logs, 
then rewrite the IAM policy using the Principle of Least Privilege.

RULES:
1. Output ONLY valid JSON.
2. Deny unauthorized actions from logs.
3. Allow only required actions.
4. No explanations or markdown.
""").strip()


def build_user_prompt(step: int, observation: Dict[str, Any], history: List[str]) -> str:
    return textwrap.dedent(f"""
    Step: {step}
    Goal: {observation.get("goal", "")}

    CURRENT POLICY:
    {json.dumps(observation.get("current_policy", {}), indent=2)}

    ACCESS LOGS:
    {json.dumps(observation.get("access_logs", []), indent=2)}

    HISTORY:
    {history[-2:] if history else "None"}

    Rewrite secure IAM policy.
    """)


def extract_json_from_response(text: str) -> str:
    try:
        match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
        if match:
            return match.group(1)

        match = re.search(r"(\{.*\})", text, re.DOTALL)
        if match:
            return match.group(1)

        return text.strip()
    except Exception as e:
        return json.dumps({"error": str(e)})


def call_llm(system: str, user: str) -> str:
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user}
            ],
        )
        return response.choices[0].message.content
    except Exception as e:
        return json.dumps({"error": str(e)})


def run_inference(observation: Dict[str, Any]) -> Dict[str, Any]:
    history = []

    for step in range(1, MAX_STEPS + 1):
        user_prompt = build_user_prompt(step, observation, history)
        raw = call_llm(SYSTEM_PROMPT, user_prompt)
        cleaned = extract_json_from_response(raw)

        try:
            parsed = json.loads(cleaned)
            return parsed
        except:
            history.append(cleaned)

    return {"error": "Failed to generate valid policy", "history": history}


def inference(observation: Dict[str, Any]) -> Dict[str, Any]:
    return run_inference(observation)
