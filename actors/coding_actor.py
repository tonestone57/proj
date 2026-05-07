import contextlib
import io
import logging
import os
import ray
import re
import sys
from core.base import CognitiveModule
from core.config import CORES_CODING

# Standard SGI 2026 Logging
logger = logging.getLogger(__name__)

class CodingActorBase(CognitiveModule):
    def __init__(self, workspace, scheduler, model_registry=None, critic=None):
        super().__init__(workspace, scheduler, model_registry)
        self.critic = critic
        logger.info("Initialized. Using Shared Model Provider for coding tasks...")

    def set_critic(self, critic):
        self.critic = critic
        logger.info("Reflector (InternalCritic) integrated.")

    def receive(self, message):
        try:
            if super().receive(message): return True
            if message["type"] == "set_critic":
                self.set_critic(message["data"])
            elif message["type"] == "code_execution":
                data = message["data"]
                if isinstance(data, dict):
                    code = data.get("code", "")
                    mode = data.get("mode", message.get("mode", ""))
                else:
                    code = data
                    mode = message.get("mode", "")

                persistent = message.get("persistent", False)
                confidence = self.calculate_confidence_score()

                if confidence < 0.4:
                    snippet = str(code)[:50]
                    self.scheduler.submit.remote(None, {
                        "type": "search_request",
                        "data": f"Docs for: {snippet}",
                        "reason": "Low Confidence"
                    })

                if self.model_registry and "generate" in mode:
                    result = self.generate_and_verify(code)
                else:
                    result = self.execute_code(code, persistent=persistent)
                result["confidence"] = confidence

                self.send_result("code_result", result)
            elif message["type"] == "simulation_obs":
                # SGI 2026: Code-based response to simulation state
                obs = message["data"]
                logger.debug(f"Simulation Update: {obs}")
                if obs.get("load", 0) > 70:
                    self.send_result("simulation_action", {
                        "agent_id": "CodingActor",
                        "action": {"type": "resource_release", "amount": 20}
                    })
        except Exception as e:
            logger.error(f"Error in receive: {e}")

    def calculate_confidence_score(self):
        from core.drives import calculate_entropy
        state = ray.get(self.workspace.get_current_state.remote())
        entropy = calculate_entropy(state)
        return max(0.0, 1.0 - (entropy / 5.0))

    def detect_recursion(self, code):
        """
        Uses AST analysis to identify recursive function calls.
        """
        import ast
        try:
            tree = ast.parse(code)
        except SyntaxError:
            return []

        recursive_funcs = []
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                func_name = node.name
                is_recursive = False
                # SGI 2026: Determine the name of 'self' (usually 'self' or 'cls')
                self_names = {"self"}
                if node.args.args:
                    self_names.add(node.args.args[0].arg)

                for subnode in ast.walk(node):
                    if isinstance(subnode, ast.Call):
                        # Matches direct recursion: func()
                        if isinstance(subnode.func, ast.Name) and subnode.func.id == func_name:
                            is_recursive = True
                            break
                        # Matches method recursion: self.func() or cls.func()
                        elif isinstance(subnode.func, ast.Attribute) and subnode.func.attr == func_name:
                            if isinstance(subnode.func.value, ast.Name) and subnode.func.value.id in self_names:
                                is_recursive = True
                                break
                        # Matches function handle passed as argument
                        for arg in subnode.args:
                            if isinstance(arg, ast.Name) and arg.id == func_name:
                                is_recursive = True
                                break
                if is_recursive:
                    recursive_funcs.append(func_name)
        return recursive_funcs

    def iterative_transform(self, code, recursive_funcs=None):
        """
        SGI 2026: Neuro-Symbolic Refactoring.
        Converts detected recursion into stack-based loops using the Shared Model Registry.
        Optimized with SortedList for O(log N) state management if available.
        """
        if recursive_funcs is None:
            recursive_funcs = self.detect_recursion(code)

        if not recursive_funcs:
            return code

        logger.info(f"Iterative Transformation: Refactoring {recursive_funcs}...")

        # SGI 2026 Strategy: We use the Reasoning Brain (Tier 3) to perform the rewrite
        # while keeping the Symbolic logic intact.
        if self.model_registry:
            prompt = (
                f"Refactor the following Python code to convert recursive functions {recursive_funcs} "
                f"into iterative versions using explicit stacks (while loops). "
                f"This is to prevent RecursionError on large inputs. "
                f"Maintain exact functional parity. Return only the refactored code, without any explanations.\n\n"
                f"Original Code:\n{code}"
            )
            try:
                # Handle both Ray remote objects and local objects for testing
                if hasattr(self.model_registry.generate, "remote"):
                    transformed = ray.get(self.model_registry.generate.remote(prompt))
                else:
                    transformed = self.model_registry.generate(prompt)

                # SGI 2026: Clean extraction of refactored code
                # Strip thought blocks if present
                if "<thought>" in transformed:
                    transformed = re.sub(r"<thought>.*?</thought>\s*", "", transformed, flags=re.DOTALL)

                # Cleanup potential Markdown
                if "```python" in transformed:
                    transformed = transformed.split("```python")[1].split("```")[0].strip()
                elif "```" in transformed:
                    transformed = transformed.split("```")[1].strip()

                # SGI 2026: Validation - Ensure the transformed code is valid Python
                import ast
                try:
                    ast.parse(transformed)
                    return transformed
                except SyntaxError:
                    logger.warning(f"Refined code has syntax errors. Falling back to original.")
                    return code

            except Exception as e:
                logger.error(f"Refactoring failed: {e}")
                return code
        return code

    def DigitalTwin_Branching(self, branch_name):
        logger.info(f"Creating speculative branch: {branch_name}")
        return f"vm_branch_{branch_name}_0xdeadbeef"

    def execute_code(self, code, persistent=False):
        if persistent:
            from world_model.state import VMStateDigitalTwin
            twin = VMStateDigitalTwin(vm_id="speculative-01")
            twin.start()
            branch_id = self.DigitalTwin_Branching("speculative_run")
            twin.branch(branch_id)
        return self.execute_logic_internal(code)

    def generate_and_verify(self, code):
        """
        SGI 2026: Generates code, creates a Pytest suite, and self-corrects if tests fail.
        Upgraded to use InternalCritic (Reflector) for AI Feedback.
        """
        logger.info("Generating code and autonomous test suite...")
        generated_code = ray.get(self.model_registry.generate.remote(f"Code for: {code}"))

        if "LLM-Generated" in generated_code or "Mock response" in generated_code:
            generated_code = "def sample_func(): return True"

        # 1. Generate Test Suite
        test_suite = ray.get(self.model_registry.generate.remote(f"Generate pytest for: {generated_code}"))
        if "LLM-Generated" in test_suite or "Mock response" in test_suite:
            test_suite = "def test_sample(): from solution import sample_func; assert sample_func() == True"

        # 2. Verification Loop
        logger.info("Entering Reflector Loop...")
        test_passed = False
        retry_count = 0
        last_critique = ""
        score = 0.0

        while not test_passed and retry_count < 3:
            # Stage A: Execution Sandbox
            exec_result = self.execute_in_sandbox(generated_code, test_suite)

            # Stage B: AI Reflector (InternalCritic)
            critique_issues = []
            score = 1.0
            if self.critic:
                try:
                    critique_issues, score = ray.get(self.critic.critique_code.remote(generated_code, context=code))
                    logger.info(f"Reflector Score: {score:.2f}")
                except Exception as e:
                    logger.error(f"Reflector call failed: {e}")

            if exec_result["status"] == "success" and score > 0.8:
                logger.info(f"Verification successful. Score={score:.2f}")
                test_passed = True
                # Record as a potential "Skill" if it was high quality
                if score > 0.9:
                    self.send_result("skill_candidate", {
                        "task": code,
                        "implementation": generated_code,
                        "score": score
                    })
            else:
                exec_error = exec_result.get("error", "")
                critique_str = "\n".join(critique_issues)
                last_critique = f"Test Errors: {exec_error}\nReflector Issues: {critique_str}"

                # SGI 2026 ACE: Report failure to PlaybookManager if it persists
                if retry_count == 2:
                    self.send_result("failure_report", {
                        "task": code,
                        "implementation": generated_code,
                        "critique": last_critique
                    })

                logger.warning(f"Refinement needed (Attempt {retry_count + 1})...")
                refine_prompt = (
                    f"The previous implementation failed. Fix it based on this feedback:\n"
                    f"{last_critique}\n\nOriginal Task: {code}\nPrevious Code:\n{generated_code}"
                )
                generated_code = ray.get(self.model_registry.generate.remote(refine_prompt))
                if "LLM-Generated" in generated_code or "Mock response" in generated_code:
                    generated_code = "def sample_func(): return True"
                retry_count += 1

        return {
            "status": "success" if test_passed else "failed_verification",
            "output": generated_code,
            "verified": test_passed,
            "last_critique": last_critique if not test_passed else None,
            "score": score
        }

    def execute_in_sandbox(self, code, test_suite):
        """
        Executes code and tests in a temporary isolated environment.
        """
        import os
        import subprocess
        import tempfile

        with tempfile.TemporaryDirectory() as tmpdir:
            solution_path = os.path.join(tmpdir, "solution.py")
            test_path = os.path.join(tmpdir, "test_solution.py")

            with open(solution_path, "w") as f: f.write(code)
            with open(test_path, "w") as f: f.write(test_suite)

            try:
                # Run pytest on the temp files
                result = subprocess.run(
                    [sys.executable, "-m", "pytest", test_path],
                    cwd=tmpdir,
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                if result.returncode == 0:
                    return {"status": "success", "output": result.stdout}
                else:
                    return {"status": "failed", "error": result.stdout + result.stderr}
            except Exception as e:
                return {"status": "exception", "error": str(e)}

    def execute_logic_internal(self, code):
        """
        SGI 2026: Internal execution logic with proactive refactoring and isolated execution.
        """
        # SGI 2026: Proactive Recursive Refactoring
        recursive_funcs = self.detect_recursion(code)
        if recursive_funcs:
            code = self.iterative_transform(code, recursive_funcs=recursive_funcs)

        import subprocess
        import tempfile

        # Prepend standard SGI 2026 imports and resource limits
        imports = """
import os
import resource
import math

# SGI 2026: Resource limits applied within the script for safety
try:
    # Set 1GB memory limit (Address Space)
    limit_bytes = 1024 * 1024 * 1024
    resource.setrlimit(resource.RLIMIT_AS, (limit_bytes, limit_bytes))
    # Set 15s CPU time limit
    resource.setrlimit(resource.RLIMIT_CPU, (15, 15))
except Exception:
    pass
import collections
import heapq
import bisect
import itertools
import functools
import operator
import re
import typing
import numpy as np
import pandas as pd
import dataclasses
import string
import traceback
import gc
import sys

# Inject common names into global scope for convenience
from collections import deque, Counter, defaultdict, OrderedDict
from functools import cache, lru_cache
from itertools import accumulate, permutations, combinations, product, groupby, islice, chain, repeat
from math import inf, nan, comb, gcd, ceil, floor, sqrt
from typing import List, Dict, Tuple, Set, Optional, Union, Any, Callable, Iterable, Iterator, Generator

try:
    from sortedcontainers import SortedList, SortedDict, SortedSet
except ImportError:
    SortedList = SortedDict = SortedSet = None
"""
        full_code = imports + "\n" + code

        with tempfile.TemporaryDirectory() as tmpdir:
            script_path = os.path.join(tmpdir, "script.py")
            with open(script_path, "w") as f:
                f.write(full_code)

            try:
                # SGI 2026: Subprocess execution
                cmd = [sys.executable, script_path]

                # SGI 2026: Cross-platform safety. start_new_session is used for process group isolation.
                # Removed preexec_fn to avoid potential deadlocks in multi-threaded environments.
                # Resource limits are now handled within the script itself.
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=15,
                    start_new_session=(os.name != 'nt')
                )
                if result.returncode == 0:
                    return {"status": "success", "output": result.stdout}
                else:
                    return {"status": "failed", "error": result.stdout + result.stderr}
            except subprocess.TimeoutExpired:
                return {"status": "failed", "error": "Execution timed out (15s limit)"}
            except Exception as e:
                return {"status": "exception", "error": str(e)}

    def _execute_logic_internal_legacy(self, code):
        # Keeping this for reference or non-isolated needs
        stdout, stderr = io.StringIO(), io.StringIO()

        # SGI 2026: Inject high-performance libraries for Dynamic Programming, Graph Theory & Symbolic Reasoning
        import math
        import collections
        import heapq
        import bisect
        import itertools
        import functools
        import operator
        import re
        import typing
        import numpy as np
        import pandas as pd
        import dataclasses
        import string
        import traceback
        import gc
        import tracemalloc
        import threading
        try:
            import sortedcontainers
        except ImportError:
            sortedcontainers = None

        safe_globals = {
            "__builtins__": {
                "print": print, "range": range, "len": len, "int": int, "str": str,
                "dict": dict, "list": list, "set": set, "tuple": tuple, "bool": bool,
                "float": float, "abs": abs, "min": min, "max": max, "sum": sum,
                "sorted": sorted, "reversed": reversed, "enumerate": enumerate, "zip": zip,
                "any": any, "all": all, "map": map, "filter": filter, "round": round, "pow": pow,
                "repr": repr, "chr": chr, "ord": ord, "hex": hex, "bin": bin, "oct": oct
            },
            "math": math,
            "collections": collections,
            "heapq": heapq,
            "bisect": bisect,
            "itertools": itertools,
            "functools": functools,
            "operator": operator,
            "re": re,
            "typing": typing,
            "np": np,
            "pd": pd,
            "dataclasses": dataclasses,
            "string": string,
            "traceback": traceback,
            "gc": gc,
            "tracemalloc": tracemalloc,
            "threading": threading,
            # Direct Access for common DP/Graph tools
            "deque": collections.deque,
            "Counter": collections.Counter,
            "defaultdict": collections.defaultdict,
            "cache": functools.cache,
            "lru_cache": functools.lru_cache,
            "accumulate": itertools.accumulate,
            "comb": math.comb,
            "inf": float("inf"),
            "nan": float("nan"),
            "SortedList": sortedcontainers.SortedList if sortedcontainers else None,
            "SortedDict": sortedcontainers.SortedDict if sortedcontainers else None,
            "SortedSet": sortedcontainers.SortedSet if sortedcontainers else None,
            "dataclass": dataclasses.dataclass,
            "List": typing.List, "Dict": typing.Dict, "Tuple": typing.Tuple, "Set": typing.Set,
            "Optional": typing.Optional, "Union": typing.Union, "Any": typing.Any
        }

        try:
            # SGI 2026: Resource limits and stability (Unix only)
            try:
                import resource
                # Adjusted for sandbox: 1GB memory and 15s CPU
                #resource.setrlimit(resource.RLIMIT_AS, (1024 * 1024 * 1024, 1024 * 1024 * 1024))
                #resource.setrlimit(resource.RLIMIT_CPU, (15, 15))
            except (ImportError, Exception):
                pass

            # SGI 2026: Elevate recursion limit for deep symbolic reasoning/DP
            original_limit = sys.getrecursionlimit()
            sys.setrecursionlimit(10**6)

            with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                exec(code, safe_globals)

            sys.setrecursionlimit(original_limit)
            # SGI 2026: Forced GC after execution to maintain stability
            gc.collect()
            return {"status": "success", "output": stdout.getvalue()}
        except Exception:
            return {"status": "exception", "error": traceback.format_exc()}

@ray.remote(num_cpus=CORES_CODING)
class CodingActor(CodingActorBase):
    pass
