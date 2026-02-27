import requests
from ai.prompt_templates import SYSTEM_PROMPT
from memory.database import get_recent_messages
from ai.prompt_templates import TOOL_DECIDER_PROMPT

API_KEY = "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"
url = "https://api.groq.com/openai/v1/chat/completions"
headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
# llama-3.3-70b-versatile
# llama-3.1-8b-instant
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
    
    
import json
from core.tools import TOOLS
def decide_tool(user_message):

    tool_descriptions = ""

    for name, tool in TOOLS.items():
        tool_descriptions += f"""
Tool name: {name}
Description: {tool['description']}
"""

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