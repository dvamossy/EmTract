import os

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
import pandas as pd

from emtract.model import Model, ModelType


class ModelInference:

    MODEL_BASE_PATH = "build/models/"
    DATA_BASE_PATH = "./emtract/data/"

    def __init__(self, model_type):
        if model_type == "twitter":
            self.model = Model(ModelType.TWITTER)
        else:
            self.model = Model(ModelType.STOCK_TWITS)

    def inference(self, text):
        return self.model.predict([text])

    def file_inference(self, file_name, output):
        df = pd.read_csv(file_name, header=None)
        predictions = self.model.predict(df.iloc[:, 0].values)
        predictions.to_csv(output, index=False)
