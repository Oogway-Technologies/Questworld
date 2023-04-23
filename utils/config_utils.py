import openai
from config import Config


def setup_keys():
    # Initialize OpenAI
    if Config.OPENAI_ORGANIZATION is not None and Config.OPENAI_ORGANIZATION != "":
        openai.organization = Config.OPENAI_ORGANIZATION
    openai.api_key = Config.OPENAI_API_KEY
