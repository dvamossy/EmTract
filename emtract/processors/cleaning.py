import functools
import html
import operator
import re
import string
from typing import List

import advertools as adv
import emoji
import numpy as np
import pandas as pd
import pkg_resources
import regex
from dateutil.parser import parse
from symspellpy import SymSpell, Verbosity

"""
Text cleaning designed for social media text. 
"""

BASE_DIR = "emtract/data/dictionaries/"
PLACEHOLDERS = ["<user>", "<number>", "<ticker>", "<unknown>", "<company>"]
ENT_RE = regex.compile(r"&(#?(x?))([^&;\s]+);")
PUNCTUATIONS = '!"#&()*+,-/:;<=>?@[\\]^`{|}~'
FULL_PUNCTUATIONS = "!\"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n'"
PUNCTUATION_TABLE = str.maketrans(PUNCTUATIONS, " " * len(PUNCTUATIONS))
FULL_PUNCTUATION_TABLE = str.maketrans(FULL_PUNCTUATIONS, " " * len(FULL_PUNCTUATIONS))
REMOVE_DICT = {"'s": "", "'d": ""}
KEEP_CHARACTERS = string.printable + "".join(list(emoji.UNICODE_EMOJI["en"].keys()))

######################################################################

######################################################################
# Dictionaries for cleaning text
######################################################################

# Correct misspellings and contractions
misspell_df = pd.read_csv(BASE_DIR + "misspell_df.csv")
contraction_mapping = (
    misspell_df[misspell_df.type == "contraction"]
    .set_index("original")
    .to_dict()["changed"]
)

# Emojis + emoticons
emoticons = pd.read_csv(BASE_DIR + "emoticons.csv").values
EMOJI_EMOTICONS = np.array(
    list(emoji.UNICODE_EMOJI["en"].keys()) + list(emoticons[:, 0])
)
EMOJI_EMOTICONS_DICT = {item: "emoji" for item in EMOJI_EMOTICONS}

# Words that appear frequently
blacklist_words = pd.read_csv(BASE_DIR + "blacklist_df.csv")[
    "word"
].tolist()  # words that appear at least 1k times

# Tickers and companies
symbols_df = pd.read_csv(BASE_DIR + "symbol_df.csv")
tickers = set(symbols_df.symbol)
non_ambiguous_tickers = set(symbols_df[symbols_df.ambiguous_ticker == False].symbol)
company_name_df = pd.read_csv(BASE_DIR + "company_name_df.csv")
company_titles = set(company_name_df.title)
non_ambiguous_company_titles = set(
    company_name_df[company_name_df.ambiguous_title == False].title
)

try:
    symspell_list = pd.read_csv(
        "https://raw.githubusercontent.com/mammothb/symspellpy/master/symspellpy/frequency_dictionary_en_82_765.txt",
        sep="\s",
        names=["word", "counts"],
    )["word"].tolist()

except:
    symspell_list = pd.read_csv(BASE_DIR+"symspell_dict.csv")["word"].tolist()

blacklist_items = (
    list(emoji.UNICODE_EMOJI["en"].keys())
    + list(emoticons[:, 0])
    + PLACEHOLDERS
    + symspell_list
    + list(tickers)
    + list(company_titles)
)
INITIAL_BLACKLIST = np.array(blacklist_items)
BLACKLIST = np.array(
    list(set(blacklist_items + blacklist_words + list(string.punctuation)))
)
BLACKLIST_DICT = {item: "word" for item in BLACKLIST}

# For segmenting
dict_type = "frequency_dictionary_en_82_765.txt"
sym_spell = SymSpell(
    max_dictionary_edit_distance=0, prefix_length=7
)  # use this for first segmenting
sym_spell_two = SymSpell(
    max_dictionary_edit_distance=1, prefix_length=7
)  # use this for first segmenting
dictionary_path = pkg_resources.resource_filename("symspellpy", dict_type)
sym_spell.load_dictionary(dictionary_path, term_index=0, count_index=1)
sym_spell_two.load_dictionary(dictionary_path, term_index=0, count_index=1)


######################################################################

######################################################################
# Functions for converting html entities
######################################################################


def _str_to_unicode(text, encoding=None, errors="strict"):
    if encoding is None:
        encoding = "utf-8"
    if isinstance(text, bytes):
        return text.decode(encoding, errors)
    return text


