from langchain import LLMChain, PromptTemplate
from langchain.chat_models import ChatOpenAI

import re


async def get_suggestions_questions(input: str) -> list[str]:
    """Get suggestions questions."""

    llm = ChatOpenAI(
        streaming=True,
        temperature=0,
    )

    prompt_is_farewell_topic_chain = PromptTemplate(
        input_variables=["input"],
        template="Determinate if the '{input}' is related to the topic of farewell and return True or False",
    )
    prompt = PromptTemplate(
        input_variables=["input"],
        template="Create three good suggestions questions about this topic of: {input}. Return the suggestions like a list.",
    )
    is_farewell_topic_chain = LLMChain(llm=llm, prompt=prompt_is_farewell_topic_chain)
    is_farewell_topic_response = await is_farewell_topic_chain.arun(input)
    suggested_responses = []

    if "False" in is_farewell_topic_response:
        chain = LLMChain(llm=llm, prompt=prompt)
        response_chain = await chain.arun(input)
        suggested_responses = re.findall(r"\d+\.\s(.*?\?)", response_chain)
        suggested_responses = suggested_responses[:3]

    return suggested_responses
