from gpt.models.gpt3_summarizer import GPT3Summarizer
from gpt.models.chatgpt_summarizer import ChatGPTSummarizer
from enum import Enum


class GPTModel(Enum):
    GPT3 = 1
    CHATGPT = 2


def load_model(model_type: GPTModel = GPTModel.GPT3):
    """
    Loads and returns a model
    :return: the model instance
    """
    if model_type == GPTModel.CHATGPT:
        return ChatGPTSummarizer()
    else:
        return GPT3Summarizer()
