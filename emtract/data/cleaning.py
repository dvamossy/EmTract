import pandas as pd

special_dict_r1 = {"&amp;#39,s": "'", "Â´": "'", "-&gt;": ""}
special_dict_r2 = {
    "(s)": "s",
    "&#39;": "'",
    "lt;": "",
    ";lt": "",
    "gt;": "",
    ";gt": "",
    "\'": "'",
    "&quot;": "",
    "&amp;": " and ",
    "â€™": "'",
    "Ã©": "'",
    "\n": " ",
    "\t": " ",
    "-ly ": "ly ",
    " i.e. ": " that is ",
    " e.g. ": " for example "
}
special_dict_r3 = {
    "''": "'",
    " you 'll ": " you will ",
    " we 'll ": " we will ",
    " they 'll ": " they will ",
    " i 'll ": " i will ",
    " would ve ": " would have ",
    " we ve ": " we have ",
    " i ve ": " i have "
}
remove_dict = {"'s": "", "'d": ""}

BASE_DIR = 'emtract/data/'

emoticons = pd.read_csv(BASE_DIR + 'emoticons.csv').values
unicode_emotes = pd.read_csv(BASE_DIR + 'unicode_emotes.csv').values

misspell_df = pd.read_csv(BASE_DIR + 'misspell_df.csv')
segmented_df = pd.read_parquet(BASE_DIR + 'segmented_df.parquet.snappy').dropna()
autocorrected_df = pd.read_parquet(BASE_DIR + 'auto_corrected_df.parquet.snappy').dropna()
#Correct misspellings and contractions
contraction_mapping = misspell_df[misspell_df.type == 'contraction'].set_index(
    'original').to_dict()['changed']
misspell_mapping = misspell_df[misspell_df.type == 'misspell'].append(
    segmented_df).append(autocorrected_df).set_index(
        'original').to_dict()['changed']

# Tickers and companies
symbols_df = pd.read_csv(BASE_DIR + 'symbol_df.csv')

# Removed \', % and $ as we use them for tagging
punctuation_table = str.maketrans('!"#&()*+,-./:;<=>?@[\\]^_`{|}~', ' '*len('!"#&()*+,-./:;<=>?@[\\]^_`{|}~'))

# Words after _ in tickers
tickers = set([item.translate(punctuation_table) for item in set(symbols_df.symbol)])
non_ambiguous_tickers = set([item.translate(punctuation_table) for item in set(symbols_df[symbols_df.ambiguous_ticker == False].symbol)])

non_ambiguous_tickers = set(symbols_df[symbols_df.ambiguous_ticker == False].symbol)
company_name_df = pd.read_csv(BASE_DIR + 'company_name_df.csv')
company_titles = set(company_name_df.title)
non_ambiguous_company_titles = set(company_name_df[company_name_df.ambiguous_title == False].title)
