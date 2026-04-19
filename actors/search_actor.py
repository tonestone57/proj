import re
import ray
from core.base import CognitiveModule
try:
    from ipex_llm.transformers import AutoModelForCausalLM
except ImportError:
    AutoModelForCausalLM = None
from core.config import CORES_SEARCH

class LicenseActor:
    def __init__(self):
        self.prohibited_patterns = [
            re.compile(r"GNU\s+General\s+Public\s+License", re.IGNORECASE),
            re.compile(r"GPLv[123]", re.IGNORECASE),
            re.compile(r"LGPL\s*[0-9\.]*", re.IGNORECASE),
            re.compile(r"Lesser\s+General\s+Public\s+License", re.IGNORECASE),
            re.compile(r"COPYING(?:\.txt|\.md)?", re.IGNORECASE),
            re.compile(r"licensed\s+under\s+the\s+GPL", re.IGNORECASE),
            re.compile(r"Free\s+Software\s+Foundation", re.IGNORECASE),
            re.compile(r"vulnerability\s+to\s+viral\s+licensing", re.IGNORECASE),
            re.compile(r"Affero\s+General\s+Public\s+License", re.IGNORECASE),
            re.compile(r"AGPLv[123]", re.IGNORECASE),
            re.compile(r"license\s+is\s+viral", re.IGNORECASE),
            re.compile(r"strictly\s+prohibited\s+without\s+FSF\s+approval", re.IGNORECASE),
        ]
    def is_compliant(self, content):
        for pattern in self.prohibited_patterns:
            if pattern.search(content): return False
        return True

@ray.remote(num_cpus=CORES_SEARCH)
class SearchActor(CognitiveModule):
    def __init__(self, workspace, scheduler, model_id="intel/neural-chat-14b-v3-3"):
        super().__init__(workspace, scheduler)
        self.license_actor = LicenseActor()
        print(f"[SearchActor] Loading {model_id} in NF4 precision for search distillation...")
        try:
            if AutoModelForCausalLM:
                self.model = AutoModelForCausalLM.from_pretrained(model_id, load_in_low_bit="nf4", trust_remote_code=True, use_cache=True)
            else: self.model = None
        except Exception as e:
            print(f"[SearchActor] Error loading model: {e}. Using mock model.")
            self.model = None

    def receive(self, message):
        if message["type"] == "search_request":
            query = message["data"]
            results = self.perform_search(query)
            compliant_results = [res for res in results if self.license_actor.is_compliant(res)]
            actionable_spec = self.distill_results(compliant_results)
            res_obj = {"type": "search_result", "data": compliant_results, "actionable_spec": actionable_spec, "sender": "SearchActor"}
            self.workspace.broadcast.remote(res_obj)
            return res_obj
        return None

    def perform_search(self, query):
        return [f"Documentation for {query}: Permissive MIT license.", f"Technical spec for {query}: Apache 2.0."]

    def distill_results(self, results):
        spec = "Synthesized Actionable Spec:\n"
        for i, res in enumerate(results): spec += f"- Spec {i+1}: {res[:50]}...\n"
        return spec
