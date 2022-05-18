from enum import Enum

import pandas as pd
import torch
import transformers
from datasets import Dataset
from scipy.special import softmax

from .processors.cleaning import clean_tweet

# We will leverage the trainer for predictions
TRAINING_ARGS = transformers.TrainingArguments(
    output_dir="results",
    num_train_epochs=8,
    learning_rate=2e-5,
    per_device_train_batch_size=BATCH_SIZE,
    per_device_eval_batch_size=BATCH_SIZE * 16,
    load_best_model_at_end=True,
    metric_for_best_model="loss",
    weight_decay=0.01,
    evaluation_strategy="epoch",
    save_strategy="epoch",
    disable_tqdm=False,
)

# We use the same tokenizer for both models
tokenizer = transformers.DistilBertTokenizerFast.from_pretrained(
    f"./build/models/emotion-twitter", model_max_length=64
)


def tokenize(batch):
    return tokenizer(
        batch["text"], truncation=True, padding="max_length", max_length=64
    )


def batch_predict(model, dataset):
    trainer = transformers.Trainer(model=model, args=TRAINING_ARGS)
    preds_output = trainer.predict(dataset)
    probabilities = softmax(preds_output[0], axis=1)
    return probabilities


class ModelType(Enum):
    TWITTER = "twitter"
    STOCK_TWITS = "stocktwits"


class Model:

    MODEL_BASE_PATH = "./build/models/"
    DATA_BASE_PATH = "./emtract/data/"

    def __init__(self, model_type: ModelType):
        self.model = transformers.DistilBertForSequenceClassification.from_pretrained(
            Model.MODEL_BASE_PATH + f"emotion-{model_type}", num_labels=7
        )
        self.model_type = model_type

    def predict(self, text):
        clean_text = [clean_tweet(t) for t in text]
        dataset = Dataset.from_pandas(pd.DataFrame(clean_text, columns=["text"])).map(
            tokenize, batched=True, batch_size=100000
        )
        dataset.set_format("torch", columns=["input_ids", "attention_mask"])
        y_prob = batch_predict(self.model, dataset)

        emotions = pd.DataFrame(
            {
                "text": text,
                "emotion": y_prob.argmax(axis=-1),
                "neutral": y_prob[:, 0],
                "happy": y_prob[:, 1],
                "sad": y_prob[:, 2],
                "disgust": y_prob[:, 4],
                "anger": y_prob[:, 3],
                "surprise": y_prob[:, 5],
                "fear": y_prob[:, 6],
            }
        )
        return emotions
