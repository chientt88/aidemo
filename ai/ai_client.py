import requests
from ai.prompt_templates import SYSTEM_PROMPT
from memory.database import get_recent_messages

API_KEY = ""

def call_ai(user_id, user_message):

    history = get_recent_messages(user_id)

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        *history,
        {"role": "user", "content": user_message}
    ]

    data = {
        "model": "llama-3.1-8b-instant",
        "messages": messages
    }
    
    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    r = requests.post(url, headers=headers, json=data)

    print("STATUS:", r.status_code)
    print("RESPONSE:", r.text)

    result = r.json()
    return result["choices"][0]["message"]["content"]


