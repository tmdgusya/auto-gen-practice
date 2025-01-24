import os
from dotenv import load_dotenv
load_dotenv()

"""
Several strategies to select the next agent

- round_robin
- random
- manual (how?)
- auto (decided by LLM)

Summarize

- reflection_with_llm
    - gives all conversation between agents to summarize 
"""
from autogen import ConversableAgent
import pprint

llm_config = {
    "config_list": [{
        "model": "gpt-4o-mini",
        "api_key": os.environ.get("OPEN_AI_API_KEY"),
    }, {
        "model": "gpt-4o",
        "api_key": os.environ.get("OPEN_AI_API_KEY"),
    }]
}

student_agent = ConversableAgent(
    name="student_agent",
    system_message="You are a student willing to learn.",
    llm_config=llm_config,
)

teacher_agent = ConversableAgent(
    name="teacher_agent",
    system_message="You are a pro math teacher. :)",
    llm_config=llm_config,
)

chat_result = student_agent.initiate_chat(
    recipient=teacher_agent,
    message="What is triangle inequality?",
    summary_method="reflection_with_llm",
    max_turns=2
)

print(chat_result.summary)

print("-"*50)

pprint.pprint(chat_result.chat_history) # if I make this to be jsonl file, then it could be used as traininig data sets to learn ai