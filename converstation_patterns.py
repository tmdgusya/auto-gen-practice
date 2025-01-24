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
    "config_list": [
        {
            "model": "lmstudio-community/Qwen2.5-7B-Instruct-GGUF/Qwen2.5-7B-Instruct-Q4_K_M.gguf",
            "base_url": "http://localhost:1234/v1",
            "api_key": "lm-studio",
        },
    ],
    "cache_seed": None,  # Disable caching.
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

"""
Carry-over mechanism which brings the summaries of previous chat to the context of the next chat

@params context which has summaries of previous chat

Summary of current chat -----> next_chat(context)

"""