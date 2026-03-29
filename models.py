from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class IAMObservation(BaseModel):
    current_policies: Dict[str, Any]
    access_logs: List[Dict[str, str]]
    feedback: str = ""

class IAMAction(BaseModel):
    # Adding 'Optional' and default values prevents the 422 error
    role_name: Optional[str] = "default-role"
    updated_policy: Optional[Dict[str, Any]] = None 
    justification: Optional[str] = "No justification provided."

class IAMReward(BaseModel):
    score: float
    permissions_removed: int
    workflows_broken: int