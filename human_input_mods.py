from dotenv import load_dotenv
import os
import random
load_dotenv()

from autogen import ConversableAgent

llm_config = {
    "config_list" : [{
        "model" : "gpt-4o-mini",
        "api_key" : os.environ.get("OPEN_AI_API_KEY")
    }]
}

generated_number_in_mind = random.randint(1, 100)

agent_with_number = ConversableAgent(
    name="agent_with_number",
    system_message=f"You are playing a game of guess-my-number. You have the number {generated_number_in_mind} in your mind" +
    " and I will try to guess it. If I guess to high, say 'too high', if I guess too lower, say 'too low'. " +
    " If I say correct answer, then say 'correct!'",
    llm_config=llm_config,
    human_input_mode="NEVER",
)

agent_guess_number = ConversableAgent(
    name="agent_guess_number",
    system_message="I have a number in my mind, and you will try to guess it. say the number to guess it. " +
    "If I say 'too high', you should guess a lower number. If I say 'too low' " + 
    "You should guess a high number " +
    "If I say 'correct', then the game end :)",
    llm_config=llm_config,
    human_input_mode="NEVER",
    is_termination_msg=lambda msg: "correct" in msg["content"].lower()
)

human_proxy = ConversableAgent(
    name="human_proxy",
    llm_config=False, # because it comes from human react.
    human_input_mode="ALWAYS",
)

# can intercept, skip, or terminate the conversation
result = human_proxy.initiate_chat(
    agent_with_number, 
    message="10",
)

# result = agent_with_number.initiate_chat(
#     agent_guess_number,
#     message="I have a number between 1 and 100. Guess it",
# )