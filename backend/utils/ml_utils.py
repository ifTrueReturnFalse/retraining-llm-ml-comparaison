import spacy

nlp = spacy.load("fr_core_news_sm")

def clean_text(text):
    doc = nlp(text.lower())

    tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct and not token.is_space]

    return " ".join(tokens)