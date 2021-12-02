import pickle
from keras.models import load_model
from enum import Enum
from keras.preprocessing.sequence import pad_sequences
import pandas as pd
from .processors.cleaning import clean_tweet


class ModelType(Enum):
    TWITTER = 'twitter'
    STOCK_TWITS = 'stocktwits'

    def get_h5_file_name(self):
        return self.value + '.h5'

    def get_tokenizer(self):
        return 'tokenizer_{}.pickle'.format(self.value)


class Model:

    MODEL_BASE_PATH = './build/models/'
    DATA_BASE_PATH = './emtract/data/'

    def __init__(self, model_type: ModelType):
        self.model = load_model(Model.MODEL_BASE_PATH + model_type.get_h5_file_name())
        self.model_type = model_type
        with open(Model.DATA_BASE_PATH + model_type.get_tokenizer(), 'rb') as handle:
            self.tokenizer = pickle.load(handle)

    def predict(self, text):
        clean_text = [clean_tweet(t) for t in text]
        sequences = self.tokenizer.texts_to_sequences(clean_text)
        data = pad_sequences(sequences, padding='pre', maxlen=30)
        y_prob = self.model.predict(data, batch_size=20000)

        emotions = pd.DataFrame({
            'text': text,
            'emotion': y_prob.argmax(axis=-1),
            'neutral': y_prob[:, 0],
            'happy': y_prob[:, 1],
            'sad': y_prob[:, 2],
            'disgust': y_prob[:, 4],
            'anger': y_prob[:, 3],
            'surprise': y_prob[:, 5],
            'fear': y_prob[:, 6],
        })
        return emotions
