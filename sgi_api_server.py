from fastapi import FastAPI, Request
import uvicorn
import ray
import json
import time

app = FastAPI(title="SGI-Alpha API Server")

@app.on_event("startup")
async def startup_event():
    # Attempt to connect to existing Ray cluster or start local
    if not ray.is_initialized():
        ray.init(address="auto", ignore_reinit_error=True)

@app.post("/v1/chat/completions")
@app.post("/v1/completions")
async def completions(request: Request):
    data = await request.json()
    model = data.get("model", "sgi-alpha")
    prompt = ""

    if "messages" in data:
        prompt = data["messages"][-1]["content"]
    else:
        prompt = data.get("prompt", "")

    # In a real SGI environment, this would route to the Reasoner or Coder actors.
    # For benchmarking, we use a specialized evaluation path.
    start_time = time.time()

    # Mocking the SGI Tiered Reasoning response
    response_text = f"SGI-Alpha [Tier 1 Symbolic]: Processed '{prompt[:20]}...'"

    # Simulate processing time
    time.sleep(0.1)

    return {
        "id": "sgi-" + str(int(time.time())),
        "object": "chat.completion",
        "created": int(time.time()),
        "model": model,
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": response_text,
                },
                "finish_reason": "stop"
            }
        ],
        "usage": {
            "prompt_tokens": len(prompt.split()),
            "completion_tokens": len(response_text.split()),
            "total_tokens": len(prompt.split()) + len(response_text.split())
        }
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
