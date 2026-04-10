---

title: IAM Privilege Reducer
emoji: 🛡️
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
tags:

- openenv

---

🛡️ IAM Privilege Reducer

📌 Overview

IAM Privilege Reducer is a deterministic OpenEnv environment designed to train AI agents to enforce the Principle of Least Privilege in cloud IAM systems.

The agent analyzes:

- Current IAM policies
- Access logs

And learns to:
👉 Remove unnecessary permissions
👉 Preserve required functionality

---

🎯 Objective

The goal is to:

- Minimize over-permissioned roles
- Prevent security risks
- Maintain system functionality

---

⚙️ Environment Design

🔹 Observation

- Current IAM policy
- Access logs
- Feedback message

🔹 Action

- Updated IAM policy
- Justification

🔹 Reward

- ✅ Full score: Perfect least-privilege policy
- ⚠️ Partial score: Some permissions removed
- ❌ Zero: Broke required workflows

---

🔁 API Endpoints

Reset Environment

POST /reset

Take Action

POST /step

---

▶️ How to Run

Run Locally

pip install -r requirements.txt
uvicorn server.app:app --host 0.0.0.0 --port 7860

---

🧪 Example Flow

1. Call "/reset"
2. Receive observation
3. Send action to "/step"
4. Receive reward and updated state

---

🏆 Use Case

This environment simulates real-world cloud security scenarios where:

- Over-permissioned IAM roles are common
- Security engineers must enforce least privilege

---

🚀 Built For

Meta PyTorch OpenEnv Hackathon
Scaler School of Technology

---

👩‍💻 Team

Team Lead:
PESALAVARI PALLAVI

Team Member:
PESALAVARI VENKATA SAI MANOJ
