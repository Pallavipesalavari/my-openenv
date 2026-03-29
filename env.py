import copy
from typing import Tuple, Dict, Any
from models import IAMObservation, IAMAction, IAMReward
from tasks import TASKS

class IAMPrivilegeEnv:
    def __init__(self, task_level: str = "easy"):
        if task_level not in TASKS:
            raise ValueError(f"Task {task_level} not found.")
        self.task_level = task_level
        self.reset()

    def reset(self) -> IAMObservation:
        self.state = copy.deepcopy(TASKS[self.task_level])
        self.current_policy = self.state["initial_policy"]
        self.logs = self.state["logs"]
        self.done = False
        self.last_reward = IAMReward(score=0.0, permissions_removed=0, workflows_broken=0)
        
        return IAMObservation(
            current_policies=self.current_policy,
            access_logs=self.logs,
            feedback="Environment initialized. Remove unnecessary permissions without breaking logged workflows."
        )

    def state_dict(self) -> Dict[str, Any]:
        return {
            "task_level": self.task_level,
            "current_policy": self.current_policy,
            "done": self.done
        }

    def step(self, action: IAMAction) -> Tuple[IAMObservation, IAMReward, bool, Dict[str, Any]]:
        if self.done:
            return IAMObservation(current_policies=self.current_policy, access_logs=self.logs, feedback="Episode finished."), self.last_reward, True, {}

        self.current_policy = action.updated_policy
        
        # --- DETERMINISTIC GRADER ---
        required = set(self.state["required_actions"])
        forbidden = set(self.state["forbidden_actions"])
        
        # Flatten the actions in the new policy
        new_actions = []
        for statement in self.current_policy.get("Statement", []):
            acts = statement.get("Action", [])
            if isinstance(acts, list):
                new_actions.extend(acts)
            else:
                new_actions.append(acts)
        
        new_actions_set = set(new_actions)
        
        workflows_broken = len(required - new_actions_set)
        permissions_removed = len(forbidden - new_actions_set)
        total_forbidden = len(forbidden)

        if workflows_broken > 0:
            score = 0.0
            feedback = f"Failed: You broke {workflows_broken} legitimate workflows."
        elif permissions_removed == total_forbidden:
            score = 1.0
            feedback = "Success: Perfect least-privilege policy achieved."
        elif permissions_removed > 0:
            score = permissions_removed / total_forbidden
            feedback = "Partial Success: Some unnecessary permissions removed, but not all."
        else:
            score = 0.0
            feedback = "Failed: No unnecessary permissions were removed."

        self.done = True
        self.last_reward = IAMReward(
            score=score, 
            permissions_removed=permissions_removed, 
            workflows_broken=workflows_broken
        )
        
        obs = IAMObservation(
            current_policies=self.current_policy,
            access_logs=self.logs,
            feedback=feedback
        )
        
        return obs, self.last_reward, self.done, {"justification": action.justification}
