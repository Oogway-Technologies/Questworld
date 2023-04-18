from abc import ABC, abstractmethod


class AbstractSummarizer(ABC):
    @abstractmethod
    def __call__(self, texts):
        pass

    @abstractmethod
    def get_tokenizer(self):
        pass
