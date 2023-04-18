from typing import List
from langchain.retrievers import TimeWeightedVectorStoreRetriever
from langchain.chat_models import ChatOpenAI
from projects.llm.agents.agent import GenerativeAgent


def build_agent(
    name: str,
    age: int,
    traits: str,  # anxious, likes design, etc
    status: str,  # looking for a job, etc
    memory_retriever: TimeWeightedVectorStoreRetriever,
    llm: ChatOpenAI,
    daily_summaries: List[str],
    reflection_threshold: float = 8
) -> GenerativeAgent:
    agent = GenerativeAgent(
        name=name,
        age=age,
        traits=traits,
        status=status,
        memory_retriever=memory_retriever,
        llm=llm,
        daily_summaries=daily_summaries,
        reflection_threshold=reflection_threshold
    )
    return agent
