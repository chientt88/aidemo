from ai.ai_client import call_ai
from memory.database import save_message

def route_message(user_id, text):

    save_message(user_id, "user", text)

    response = call_ai(user_id, text)

    save_message(user_id, "assistant", response)

    return response