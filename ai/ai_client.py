import json
import requests
from ai.prompt_templates import SYSTEM_PROMPT, TOOL_DECIDER_PROMPT
from memory.database import get_recent_messages
from core.tools import TOOLS
import config
import logging

logger = logging.getLogger(__name__)

API_KEY = config.get("groq_api_key")
url = "https://api.groq.com/openai/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}


def _extract_content(r: requests.Response) -> str | None:
    """Parse response and return content string, or None if error."""
    if r.status_code != 200:
        logger.error(f"Groq API error {r.status_code}: {r.text}")
        return None
    result = r.json()
    if "choices" not in result:
        logger.error(f"Groq unexpected response: {result}")
        return None
    return result["choices"][0]["message"]["content"]


def call_ai(user_id, user_message):
    history = get_recent_messages(user_id)
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        *history,
        {"role": "user", "content": user_message}
    ]
    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": messages
    }

    r = requests.post(url, headers=headers, json=data)
    content = _extract_content(r)
    if content is None:
        return "⚠️ AI tạm thời không phản hồi được, vui lòng thử lại sau."
    return content


def decide_tool(user_message):
    tool_descriptions = ""
    for name, tool in TOOLS.items():
        tool_descriptions += f"\nTool name: {name}\nDescription: {tool['description']}\n"

    system_prompt = TOOL_DECIDER_PROMPT + "\nAvailable tools:\n" + tool_descriptions

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message}
    ]

    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": messages,
        "temperature": 0
    }

    r = requests.post(url, headers=headers, json=data)
    content = _extract_content(r)
    if content is None:
        return {"tool": None}

    logger.debug(f"TOOL RAW: {content}")

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return {"tool": None}