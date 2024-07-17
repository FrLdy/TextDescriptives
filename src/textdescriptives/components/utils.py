""" Utility functions for calculating various text descriptives."""

from typing import Union

from pyphen import Pyphen
from spacy.tokens import Doc, Span, Token


def filter_tokens(doc: Union[Doc, Span], keep_punct=False):
    """Return words in document or span.

    Filters punctuation and words that start with an apostrophe (contractions)
    """
    language_conditions = {
        "fr": lambda word: True,
        "en": lambda word: word.text[0] != "'",
    }

    lang = doc.lang_ if isinstance(doc, Doc) else doc.doc.lang_

    filtered_tokens = [
        word
        for word in doc
        if (keep_punct or not word.is_punct)
        and not word.is_space
        and language_conditions[lang if lang in language_conditions else "en"](word)
    ]
    return filtered_tokens


def n_sentences(doc: Doc):
    """Return number of sentences in the document."""
    return len(list(doc.sents))


def n_tokens(doc: Union[Doc, Span]):
    """Return number of words in the document."""
    return len(filter_tokens(doc))


def n_syllables(doc: Doc):
    """Return number of syllables per token."""
    dic = Pyphen(lang=doc.lang_)

    def count_syl(token: Token):
        word_hyphenated = dic.inserted(token.lower_)
        return max(1, word_hyphenated.count("-") + 1)

    return [count_syl(token) for token in filter_tokens(doc)]


all_upos_tags = [
    "ADJ",
    "ADP",
    "ADV",
    "AUX",
    "CCONJ",
    "DET",
    "INTJ",
    "NOUN",
    "NUM",
    "PART",
    "PRON",
    "PROPN",
    "PUNCT",
    "SCONJ",
    "SYM",
    "VERB",
    "X",
]
