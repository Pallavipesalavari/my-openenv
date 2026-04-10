from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, field_validator


class IAMObservation(BaseModel):
    current_policies: Dict[str, Any]
    access_logs: List[Dict[str, str]]
    feedback: str = ""


class IAMAction(BaseModel):
    role_name: Optional[str] = "default-role"
    updated_policy: Optional[Dict[str, Any]] = None
    justification: Optional[str] = "No justification provided."

    # ✅ VALIDATION (prevents runtime crash)
    @field_validator("updated_policy")
    @classmethod
    def validate_policy(cls, v):
        if v is None:
            return v

        if not isinstance(v, dict):
            raise ValueError("updated_policy must be a dictionary")

        # Ensure basic IAM structure exists
        if "Statement" not in v:
            raise ValueError("Policy must contain 'Statement' field")

        return v


class IAMReward(BaseModel):
    score: float
    permissions_removed: int
    workflows_broken: int
