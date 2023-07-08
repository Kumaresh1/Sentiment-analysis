import numpy as np
import math
import re
import pandas as pd
from bs4 import BeautifulSoup

import tensorflow as tf
import tensorflow_hub as hub

import bert

def clean_tweet(tweet):
    tweet = BeautifulSoup(tweet, "lxml").get_text()
    # Delete the @
    tweet = re.sub(r"@[A-Za-z0-9]+", ' ', tweet)
    # Delete URL links
    tweet = re.sub(r"https?://[A-Za-z0-9./]+", ' ', tweet)
    # Just keep letters and important punctuation
    tweet = re.sub(r"[^a-zA-Z.!?']", ' ', tweet)
    # Remove additional spaces
    tweet = re.sub(r" +", ' ', tweet)
    return tweet

def encode_sentence(sent):
    return tokenizer.convert_tokens_to_ids(tokenizer.tokenize(sent))

class DCNN(tf.keras.Model):
    def __init__(self,
                 vocab_size,
                 emb_dim=128,
                 nb_filters=50,
                 FFN_units=512,
                 nb_classes=2,
                 dropout_rate=0.1,
                 training=False,
                 name="dcnn"):
        super(DCNN, self).__init__(name=name)
        self.embedding = tf.keras.layers.Embedding(vocab_size, emb_dim)
        self.bigram = tf.keras.layers.Conv1D(filters=nb_filters,
                                    kernel_size=2,
                                    padding="valid",
                                    activation="relu")
        self.trigram = tf.keras.layers.Conv1D(filters=nb_filters,
                                     kernel_size=3,
                                     padding="valid",
                                     activation="relu")
        self.fourgram = tf.keras.layers.Conv1D(filters=nb_filters,
                                      kernel_size=4,
                                      padding="valid",
                                      activation="relu")
        self.pool = tf.keras.layers.GlobalMaxPool1D()
        self.dense_1 = tf.keras.layers.Dense(units=FFN_units, activation="relu")
        self.dropout = tf.keras.layers.Dropout(rate=dropout_rate)
        if nb_classes == 2:
            self.last_dense = tf.keras.layers.Dense(units=1, activation="sigmoid")
        else:
            self.last_dense = tf.keras.layers.Dense(units=nb_classes, activation="softmax")

    def call(self, inputs, training):
        x = self.embedding(inputs)
        x_1 = self.bigram(x)
        x_1 = self.pool(x_1)
        x_2 = self.trigram(x)
        x_2 = self.pool(x_2)
        x_3 = self.fourgram(x)
        x_3 = self.pool(x_3)
        merged = tf.concat([x_1, x_2, x_3], axis=-1)
        merged = self.dense_1(merged)
        merged = self.dropout(merged, training)
        output = self.last_dense(merged)
        return output

# Load the tokenizer
FullTokenizer = bert.bert_tokenization.FullTokenizer
bert_layer = hub.KerasLayer("https://tfhub.dev/tensorflow/bert_en_uncased_L-12_H-768_A-12/1", trainable=False)
vocab_file = bert_layer.resolved_object.vocab_file.asset_path.numpy()
do_lower_case = bert_layer.resolved_object.do_lower_case.numpy()
tokenizer = FullTokenizer(vocab_file, do_lower_case)

def get_sentiment_output(text):
    # Preprocess the text
    clean_text = clean_tweet(text)
    tokens = encode_sentence(clean_text)
    inputs = tf.expand_dims(tokens, 0)

    # Load the model and checkpoint
    VOCAB_SIZE = len(tokenizer.vocab)
    EMB_DIM = 200
    NB_FILTERS = 100
    FFN_UNITS = 256
    NB_CLASSES = 2
    DROPOUT_RATE = 0.2

    Dcnn = DCNN(vocab_size=VOCAB_SIZE, emb_dim=EMB_DIM, nb_filters=NB_FILTERS, FFN_units=FFN_UNITS,
                nb_classes=NB_CLASSES, dropout_rate=DROPOUT_RATE)

    checkpoint_path = "backend\server\\bertModel\ckpt_bert_tok\\"
    ckpt = tf.train.Checkpoint(Dcnn=Dcnn)
    ckpt_manager = tf.train.CheckpointManager(ckpt, checkpoint_path, max_to_keep=1)

    if ckpt_manager.latest_checkpoint:
        ckpt.restore(ckpt_manager.latest_checkpoint)
        print("Latest checkpoint restored!")

    # Generate the sentiment output
    output = Dcnn(inputs, training=False)
    sentiment = "POSITIVE" if output > 0.5 else "NEGATIVE"

    return sentiment

# # Example usage
# text = "I'd rather not do that again."
# sentiment = get_sentiment_output(text)
# print(f"The sentiment of '{text}' is: {sentiment}")
