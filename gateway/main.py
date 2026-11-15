"""Spiderweb Gateway: sits between AI clients and the LLM API."""
import json
import os

import httpx
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from gateway.events import log_event

UPSTREAM_URL = os.getenv("UPSTREAM_URL", "http://localhost:9000")
UPSTREAM_API_KEY = os.getenv("UPSTREAM_API_KEY", "fake-key")

app = FastAPI(title="Spiderweb Gateway")


def extract_tool_calls(response_body: dict) -> list[dict]:
    """Return tool calls from an LLM response with arguments parsed to dicts."""
    choices = response_body.get("choices") or [{}]
    message = choices[0].get("message", {})
    tool_calls = []
    for call in message.get("tool_calls") or []:
        function = call.get("function", {})
        raw_args = function.get("arguments") or "{}"
        try:
            arguments = json.loads(raw_args)
        except json.JSONDecodeError:
            arguments = {"_unparseable": raw_args}
        tool_calls.append({"name": function.get("name"), "arguments": arguments})
    return tool_calls


@app.post("/v1/chat/completions")
async def chat_completions(request: Request) -> JSONResponse:
    body = await request.json()

    async with httpx.AsyncClient(timeout=60) as client:
        upstream = await client.post(
            f"{UPSTREAM_URL}/v1/chat/completions",
            json=body,
            headers={"Authorization": f"Bearer {UPSTREAM_API_KEY}"},
        )

    response_body = upstream.json()

    log_event(
        "llm_response",
        model=body.get("model"),
        upstream_status=upstream.status_code,
        tool_calls=extract_tool_calls(response_body),
    )

    return JSONResponse(content=response_body, status_code=upstream.status_code)