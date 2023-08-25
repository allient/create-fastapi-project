# flake8: noqa
from pydantic import BaseModel


class IZeroPrompt(BaseModel):
    prefix: str
    suffix: str
    format_instructions: str
    input_variables: list[str]


PREFIX = """Answer the following questions as best and complete you can. You have access to the following tools:"""
FORMAT_INSTRUCTIONS = """Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question"""
SUFFIX = """When answering, your answers should be with markdown format.

Question: {input}
Thought:{agent_scratchpad}"""


# Question: What is the topic of the question?
# Thought: I now know the partial answer
# Action: the action to take, should be determinate the topic of the question with GeneralKnowledgeTool tool
# Action Input: the input to the action
# Observation: the result of the action
# ... (this Thought/Action/Action Input/Observation can repeat 1 time)
# If you detect this answer topic is about Greetings append this to the end of the answer: "Greetings" : [BOOL_VALUE]
zero_agent_prompt = IZeroPrompt(
    prefix=PREFIX,
    suffix=SUFFIX,
    format_instructions=FORMAT_INSTRUCTIONS,
    input_variables=["input", "agent_scratchpad"],
)
