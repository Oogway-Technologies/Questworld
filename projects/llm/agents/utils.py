import math
import faiss
from termcolor import colored
from typing import List
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.docstore import InMemoryDocstore
from langchain.retrievers import TimeWeightedVectorStoreRetriever
from projects.llm.agents.agent import GenerativeAgent


def relevance_score_fn(score: float) -> float:
    """Return a similarity score on a scale [0, 1]."""
    # This will differ depending on a few things:
    # - the distance / similarity metric used by the VectorStore
    # - the scale of your embeddings (OpenAI's are unit norm. Many others are not!)
    # This function converts the euclidean norm of normalized embeddings
    # (0 is most similar, sqrt(2) most dissimilar)
    # to a similarity function (0 to 1)
    return 1.0 - score / math.sqrt(2)


def create_agent_llm(max_tokens: int = 1500, model_name: str = "gpt-3.5-turbo"):
    # Can be any LLM
    return ChatOpenAI(max_tokens=max_tokens, model_name=model_name)


def create_memory_retriever() -> TimeWeightedVectorStoreRetriever:
    """Create a new vector store retriever unique to the agent."""
    # Define your embedding model
    embeddings_model = OpenAIEmbeddings()
    # Initialize the vectorstore as empty
    embedding_size = 1536
    index = faiss.IndexFlatL2(embedding_size)
    vectorstore = FAISS(embeddings_model.embed_query, index, InMemoryDocstore(
        {}), {}, relevance_score_fn=relevance_score_fn)
    return TimeWeightedVectorStoreRetriever(vectorstore=vectorstore, other_score_keys=["importance"], k=15)


def observe_agent(agent: GenerativeAgent, observations: List[str], observation_threshold: int = 5) -> str:
    """Help the notebook user interact with the agent."""
    for i, observation in enumerate(observations):
        _, reaction = agent.generate_reaction(observation)
        print(colored(observation, "green"), reaction)
        if ((i+1) % observation_threshold) == 0:
            print('*'*40)
            print(colored(
                f"After {i+1} observations, Tommie's summary is:\n{agent.get_summary(force_refresh=True)}", "blue"))
            print('*'*40)
