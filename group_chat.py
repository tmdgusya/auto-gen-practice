import os
from autogen import ConversableAgent
from autogen import GroupChat, GroupChatManager
import re

llm_config = {"config_list": [
        {
            "model": "deepseek-r1-distill-qwen-7b",
            "base_url": "http://localhost:1234/v1",
            "api_key": "lm-studio",
        },
    ]}

professor = ConversableAgent(
    name="professor",
    system_message="You are a skilled and knowledgeable AI professor." +
    " and if you agree with current approach for homework, say agree",
    max_consecutive_auto_reply=10,
    llm_config=llm_config,
)
professor.description = "professor(and master of this class)"

assistant1 = ConversableAgent(
    name="assistant-1",
    system_message="You are an assistant to the AI professor. Your role is to critique and advise on how the professor educates students (e.g., through homework). Provide suggestions to make the homework more understandable for students." +
    " and if you agree with current approach for homework, say agree",
    max_consecutive_auto_reply=10,
    human_input_mode="NEVER",
    llm_config=llm_config,
)
assistant1.description = "crisitic for homework, and etc. he's really great looking down it"

assistant2 = ConversableAgent(
    name="assistant-2",
    system_message="You are an assistant to the professor. Your role is to create homework for the professor and students. Fully understand today's lessons and design homework based on them." + 
    " and if you agree with current approach for homework, say agree",
    max_consecutive_auto_reply=10,
    human_input_mode="NEVER",
    llm_config=llm_config,
)

assistant2.description = "whose make homework"

assistant3 = ConversableAgent(
    name="assistant-3",
    system_message="You should evaluate the homework to determine whether it is appropriate for students. Assess its difficulty and provide advice to assistants or the professor on how to make it easier to solve." + 
    " and if you agree with current approach for homework, say agree",
    llm_config=llm_config,
    human_input_mode="NEVER",
)

assistant3.description = "great and passion for studying people, and make something easily to be understandable format"


class CustomGroupChat(GroupChat):
    def should_end_conversation(self):
        """대화 종료 여부를 결정합니다. 'agree' 단어가 과반수 이상 등장하면 종료합니다."""
        agree_count = 0
        for message in self.messages:
            if message["content"] and isinstance(message["content"], str):
                agree_count += len(re.findall(r'\bagree\b', message["content"].lower()))
        
        if agree_count >= len(self.agents) / 2:
            return True
        return False

# 그룹 채팅과 매니저 생성
group_chat = CustomGroupChat(
    agents=[professor, assistant1, assistant2, assistant3],
    messages=[],
    max_round=3,  # 필요에 따라 max_round를 조정할 수 있습니다.
)

group_chat_manager = GroupChatManager(
    groupchat=group_chat,
    llm_config=llm_config,
)

student_agent = ConversableAgent(
    name="student_agent",
    system_message="You are a student in the AI class at MIT.",
    llm_config=llm_config,
    human_input_mode="NEVER",
)

chat_result = student_agent.initiate_chat(
    group_chat_manager,
    message="Can you make a homework that can make me to understand easily what is CNN?",
)

print(chat_result.summary)