def _replace_html_entities(text, keep=(), remove_illegal=True, encoding="utf-8"):
    """
    Remove entities from text by converting them to their
    corresponding unicode character.

    :param text: a unicode string or a byte string encoded in the given
    `encoding` (which defaults to 'utf-8').

    :param list keep:  list of entity names which should not be replaced.\
    This supports both numeric entities (``&#nnnn;`` and ``&#hhhh;``)
    and named entities (such as ``&nbsp;`` or ``&gt;``).

    :param bool remove_illegal: If `True`, entities that can't be converted are\
    removed. Otherwise, entities that can't be converted are kept "as
    is".

    :returns: A unicode string with the entities removed.

    See https://github.com/scrapy/w3lib/blob/master/w3lib/html.py

        >>> from nltk.tokenize.casual import _replace_html_entities
        >>> _replace_html_entities(b'Price: &pound;100')
        'Price: \\xa3100'
        >>> print(_replace_html_entities(b'Price: &pound;100'))
        Price: £100
        >>>
    """

    def _convert_entity(match):
        entity_body = match.group(3)
        if match.group(1):
            try:
                if match.group(2):
                    number = int(entity_body, 16)
                else:
                    number = int(entity_body, 10)
                # Numeric character references in the 80-9F range are typically
                # interpreted by browsers as representing the characters mapped
                # to bytes 80-9F in the Windows-1252 encoding. For more info
                # see: https://en.wikipedia.org/wiki/ISO/IEC_8859-1#Similar_character_sets
                if 0x80 <= number <= 0x9F:
                    return bytes((number,)).decode("cp1252")
            except ValueError:
                number = None
        else:
            if entity_body in keep:
                return match.group(0)
            number = html.entities.name2codepoint.get(entity_body)
        if number is not None:
            try:
                return chr(number)
            except (ValueError, OverflowError):
                pass

        return "" if remove_illegal else match.group(0)

    return ENT_RE.sub(_convert_entity, _str_to_unicode(text, encoding))


######################################################################
# Normalization Functions
######################################################################


def remove_links(text):
    """
    Takes a string and removes web links from it.
    """
    text = re.sub(r"http\S+", " ", text)  # remove http links
    text = re.sub(r"www.\S+", " ", text)  # remove www. links
    text = re.sub(r"bit.ly/\S+", " ", text)  # remove bitly links
    text = re.sub(r"\S+://\S+", " ", text)  # remove tricky links
    text = re.sub(r"\[[^]]*\]", " ", text)  # remove words inside brackets
    text = re.sub(
        "\S+\.(gif|png|jpg|jpeg|eps|pdf|raw|psd|tiff)\W+?", "", text
    )  # remove image filenames
    text = re.sub("\S*@\S*\s?", " ", text)  # remove email addresses
    text = re.sub(r"\d{1,2}:\d{2}:\d{2}[a|p]?m?", "", text)  # remove dates
    text = re.sub(r"\d{1,2}:\d{2}[a|p]?m?", "", text)  # remove dates
    text = "".join(
        filter(lambda char: char in KEEP_CHARACTERS, text)
    )  # remove nonprintable characters (that are not emojis)
    return text.replace("&lt;", "").replace("&gt;", "")


def remove_tags(text):
    """
    Takes a string and removes @user.
    """
    text = text.lower() + " "
    text = re.sub("(@[a-z0-9]+[a-z0-9-_]+)", " <user> ", text)  # remove users
    return text


def swap_numbers(text):
    """
    Swap numbers for placeholder, as our model doesn't learn much from them
    """
    text = text.replace("_", " ").replace("#", "")
    text = re.sub(r"([0-9,.]*[0-9]+)", " <number> ", text)
    return text


def split_emoji_from_text(text):
    num_emojis = adv.extract_emoji(text)["overview"]["num_emoji"]
    if num_emojis > 0:
        em_split_emoji = emoji.get_emoji_regexp().split(text)
        em_split_whitespace = [substr.split() for substr in em_split_emoji]
        em_split = " ".join(functools.reduce(operator.concat, em_split_whitespace))
        return em_split
    else:
        return text


def split_emoticon_from_text(tweet):
    """
    Split emoticons from text.
    """
    for emoticon, text in emoticons:
        tweet = tweet.replace(emoticon, f" {emoticon} ")
    return tweet


def multiple_replace(replace_dict, text):
    """
    Replaces every value from the given dictionary using regular expression
    :param replace_dict: keys in text are replaced by values
    :param text:
    :return:
    """
    regex = re.compile("(%s)" % "|".join(map(re.escape, replace_dict.keys())))
    # For each match, look-up corresponding value in dictionary
    return regex.sub(lambda mo: replace_dict[mo.string[mo.start() : mo.end()]], text)


