import tiktoken


class Tokenizer:
    def __init__(self, model: str):
        self.model = model
        try:
            self.encoding = tiktoken.encoding_for_model(self.model)
        except KeyError:
            self.encoding = tiktoken.get_encoding('cl100k_base')

    def get_num_tokens(self, text: str) -> int:
        return len(self.encoding.encode(text))

    def encode(self, text: str) -> list:
        return self.encoding.encode(text)

    def get_num_tokens_for_chat(self, messages: dict) -> int:
        num_tokens = 0
        for message in messages:
            num_tokens += 4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
            for key, value in message.items():
                num_tokens += len(self.encoding.encode(value))
                if key == 'name':  # if there's a name, the role is omitted
                    num_tokens += -1  # role is always required and always 1 token
        num_tokens += 2  # every reply is primed with <im_start>assistant
        return num_tokens
