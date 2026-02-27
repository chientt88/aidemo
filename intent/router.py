from memory.database import save_message
from ai.ai_client import call_ai, decide_tool
from core.tools import TOOLS

def route_message(user_id, text):

    decision = decide_tool(text)

    print("TOOL RAW:", decision)

    # nếu classifier nói là tool
    if decision.get("type") == "tool":

        tool_name = decision.get("tool")  # phải có field này
        if tool_name and tool_name in TOOLS:

            tool_function = TOOLS[tool_name]["function"]
            result = tool_function()

            return call_ai(
                user_id,
                f"Dữ liệu hệ thống trả về: {result}. Hãy trả lời tự nhiên."
            )

    # normal chat
    save_message(user_id, "user", text)
    response = call_ai(user_id, text)
    save_message(user_id, "assistant", response)
    return response