def replace_contractions(text):
    """
    Expands contractions into complete words (i.e. don't -> do not)
    """
    text = re.sub("\s+", " ", text)  # remove tabs and etc.
    new_text_list = []

    for word in text.split():
        if word not in EMOJI_EMOTICONS_DICT:
            word = swap_numbers(word)
            word_list = re.findall(
                r"[<\w'>]+|[\w']+|[:.,!?;\+\-\*\/\%\&\$]", word
            )  # split punctuations from words, such as thats, will be split to thats ,
            for part in word_list:
                part = (
                    contraction_mapping[part] if part in contraction_mapping else part
                )
                part = multiple_replace(REMOVE_DICT, part)

                if part.strip():
                    new_text_list.append(part)
        else:
            new_text_list.append(word)

    text = " ".join(new_text_list)

    return text


def correct_segments(text):
    new_text_list = []
    for word in text.split():
        if word not in BLACKLIST_DICT:
            last_punctuation = " " + re.split(r"\w+", word)[-1]
            stripped_word = " ".join(word.translate(FULL_PUNCTUATION_TABLE).split())
            if len(stripped_word) > 0:
                segmented_word = sym_spell.word_segmentation(stripped_word)
                segmented_corrected_word = sym_spell_two.word_segmentation(
                    stripped_word
                )
                if (
                    segmented_word.corrected_string
                    == segmented_corrected_word.corrected_string
                ):
                    new_text_list.append(
                        segmented_word.corrected_string + last_punctuation
                    )
                else:
                    new_text_list.append(stripped_word + last_punctuation)
        else:
            new_text_list.append(word)
    text = " ".join(new_text_list)
    return text


def reduce_lengthening(text):
    """
    Replace repeated character sequences of length 2 or greater with sequences
    of length 2.
    """
    pattern = regex.compile(r"(.)\1{2,}")
    text = pattern.sub(r"\1\1", text)
    text = re.sub(r"(.)\1+", r"\1\1", text)  # remove repeated characters
    text = regex.sub(
        r"(?<= |^)(\S+)(?: \1){2,}(?= |$)", r"\1 \1", text
    )  # remove words that repeat more than twice
    return text


def remove_tickers_and_companies(text):
    """
    Remove any tickers or company names that appear in the text. We append a placeholder to denote the presence
    of a ticker in the text. We ignore some company and tickers which are also commonly used words.
    :param text:
    :return:
    """
    text_list = text.split()
    new_text_list = []
    for index, word in enumerate(text_list):
        check_word = word.translate(PUNCTUATION_TABLE).strip()
        if word[0] == "$":
            if check_word[1:] in tickers:
                new_text_list.append("<ticker>")
                continue
        if word in non_ambiguous_tickers or check_word in non_ambiguous_tickers:
            new_text_list.append("<ticker>")
            continue
        if (
            word in non_ambiguous_company_titles
            or check_word in non_ambiguous_company_titles
        ):
            new_text_list.append("<company>")
            continue
        new_text_list.append(word)
    text = " ".join(new_text_list)
    text = re.sub(
        "\$[a-z._]+", " <unknown> ", text
    )  # replace fake tickers with unknown
    return text


def clean_text(text: str, reduce_len=True, segment_words=True) -> str:
    """Clean the input text.

    :param text: str
    :rtype: list(str)
    :return: a tokenized list of strings; joining this list returns\
    the original string if `preserve_case=False`.
    """
    try:
        # Fix HTML character entities:
        text = _replace_html_entities(text)
        # Fix retext at, replace username with <user> placeholder
        text = remove_tags(text)
        # Remove links, dates, email addresses, images
        text = remove_links(text)
        # Split emojis and emoticons from words
        text = split_emoji_from_text(text)
        text = split_emoticon_from_text(text)
        # Remove company names and tickers
        text = remove_tickers_and_companies(text)
        # Fix contractions
        text = replace_contractions(text)
        if segment_words:
            text = correct_segments(text)

        # Normalize word lengthening
        if reduce_len:
            text = reduce_lengthening(text)
        check_text = text.strip().split()
        if len(check_text) < 1 or set(check_text).issubset(PLACEHOLDERS):
            text = ""
    except:
        text = ""

    return text


def clean_words(text):
    """
    Swap numbers for placeholder, as our model doesn't learn much from them
    """
    # Fix HTML character entities:
    text = _replace_html_entities(text)
    # Fix retext at, replace username with <user> placeholder
    text = remove_tags(text)
    # Remove links, dates, email addresses, images
    text = remove_links(text)
    # Split emojis and emoticons from words
    try:
        text = split_emoji_from_text(text)
    except:
        pass
    text = split_emoticon_from_text(text)
    # Remove company names and tickers
    text = remove_tickers_and_companies(text)
    # Fix contractions
    text = replace_contractions(text)
    try:
        text = reduce_lengthening(text)
    except:
        pass
    return text.split()
