"""Fake LLM that mimics the OpenAI Chat Completions API.

Returns scripted responses so the gateway can be tested
without API costs and with deterministic results.
"""
import json
import time
import uuid

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Fake LLM")


class ChatRequest(BaseModel):
    model: str
    messages: list[dict]


# Keyword in the user message -> tool call the fake LLM "decides" to make.
# Order matters: more specific keywords first.
SCENARIOS = {
    "exportiere": {
        "name": "search_knowledge_base",
        "arguments": {"query": "*", "customer_id": "*", "limit": 10000},
    },
    "kunde": {
        "name": "search_knowledge_base",
        "arguments": {"query": "Kontoauszug", "customer_id": "4711"},
    },
}


def find_scenario(text: str) -> dict | None:
    text = text.lower()
    for keyword, tool_call in SCENARIOS.items():
        if keyword in text:
            return tool_call
    return None


@app.post("/v1/chat/completions")
def chat_completions(req: ChatRequest) -> dict:
    user_messages = [m for m in req.messages if m.get("role") == "user"]
    last_text = str(user_messages[-1].get("content", "")) if user_messages else ""

    scenario = find_scenario(last_text)

    if scenario:
        message = {
            "role": "assistant",
            "content": None,
            "tool_calls": [{
                "id": f"call_{uuid.uuid4().hex[:8]}",
                "type": "function",
                "function": {
                    "name": scenario["name"],
                    # OpenAI sends arguments as a JSON *string*, not a dict
                    "arguments": json.dumps(scenario["arguments"]),
                },
            }],
        }
        finish_reason = "tool_calls"
    else:
        message = {"role": "assistant", "content": "Fake-Antwort: Wie kann ich helfen?"}
        finish_reason = "stop"

    return {
        "id": f"chatcmpl-{uuid.uuid4().hex[:12]}",
        "object": "chat.completion",
        "created": int(time.time()),
        "model": req.model,
        "choices": [{"index": 0, "message": message, "finish_reason": finish_reason}],
        "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
    }