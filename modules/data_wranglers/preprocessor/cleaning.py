import re
from unicodedata import normalize as unicode_normalize


def clean_wiki_text(text: str) -> str:
    """
    Clean wikipedia text by removing multiple new lines, removing extremely short lines,
    adding paragraph breaks and removing empty paragraphs
    """
    # get rid of multiple new lines
    while "\n\n" in text:
        text = text.replace("\n\n", "\n")

    # remove extremely short lines
    lines = text.split("\n")
    cleaned = []
    for l in lines:
        if len(l) > 30:
            cleaned.append(l)
        elif l[:2] == "==" and l[-2:] == "==":
            cleaned.append(l)
    text = "\n".join(cleaned)

    # add paragraphs (identified by wiki section title which is always in format "==Some Title==")
    text = text.replace("\n==", "\n\n\n==")

    # remove empty paragrahps
    text = re.sub(r"(==.*==\n\n\n)", "", text)

    return text


def normalize_text(text: str) -> str:
    """
    Perform text normalization using regex patterns
    """
    text = unicode_normalize("NFC", text)
    text = text.lower()
    text = re.sub("```(.|\n|\r)*?```", "", text)
    text = re.sub(r"\s+", " ", text)
    text = re.sub("[-_:/]", " ", text)

    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"\.+", ".", text)
    text = re.sub("[?!;…]", ".", text)
    text = text.replace("\n", ".")
    return text
