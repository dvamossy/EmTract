import re
import string

from emtract.data.cleaning import unicode_emotes, emoticons, special_dict_r1, special_dict_r2, special_dict_r3, \
    contraction_mapping, misspell_mapping, remove_dict, tickers, non_ambiguous_tickers, non_ambiguous_company_titles, punctuation_table

def multiple_replace(replace_dict, tweet):
    """
    Replaces every value from the given dictionary using regular expression
    :param replace_dict: keys in text are replaced by values
    :param tweet:
    :return:
    """
    regex = re.compile("(%s)" % "|".join(map(re.escape, replace_dict.keys())))
    # For each match, look-up corresponding value in dictionary
    return regex.sub(lambda mo: replace_dict[mo.string[mo.start():mo.end()]], tweet)


def remove_links(tweet):
    """
    Takes a string and removes web links from it.
    """
    tweet = re.sub(r'http\S+', ' ', tweet)  # remove http links
    tweet = re.sub(r'www.\S+', ' ', tweet)  # remove www. links
    tweet = re.sub(r'bit.ly/\S+', ' ', tweet)  # remove bitly links
    tweet = re.sub(r'\S+://\S+', ' ', tweet)  # remove tricky links
    tweet = re.sub(r'\[[^]]*\]', ' ', tweet)  # remove words inside brackets
    tweet = re.sub('\S+\.(gif|png|jpg|jpeg|eps|pdf|raw|psd|tiff)\W+?', '',
                   tweet)  # remove image filenames
    tweet = re.sub('\S*@\S*\s?', ' ', tweet)  # remove email addresses
    return tweet


def remove_tags(tweet):
    """
    Takes a string and removes retweet and @user.
    """
    tweet = re.sub('(^rt:? @[a-z]+[a-z0-9-_]+)|(\W+rt:? @[a-z]+[a-z0-9-_]+)', ' ', tweet)  # remove retweeted at
    tweet = re.sub('(@[a-z0-9]+[a-z0-9-_]+)', ' ', tweet)  # remove users
    return tweet


def clean_text(tweet):
    """
    Main cleaning function. Performs multiple actions.
    1. Removes punctuation and tabs
    2. Expands contractions into complete words (i.e. don't -> do not)
    3. Corrects misspelled words
    :param tweet:
    :return:
    """
    tweet = tweet.translate(punctuation_table)  # strip punctuation
    tweet = re.sub('\s+', ' ', tweet).rstrip().lstrip()  # remove tabs and etc.
    tweet_list = tweet.split()
    new_tweet_list = []
    for word in tweet_list:
        word = contraction_mapping[word] if word in contraction_mapping else word
        word = multiple_replace(remove_dict, word)
        word = misspell_mapping[word] if word in misspell_mapping else word
        if word.strip():
            new_tweet_list.append(word)

    tweet = ' '.join(new_tweet_list)
    tweet = tweet.replace('\'', '')
    tweet = re.sub(
        r'(.)\1+', r'\1\1',
        tweet)  # remove repeated characters #need to do it after cleaning too
    return tweet


def sub_special(tweet):
    """
    Replace tweets with 3 custom dictionaries for corner cases
    :param tweet:
    :return:
    """
    tweet = multiple_replace(special_dict_r1, tweet)
    tweet = multiple_replace(special_dict_r2, tweet)
    tweet = multiple_replace(special_dict_r3, tweet)
    tweet = re.sub(
        "[\u2019\u2018\u201a\u201b\u201c\u201d\u201e\u201f\u2039\u203a\u00ab\u00bb\u0022\u301d\u301e\u301f\uff02\uff07]",
        "'", tweet)
    tweet = re.sub('([.,!?();])', r' \1 ', tweet)  # enforce spacing
    tweet = "".join(filter(lambda char: char in string.printable, tweet))  # remove non-printable characters
    tweet = re.sub(r'(.)\1+', r'\1\1', tweet)  # remove repeated characters
    return tweet


PLACEHOLDERS = {'percentageplaceholder', 'dollarvalueplaceholder', 'numbervalueplaceholder',
                'companyplaceholder'}


