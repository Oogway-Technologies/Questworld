import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    # erver Vars
    SERVER_PORT = int(os.getenv("SERVER_PORT")) or 8000

    #
    # Add additional parameters below
    #
    # OPENAI
    OPENAI_ORGANIZATION = os.getenv("OPENAI_ORGANIZATION") or None
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    # PINECONE
    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY") or None
    PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT") or None
