import os
import json
import re
import httpx
from typing import List, Dict, Any

# ---------------------------------------------------------------------------
# Helper to extract raw JSON from model output that may be wrapped in markdown
# ---------------------------------------------------------------------------
def _extract_json(text: str) -> str:
    m = re.search(r"```(?:json)?\s*\n?([\s\S]*?)\n?\s*```", text, re.DOTALL)
    if m:
        return m.group(1).strip()
    m = re.search(r"(\{.*\}|\[.*\])", text, re.DOTALL)
    if m:
        return m.group(1).strip()
    return text.strip()

# ---------------------------------------------------------------------------
# Core inference caller – used by both business functions
# ---------------------------------------------------------------------------
async def _call_inference(messages: List[Dict[str, str]], max_tokens: int = 512) -> Dict[str, Any]:
    api_url = "https://inference.do-ai.run/v1/chat/completions"
    token = os.getenv("DIGITALOCEAN_INFERENCE_KEY")
    model = os.getenv("DO_INFERENCE_MODEL", "openai-gpt-oss-120b")
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "messages": messages,
        "max_completion_tokens": max_tokens
    }
    try:
        async with httpx.AsyncClient(timeout=90.0) as client:
            resp = await client.post(api_url, headers=headers, json=payload)
            resp.raise_for_status()
            data = resp.json()
            # Expected OpenAI‑compatible response shape
            content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
            json_str = _extract_json(content)
            return json.loads(json_str)
    except Exception as e:
        # Return a graceful fallback so routes never raise
        return {"note": "AI service temporarily unavailable", "error": str(e)}

# ---------------------------------------------------------------------------
# Public helper functions used by route handlers
# ---------------------------------------------------------------------------
async def analyze_patterns(messages: List[Dict[str, str]]) -> Dict[str, Any]:
    return await _call_inference(messages, max_tokens=512)

async def generate_insights(messages: List[Dict[str, str]]) -> Dict[str, Any]:
    return await _call_inference(messages, max_tokens=512)
