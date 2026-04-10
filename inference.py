import os
import json
import re
from typing import Dict, Any

# ✅ Safe OpenAI import
try:
    from openai import OpenAI
except Exception:
    OpenAI = None

from env import IAMPrivilegeEnv
from models import IAMAction

# Initialize environment
env = IAMPrivilegeEnv()


API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "meta-llama/Llama-3-70b-chat-hf")
HF_TOKEN = os.getenv("HF_TOKEN")

client = None
if OpenAI and HF_TOKEN:
    try:
        client = OpenAI(base_url=API_BASE_URL, api_key=HF_TOKEN)
    except Exception:
        client = None


def extract_json(text: str) -> Dict[str, Any]:
    try:
        match = re.search(r"(\{.*\})", text, re.DOTALL)
        if match:
            return json.loads(match.group(1))
    except Exception:
        pass
    return {}


def call_llm(prompt: str) -> Dict[str, Any]:
    if not client:
        return {}

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )
        return extract_json(response.choices[0].message.content)
    except Exception:
        return {}


def inference(observation: Dict[str, Any]) -> Dict[str, Any]:
    try:
        # ✅ Reset environment (important)
        obs = env.reset()

        # ✅ Simple deterministic logic (strong baseline)
        required_actions = [log["action"] for log in obs.access_logs]

        action_data = {
            "role_name": "AutoAgent",
            "updated_policy": {
                "RoleName": "AutoAgent",
                "Statement": [
                    {
                        "Effect": "Allow",
                        "Action": required_actions,
                        "Resource": "*"
                    }
                ]
            },
            "justification": "Keeping only required actions from logs"
        }

        action = IAMAction(**action_data)

        # ✅ CRITICAL: This enables grading
        obs, reward, done, info = env.step(action)

        return {
            "observation": obs.dict(),
            "reward": reward.score,
            "done": done,
            "info": info
        }

    except Exception as e:
        return {"error": str(e)}


# ✅ REQUIRED STDOUT FORMAT (MULTI-TASK)
if __name__ == "__main__":
    import sys

    tasks = ["easy", "medium", "hard"]

    for task in tasks:
        env = IAMPrivilegeEnv(task_level=task)

        sys.stdout.write(f"[START] task={task}\n")
        sys.stdout.flush()

        obs = env.reset()
        required_actions = [log["action"] for log in obs.access_logs]

        action = IAMAction(
            role_name="AutoAgent",
            updated_policy={
                "RoleName": "AutoAgent",
                "Statement": [
                    {"Effect": "Allow", "Action": required_actions, "Resource": "*"}
                ]
            },
            justification="Auto policy reduction"
        )

        obs, reward, done, info = env.step(action)

        sys.stdout.write(f"[STEP] step=1 reward={reward.score}\n")
        sys.stdout.flush()

        sys.stdout.write(f"[END] task={task} score={reward.score} steps=1\n")
        sys.stdout.flush()
