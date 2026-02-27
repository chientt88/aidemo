import json
import requests
from ai.prompt_templates import SYSTEM_PROMPT, TOOL_DECIDER_PROMPT
from memory.database import get_recent_messages
from core.tools import TOOLS
import config

API_KEY = config.get("groq_api_key")
url = "https://api.groq.com/openai/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

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

    print("STATUS:", r.status_code)
    print("RESPONSE:", r.text)

    result = r.json()
    return result["choices"][0]["message"]["content"]


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
    result = r.json()
    content = result["choices"][0]["message"]["content"]

    print("TOOL RAW:", content)

    try:
        return json.loads(content)
    except:
        return {"tool": None}