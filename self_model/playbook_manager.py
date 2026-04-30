import ray
import os
import json
import time
from core.base import CognitiveModule

@ray.remote
class PlaybookManager(CognitiveModule):
    """
    SGI 2026: Agentic Context Engineering (ACE).
    Maintains an evolving playbook of instructions that learns from failure patterns.
    """
    def __init__(self, workspace=None, scheduler=None, model_registry=None, playbook_path="./data/sgi_playbook.json"):
        super().__init__(workspace, scheduler, model_registry)
        self.playbook_path = playbook_path
        os.makedirs(os.path.dirname(self.playbook_path), exist_ok=True)
        self.playbook = self._load_playbook()

    def _load_playbook(self):
        if os.path.exists(self.playbook_path):
            try:
                with open(self.playbook_path, "r") as f:
                    return json.load(f)
            except Exception:
                pass
        return {
            "global_instructions": "Always prioritize MDL efficiency. Use formal verification for critical logic.",
            "failure_patterns": {}, # Pattern -> Correction
            "version": 1.0,
            "last_updated": time.time()
        }

    def _save_playbook(self):
        try:
            with open(self.playbook_path, "w") as f:
                json.dump(self.playbook, f, indent=2)
        except Exception as e:
            print(f"🚨 [PlaybookManager] Failed to save playbook: {e}")

    def learn_from_failure(self, task, implementation, critique):
        """
        ACE Stage: Treats the prompt as an evolving playbook.
        Updates instructions based on Reflector feedback.
        """
        print(f"[PlaybookManager] ACE: Learning from failure for task: {task[:30]}...")

        if self.model_registry:
            prompt = (
                f"Analyze this failure and update the SGI-Alpha Playbook to avoid similar mistakes.\n"
                f"Task: {task}\n"
                f"Failed Implementation: {implementation}\n"
                f"Reflector Critique: {critique}\n\n"
                f"Current Playbook: {json.dumps(self.playbook)}\n\n"
                f"Return a JSON object with the new 'global_instructions' and an entry for 'failure_patterns'."
            )
            try:
                result = ray.get(self.model_registry.generate.remote(prompt))
                # Simulated extraction of JSON
                new_instruction = "Avoid bare except blocks and prioritize vectorized operations for data processing."
                self.playbook["global_instructions"] += f" {new_instruction}"
                self.playbook["failure_patterns"][task[:50]] = critique[:100]
                self.playbook["version"] += 0.1
                self.playbook["last_updated"] = time.time()
                self._save_playbook()
                print(f"[PlaybookManager] Playbook evolved to version {self.playbook['version']:.1f}")
            except Exception as e:
                print(f"[PlaybookManager] ACE learning failed: {e}")

    def get_playbook_context(self):
        return f"SGI-Alpha Playbook (v{self.playbook['version']}): {self.playbook['global_instructions']}"

    def receive(self, message):
        if super().receive(message): return True
        if message["type"] == "failure_report":
            data = message["data"]
            self.learn_from_failure(data["task"], data["implementation"], data["critique"])
        elif message["type"] == "get_playbook":
            self.send_result("playbook_context", self.get_playbook_context())
