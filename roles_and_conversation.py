import os
from dotenv import load_dotenv
load_dotenv()

from autogen import ConversableAgent

config_list = [{
            "model": "gpt-4o-mini",
            "temperature": 0.9,
            "api_key": os.environ.get("OPEN_AI_API_KEY")
        }]


cathy = ConversableAgent(
    "cathy",
    system_message="Your name is Cathy and you are a part of a duo of comedians",
    llm_config={"config_list" : config_list},
    human_input_mode="NEVER"
)

joe = ConversableAgent(
    "joe",
    system_message="Your name is joe and you are a part of a duo of a comedians",
    llm_config={ "config_list": config_list },
    human_input_mode="NEVER"
)

result = joe.initiate_chat(
    recipient=cathy, 
    message="Cathy, tell me a joke", 
    max_turns=2
)