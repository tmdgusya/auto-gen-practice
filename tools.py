import os
from dotenv import load_dotenv
load_dotenv()

from typing import Annotated, Literal
from autogen import ConversableAgent, register_function

Operator = Literal["+", "-", "*", "/"]

def calculator(a: int, b: int, operator: Annotated[Operator, "operator"]) -> int:
    if operator == "+":
        return a + b
    elif operator == "-":
        return a - b
    elif operator == "*":
        return a * b
    elif operator == "/":
        return a / b
    else:
        raise ValueError("Invalid Operator, check the definition of operator in this file")


assistant = ConversableAgent(
    name="Assistant",
    system_message="You are a helpful AI assistant. " +
    "You can help with simple calculations. " +
    "Return 'TERMINATE' when the task is done",
    llm_config={
        "config_list" : [{
            "model" : "gpt-4o-mini",
            "api_key" : os.environ.get("OPEN_AI_API_KEY"),
        }]
    }
)

user_proxy = ConversableAgent(
    name="user",
    llm_config=False,
    is_termination_msg=lambda msg: msg.get("content") is not None and "TERMINATE" in msg["content"].upper(),
    human_input_mode="NEVER"
)

assistant.register_for_llm(
    name="calculator",
    description="A simple calculator",
)(calculator)

"""
Similar to code execution, a tool must be registerd with at least two agents for it to be useful in covnersation.

register tools to excute function with user proxy agent.
"""
user_proxy.register_for_execution(name="calculator")(calculator)

register_function(
    calculator,
    caller=assistant,
    executor=user_proxy,
    name="calculator",
    description="A simple calculator",
)

chat_result = user_proxy.initiate_chat(
    assistant,
    message="What is (44232 + 13312) / 3"
)

print(chat_result)