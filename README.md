# OpenEnv: IAM Privilege Reducer

## Description & Motivation
Cloud infrastructure is frequently plagued by overly permissive IAM roles, leading to severe security vulnerabilities. This environment simulates a genuine DevSecOps task: auditing AWS-style IAM policies against historical access logs to enforce the Principle of Least Privilege. Agents must cleanly remove unused permissions without breaking legitimate workflows.

## Spaces
* **Observation Space:** Contains the `current_policies` (JSON) and `access_logs` (List of dictionaries showing active workflows).
* **Action Space:** Requires a `role_name`, the `updated_policy` (JSON), and a `justification` string.
* **Reward Space:** Dense reward between `0.0` and `1.0`. Evaluated by counting unnecessary permissions safely removed, with massive penalties (score = 0.0) if a legitimate workflow is broken.

## Tasks
1. **Easy:** Remove a broad `"*"` wildcard and replace it with specific read actions found in logs.
2. **Medium:** Clean up a multi-service developer policy by removing entire unused service blocks.
3. **Hard:** Perform granular cleanup on a backend service policy, removing specific unused actions (e.g., `sqs:ReceiveMessage`) while preserving required ones (`sqs:SendMessage`).

## Setup & Usage
1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`
3. Export your OpenAI key: `export OPENAI_API_KEY="your-key-here"`
4. Run the baseline: `python baseline.py`
5. Start the server: `uvicorn app:app --reload`

## Baseline Scores
Using `gpt-4o-mini` via the `baseline.py` script:
* Easy: 1.0
* Medium: 1.0
* Hard: 1.0
