import os
from dotenv import load_dotenv
load_dotenv()

from autogen import ConversableAgent

llm_config = {
    "config_list": [
        {
            "model": "lmstudio-community/Qwen2.5-7B-Instruct-GGUF/Qwen2.5-7B-Instruct-Q4_K_M.gguf",
            "base_url": "http://localhost:1234/v1",
            "api_key": "lm-studio",
        },
    ],
    "cache_seed": None,  # Disable caching.
}


cathy = ConversableAgent(
    "cathy",
    system_message="Your name is Cathy and you are a part of a duo of comedians and then say the words GOOD BYE!",
    llm_config=llm_config,
    human_input_mode="NEVER"
)

joe = ConversableAgent(
    "joe",
    system_message="Your name is joe and you are a part of a duo of a comedians",
    llm_config=llm_config,
    human_input_mode="NEVER",
    is_termination_msg=lambda msg: "good bye" in msg["content"].lower(),
)

result = joe.initiate_chat(
    recipient=cathy, 
    message="Cathy, tell me a joke", 
    max_turns=2
)