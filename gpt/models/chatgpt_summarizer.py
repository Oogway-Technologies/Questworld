import re
import logging
import openai
import time
from gpt.models.tokenizer import Tokenizer
from gpt.models.abstract_summarizer import AbstractSummarizer
from utils.text_processing import cut_last_sentence
from const import *


def generateSystemPrompt(prompt: str):
    return {
        'role': 'system',
        'content': prompt
    }


def generateUserPrompt(prompt: str):
    return {
        'role': 'user',
        'content': prompt
    }


def generateAssistantPrompt(prompt: str):
    return {
        'role': 'assistant',
        'content': prompt
    }


class ChatGPTSummarizer(AbstractSummarizer):
    def __init__(self):
        self.model = DEFAULT_CHATGPT_MODEL_NAME
        self.embedding_model = DEFAULT_GPT_EMBEDDING_MODEL_NAME
        self.tokenizer = Tokenizer(model=DEFAULT_CHATGPT_MODEL_NAME)
        self.controller = None
        self.custom_model = False
        self.max_context_length = 4000
        self.max_tokens = 2048
        self.summarizer_frequency_penalty = 0.0
        self.summarizer_top_p = 1.0
        self.summarizer_temperature = 0.7
        self.summarizer_presence_penalty = 0.0

    def get_tokenizer(self):
        return self.tokenizer

    def reset_model(self):
        self.set_default_model()

    def set_default_model(self):
        self.summarizer_frequency_penalty = 0.0
        self.summarizer_presence_penalty = 0.0
        self.set_model(DEFAULT_CHATGPT_MODEL_NAME)
        self.set_default_max_context_length()
        self.tokenizer = Tokenizer(model=DEFAULT_CHATGPT_MODEL_NAME)

    def get_model(self):
        return self.model

    def set_model(self, model):
        if model != DEFAULT_CHATGPT_MODEL_NAME:
            self.custom_model = True
            self.tokenizer = Tokenizer(model=model)
        else:
            self.custom_model = False
        self.model = model

    def set_max_context_length(self, max_context_length: int):
        self.max_context_length = max_context_length

    def set_default_max_context_length(self):
        self.max_context_length = 4000

    def get_embeddings(self, query: str):
        content = query.encode(encoding='ASCII', errors='ignore').decode()
        response = openai.Embedding.create(
            input=content, engine=self.embedding_model)
        vector = response['data'][0]['embedding']  # this is a normal list
        return vector

    def __call__(self, messages, max_tokens=None, top_p=None, temperature=None, retry_until_success=True,
                 stop=None, logit_bias=None, num_completions=1, cut_sentence=False, model_string=None, clean_output=False,
                 frequency_penalty=0.0, presence_penalty=0.0, save_logs=False):
        assert type(messages) == list

        if logit_bias is None:
            logit_bias = {}
        if self.controller is None:
            return self._call_helper(messages=messages, max_tokens=max_tokens, top_p=top_p,
                                     temperature=temperature, retry_until_success=retry_until_success, stop=stop,
                                     logit_bias=logit_bias, num_completions=num_completions, cut_sentence=cut_sentence,
                                     clean_output=clean_output, frequency_penalty=frequency_penalty,
                                     presence_penalty=presence_penalty, model_string=model_string, save_logs=save_logs)
        else:
            raise NotImplementedError

    def _call_helper(self, messages, max_tokens=None, top_p=None, temperature=None,
                     retry_until_success=True, stop=None, logit_bias=None, num_completions=1, cut_sentence=False,
                     model_string=None, clean_output=False, frequency_penalty=None, presence_penalty=None, save_logs=True):
        # Use default model if none is provided
        if model_string is None:
            engine = self.model if model_string is None else model_string

        if logit_bias is None:
            logit_bias = {}

        outputs = []
        completion = dict()
        num_fails = 0
        max_retry = 10
        run_generation = True
        while run_generation:
            try:
                engine = self.model if model_string is None else model_string
                if len(logit_bias) > 300:
                    logging.warning('Logit bias greater than 300')
                    logit_bias_clean = dict()
                    idx = 0
                    for key, val in logit_bias.items():
                        if idx > 299:
                            break
                        logit_bias_clean[key] = val
                        idx += 1
                    logit_bias = logit_bias_clean
                completion = openai.ChatCompletion.create(
                    model=engine,
                    messages=messages,
                    max_tokens=max_tokens,
                    temperature=temperature if temperature is not None else self.summarizer_temperature,
                    top_p=top_p if top_p is not None else self.summarizer_top_p,
                    frequency_penalty=frequency_penalty if frequency_penalty is not None else self.summarizer_frequency_penalty,
                    presence_penalty=presence_penalty if presence_penalty is not None else self.summarizer_presence_penalty,
                    stop=stop,
                    logit_bias=logit_bias,
                    n=num_completions)
                run_generation = False
            except Exception as e:
                logging.warning(str(e))
                run_generation = retry_until_success
                num_fails += 1
                if num_fails > max_retry:
                    raise e
                if run_generation:
                    logging.warning('retrying...')
                    time.sleep(num_fails * 0.5)

        outputs += [completion['choices'][j]['message']['content']
                    for j in range(num_completions)]

        # Save logs
        if save_logs:
            # TODO: save logs
            # now = datetime.now()
            # date_time = now.strftime("%m_%d_%Y_%H_%M_%S")
            # messages_list = [message['content'] for message in messages]
            # log_data = '\n'.join(messages_list) + \
            #     '\n\n==========\n\n' + outputs[0]
            # logPath = str(
            #     Path(__file__).parent.parent.parent / 'logs/gpt3')
            # save_file(log_data, f'{logPath}_{date_time}.txt')
            pass

        if clean_output:
            outputs = [text.strip() for text in outputs]
            outputs = [re.sub('[\r\n]+', '\n', text) for text in outputs]
            outputs = [re.sub('[\t ]+', ' ', text) for text in outputs]

        if cut_sentence:
            for i in range(len(outputs)):
                if len(outputs[i].strip()) > 0:
                    outputs[i] = cut_last_sentence(outputs[i])

        # Return the generated outputs
        return outputs
