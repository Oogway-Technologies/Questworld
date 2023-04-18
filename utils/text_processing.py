import spacy
from const import SPACY_MODEL


nlp = spacy.load(SPACY_MODEL)


def split_paragraphs(text, mode='none'):
    """
    Split a text into paragraphs according to the given mode.
    """
    if not text:
        return []
    if mode == 'none':
        return [text.strip()]
    elif mode == 'newline':
        while '\n\n' in text:
            text = text.replace('\n\n', '\n')
        return [s.strip() for s in text.split('\n')]
    elif mode == 'newline-filter':
        while '\n\n' in text:
            text = text.replace('\n\n', '\n')
        paragraphs = text.split('\n')
        return [p.strip() for p in paragraphs if len(p.split()) > 100]
    elif mode == 'sentence':
        doc = nlp(text)
        sentences = [sent.text.strip() for sent in doc.sents]
        return sentences
    else:
        raise NotImplementedError


def cut_last_sentence(text):
    """
    Remove possibly incomplete last sentence
    :param text: the text to process
    :return: the processed text
    """
    # Possibly start a new sentence, so we can delete it,
    # if the last sentence is already complete and ended with a period
    text = text.rstrip() + ' and'
    # Possibly incomplete, so strip it
    last_sentence = split_paragraphs(text, mode='sentence')[-1].strip()
    text = text.rstrip()[: len(text.rstrip()) - len(last_sentence)].rstrip()
    return text
