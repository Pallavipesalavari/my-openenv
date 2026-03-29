"""
Inference Script: IAM Privilege Reducer
===================================
MANDATORY
- Before submitting, ensure the following variables are defined in your environment configuration:
  API_BASE_URL   The API endpoint for the LLM.
  MODEL_NAME     The model identifier to use for inference.
  HF_TOKEN       Your Hugging Face / API key.
  
- The inference script must be named `inference.py` and placed in the root directory.
"""

import os
import re
import json
import textwrap
from typing import List
from openai import OpenAI

# Required Environment Variables
API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
API_KEY = os.getenv("HF_TOKEN") or os.getenv("API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "meta-llama/Llama-3-70b-chat-hf") # Default fallback
MAX_STEPS = 5 
TEMPERATURE = 0.2
MAX_TOKENS = 1500

# Persona for the LLM
SYSTEM_PROMPT = textwrap.dedent(
    """
    You are an expert AWS Cloud Security Engineer. 
    Your task is to analyze an overly permissive IAM JSON policy and a set of access logs, 
    then rewrite the IAM policy applying the Principle of Least Privilege.
    
    RULES:
    1. You must output VALID JSON.
    2. Deny unauthorized actions discovered in the logs.
    3. Allow actions that are required for normal system operation.
    4. Do not include markdown formatting or explanations outside of the JSON block.
    """
).strip()

def build_user_prompt(step: int, observation: dict, history: List[str]) -> str:
    current_policy = observation.get("current_policy", {})
    access_logs = observation.get("access_logs", [])
    goal = observation.get("goal", "Reduce privileges without breaking required access.")
    
    prompt = textwrap.dedent(
        f"""
        Step: {step}
        Goal: {goal}
        
        CURRENT IAM POLICY:
        {json.dumps(current_policy, indent=2)}
        
        RECENT ACCESS LOGS:
        {json.dumps(access_logs, indent=2)}
        
        Previous steps history: {history[-2:] if history else "None"}
        
        Please provide the completely rewritten, securely scoped IAM JSON policy.
        """
    ).strip()
    return prompt

def extract_json_from_response(response_text: str) -> str:
    """Extracts JSON block if the model wraps it in markdown."""
    match = re.search(r'
http://googleusercontent.com/immersive_entry_chip/0

### Quick reminder on how to add this:
1. Go to `https://huggingface.co/spaces/PALLAVIPESALAVARI/iam-privilege-reducer/tree/main`
2. Click **+ Add file** -> **Create new file**.
3. Name it exactly **`inference.py`**
4. Paste the code above into the box.
5. Click **Commit new file to `main`**.
