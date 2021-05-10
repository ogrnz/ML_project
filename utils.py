# Text sanitization
import re
import nltk
from nltk.stem.snowball import SnowballStemmer

try:
    # Avoid error if you don't have the resource
    stopwords = nltk.corpus.stopwords.words("english")
except LookupError:
    nltk.download("stopwords")
    stopwords = nltk.corpus.stopwords.words("english")
    
stemmer = SnowballStemmer(language="english")

# Lang detection
import langid
from langid.langid import LanguageIdentifier, model
identifier = LanguageIdentifier.from_modelstring(model, norm_probs=True)


def lang_detect(txt: str, threshold=0.95):
    """
    Detect tweet language
    returns None if confidence lvl < threshold
    """

    if txt is None:
        return None

    txt = txt.replace("\n", " ")
    lang = identifier.classify(txt)
    if lang[1] < threshold:
        return None
    else:
        return lang[0]
    
def sanitize(text: str) -> str:
    """Sanitize a string."""
    
    # Edited regex from @gruber
    # https://gist.github.com/gruber/8891611
    url_re = r"""(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov)\b/?(?!@)))"""
    
    edited_text = re.sub(
        "  ", " ", text
    )  # replace double whitespace with single whitespace
    edited_text = re.sub("@(?=.*\w)[\w]{1,15}", "username", edited_text) # remplace twitter username by token
    edited_text = re.sub(
        url_re, "", edited_text
    )  # remove URL
    edited_text = edited_text.split(" ")  # split the sentence into array of strs
    edited_text = " ".join(
        [char for char in edited_text if char != ""]
    )  # remove any empty str from text
    edited_text = edited_text.lower()  # lowercase
    edited_text = re.sub("\d+", "", edited_text)  # Removing numerics
    edited_text = re.split(
        "\W+", edited_text
    )  # spliting based on whitespace or whitespaces
    edited_text = " ".join(
        [stemmer.stem(word) for word in edited_text if word not in stopwords]
    )  # Snowball Stemmer
    
    return edited_text