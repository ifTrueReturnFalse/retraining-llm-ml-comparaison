import spacy
import pandas as pd

nlp = spacy.load("en_core_web_sm")


def clean_text(texts):
    """
    Cleans and preprocesses a list of text strings using spaCy.

    This function performs lemmatization, lowercasing, and removes stop words, 
    punctuation, and whitespace. It uses spaCy's pipeline for efficient batch processing.

    :param texts: An iterable of strings to be cleaned.
    :return: A list of cleaned strings, where tokens are joined by spaces.
    """
    processed_texts = []

    for doc in nlp.pipe(
        texts, disable=["parser", "ner"], batch_size=1000, n_process=-1
    ):
        tokens = [
            token.lemma_.lower()
            for token in doc
            if not token.is_stop and not token.is_punct and not token.is_space
        ]
        processed_texts.append(" ".join(tokens))

    return processed_texts


def combine_text_columns(df: pd.DataFrame) -> pd.Series:
    return (
        df["Consumer Claim"].fillna("").astype(str)
        + " "
        + df["Company"].fillna("").astype(str)
        + " "
        + df["State"].fillna("").astype(str)
        + " "
        + df["ZIP code"].fillna("").astype(str)
    )
