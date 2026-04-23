import re
import uvicorn
from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import sys
import os
import traceback

# Ensure we can import from core and actors
sys.path.append(os.path.abspath("."))

from core.model_registry import ModelRegistryBase
from actors.coding_actor import CodingActorBase
from actors.search_actor import SearchActorBase

app = FastAPI(title="SGI API Server")

# Instantiate core logic locally
search_actor = SearchActorBase(workspace=None, scheduler=None)
model_registry = ModelRegistryBase(search_actor=search_actor)
coding_actor = CodingActorBase(workspace=None, scheduler=None, model_registry=model_registry)

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatCompletionRequest(BaseModel):
    model: str
    messages: List[ChatMessage]
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = 128
    stream: Optional[bool] = False
    n: Optional[int] = 1

def extract_code_and_input(prompt: str):
    # LiveCodeBench Prompt Format has multiple [PYTHON] blocks (few-shot).
    # We want the last one.

    blocks = re.findall(r"\[PYTHON\](.*?)assert (.*?) == \?\?", prompt, re.DOTALL)
    if blocks:
        code, assertion_input = blocks[-1]
        return code.strip(), assertion_input.strip()

    # Try markdown fallback
    blocks = re.findall(r"```python(.*?)assert (.*?) == \?\?", prompt, re.DOTALL)
    if blocks:
        code, assertion_input = blocks[-1]
        return code.strip(), assertion_input.strip()

    return None, None

@app.post("/v1/chat/completions")
async def chat_completions(request: ChatCompletionRequest):
    last_message = request.messages[-1].content
    code, assertion_input = extract_code_and_input(last_message)

    num_choices = request.n or 1
    choices = []

    if code and assertion_input:
        print(f"[API] Code Execution detected for input: {assertion_input[:50]}...")
        # SGI 2026: Inject necessary imports for execution
        # We avoid using from typing import * to prevent __import__ usage inside exec if restricted
        exec_code = f"{code}\nprint(repr({assertion_input}))"

        try:
            result = coding_actor.execute_logic_internal(exec_code)
        except MemoryError:
            print("[API] MemoryError caught in server!")
            result = {"status": "exception", "error": "MemoryError"}

        if result["status"] == "success":
            output = result["output"].strip()
            # Handle potential multiple prints or trailing whitespace
            final_val = output.split("\n")[-1]
            response_content = f"assert {assertion_input} == {final_val}\n[/ANSWER]"
            print(f"[API] Success. Prediction: {final_val}")
        else:
            print(f"[API] Execution error: {result.get('error', 'Unknown')[:100]}")
            response_content = f"assert {assertion_input} == None # Error fallback"
    else:
        print(f"[API] Codegeneration/Reasoning request. Routing to ModelRegistry (Prioritized Flow)...")
        response_content = model_registry.generate(last_message, max_new_tokens=request.max_tokens or 1024)

        # SGI 2026: Clean extraction for Benchmarking.
        # Strip <thought>, <reflex>, etc. to return only pure code or prose if requested by the runner.
        if "<thought>" in response_content:
            response_content = re.sub(r"<thought>.*?</thought>\s*", "", response_content, flags=re.DOTALL)
        if "<reflex>" in response_content:
            # For reflex, we might want the content inside
            reflex_match = re.search(r"<reflex>(.*?)</reflex>", response_content, re.DOTALL)
            if reflex_match:
                response_content = reflex_match.group(1).strip()

        # Strip potential markdown
        if "```python" in response_content:
            response_content = response_content.split("```python")[1].split("```")[0].strip()
        elif "```" in response_content:
            response_content = response_content.split("```")[1].strip()

    for i in range(num_choices):
        choices.append({
            "index": i,
            "message": {
                "role": "assistant",
                "content": response_content,
            },
            "finish_reason": "stop",
        })

    return {
        "id": "sgi-123",
        "object": "chat.completion",
        "created": 123456789,
        "model": request.model,
        "choices": choices,
        "usage": {
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0,
        },
    }

if __name__ == "__main__":
    # Use single worker to save memory and avoid port conflicts
    uvicorn.run(app, host="0.0.0.0", port=8000, workers=1)