def swap_numbers(tweet):
    """
    Swap different numbers for placeholders, as our model doesn't learn much from them
    :param tweet:
    :return:
    """
    tweet = tweet.replace('_', ' ')
    tweet = re.sub('\$[0-9]+[k?m?b?t?]+',, 'dollarvalueplaceholder', tweet)  # remove symbols
    tweet = re.sub(r"\d+[k?m?b?t?]+", 'numbervalueplaceholder', tweet)  # remove symbols
    tweet = re.sub("%", "percentageplaceholder", tweet)
    if 'percentageplaceholder' in tweet:
        tweet = tweet.replace("percentageplaceholder", '') + ' percentageplaceholder'
    if 'dollarvalueplaceholder' in tweet:
        tweet = tweet.replace('dollarvalueplaceholder', '') + ' dollarvalueplaceholder'
    if 'numbervalueplaceholder' in tweet:
        tweet = tweet.replace('numbervalueplaceholder', '') + ' numbervalueplaceholder'
    return tweet.replace('$', '')


def convert_emoticons(tweet):
    """
    Convert emoticons into grouped text names.
    For example :) and (^_^)v will become happyface
    :param tweet:
    :return:
    """
    for emoticon, text in emoticons:
        tweet = tweet.replace(emoticon, text)
    return tweet


def convert_emojis(tweet):
    """
    Convert emojis into text names
    :param tweet:
    :return:
    """
    # Remove gender / race information
    tweet = re.sub("[\U0000200D\U00002642\U00002640\U0001F3FD\U0001F3FC\U0001F3FE\U0001F3FB\U0001F3FF]", "", tweet)
    for unicode_emote, text in unicode_emotes:
        tweet = tweet.replace(unicode_emote, text)
    return tweet


def remove_tickers_and_companies(tweet):
    """
    Remove any tickers or company names that appear in the text. We append a placeholder to denote the presence
    of a ticker in the text. We ignore some company and tickers which are also commonly used words.
    :param tweet:
    :return:
    """
    tweet_list = tweet.split()
    has_company = False
    new_tweet_list = []
    for index, word in enumerate(tweet_list):
        if word[0] == '$':
            if word[1:] in tickers:
                has_company = True
                continue
            if index < len(tweet_list) -1:
                if word[1:] + ' ' + tweet_list[index+1] in tickers:
                    has_company = True
                    continue
        if index < len(tweet_list) - 1:
            if word + ' ' + tweet_list[index+1] in non_ambiguous_tickers:
                has_company = True
                continue
        if word in non_ambiguous_tickers:
            has_company = True
            continue
        if word in non_ambiguous_company_titles:
            has_company = True
            continue
        new_tweet_list.append(word)
    if has_company:
        new_tweet_list.append('companyplaceholder')
    return ' '.join(new_tweet_list)


def clean_tweet(tweet):
    """
    Main function to run cleaning sequentially
    :param tweet:
    :return:
    """
    tweet = str(tweet).lower() + ' '

    tweet = remove_tags(tweet)
    tweet = remove_links(tweet)

    tweet = convert_emoticons(tweet)
    tweet = convert_emojis(tweet)

    tweet = sub_special(tweet)

    # Clean text will remove punctuation, so any cleaning action that requires it to be present (emoticons, links, etc)
    # needs to be run before this step
    tweet = clean_text(tweet)
    tweet = remove_tickers_and_companies(tweet)

    # Remove misspellings, correct contractions, remove special characters
    tweet = swap_numbers(tweet)
    tweet = " ".join(tweet.split())
    # Remove tweets shorter than n characters or that only contain placeholders
    check_tweet = tweet.strip().split()
    if len(check_tweet) < 1 or set(check_tweet).issubset(PLACEHOLDERS):
        tweet = ''
    return tweet


if __name__ == "__main__":
    while True:
        tweet_to_clean = input('Input tweet: ')
        print(clean_tweet(tweet_to_clean))
    # import pandas as pd
    # import time
    # tweets = pd.read_parquet('messages_sample.parquet.snappy')
    # n = 0
    # start = time.time()
    # for i, row in tweets.iterrows():
    #     if n == 500:
    #         print('time: {}'.format(time.time() - start))
    #         break
    #     n += 1

