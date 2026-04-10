from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Any
import uvicorn
import sys

# Fix import path (important in Docker)
sys.path.append(".")

from env import IAMPrivilegeEnv
from models import IAMAction

app = FastAPI()

env = IAMPrivilegeEnv()


class StepInput(BaseModel):
    action: Dict[str, Any]


@app.get("/")
def home():
    return {"message": "IAM Privilege Reducer API running"}


@app.post("/reset")
def reset():
    obs = env.reset()
    return obs.dict()


@app.post("/step")
def step(data: StepInput):
    action = IAMAction(**data.action)
    obs, reward, done, info = env.step(action)

    return {
        "observation": obs.dict(),
        "reward": reward.score,
        "done": done,
        "info": info
    }


# ✅ REQUIRED for OpenEnv
def main():
    uvicorn.run(app, host="0.0.0.0", port=7860)


# ✅ REQUIRED entrypoint
if __name__ == "__main__":
    main()
