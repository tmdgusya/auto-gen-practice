import os
from dotenv import load_dotenv
from dataclasses import dataclass
from typing import Callable

from autogen import ConversableAgent

load_dotenv()

agent = ConversableAgent(
    name="chatbot",
    llm_config={
        "config_list" : [{
            "model": "gpt-4o-mini",
            "api_key" : os.environ.get("OPEN_AI_API_KEY")
        }]
    },
    code_execution_config=False, # Turn off code execution
    function_map=None,
    human_input_mode="NEVER",
)

reply = agent.generate_reply(
        messages=[{
            "content": "Tell me a joke",
            "role": "user"
        }]
    )

print(reply)