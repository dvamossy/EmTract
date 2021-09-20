from keras.models import load_model


class ModelInference:

    MODEL_BASE_PATH = '../build/models/'

    def __init__(self):
        self.model = load_model(ModelInference.MODEL_BASE_PATH + 'twitter.h5')


    def inference(self, df):
        pass