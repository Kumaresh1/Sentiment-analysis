from keras.models import load_model
import pickle
import re
from nltk.corpus import stopwords
from  nltk.stem import SnowballStemmer
import nltk
from keras_preprocessing.sequence import pad_sequences

nltk.download('stopwords')
SEQUENCE_LENGTH = 300
stop_words = stopwords.words("english")
POSITIVE = "POSITIVE"
NEGATIVE = "NEGATIVE"
NEUTRAL = "NEUTRAL"
SENTIMENT_THRESHOLDS = (0.4, 0.7)
stemmer = SnowballStemmer("english")

TEXT_CLEANING_RE = "@\S+|https?:\S+|http?:\S|[^A-Za-z0-9]+"
stop_words = stopwords.words("english")


def preprocess(text, stem=False):
    # Remove link,user and special characters
    text = re.sub(TEXT_CLEANING_RE, ' ', str(text).lower()).strip()
    tokens = []
    for token in text.split():
        if token not in stop_words:
            if stem:
                tokens.append(stemmer.stem(token))
            else:
                tokens.append(token)
    return " ".join(tokens)
def decode_sentiment(score, include_neutral=True):
    if include_neutral:        
        label = NEUTRAL
        if score <= SENTIMENT_THRESHOLDS[0]:
            label = NEGATIVE
        elif score >= SENTIMENT_THRESHOLDS[1]:
            label = POSITIVE

        return label
    else:
        return NEGATIVE if score < 0.5 else POSITIVE

# Load the saved model
model = load_model('model.h5')

# Load the tokenizer and encoder
tokenizer = pickle.load(open('tokenizer.pkl', 'rb'))
encoder = pickle.load(open('encoder.pkl', 'rb'))

# Example text to predict
text = "I love this product!"

# Preprocess the text
preprocessed_text = preprocess(text)

# Tokenize and pad the preprocessed text
x = pad_sequences(tokenizer.texts_to_sequences([preprocessed_text]), maxlen=SEQUENCE_LENGTH)

# Predict the sentiment

def predictSentimentFunc(text):
    

    # Preprocess the text
    preprocessed_text = preprocess(text)

    # Tokenize and pad the preprocessed text
    x = pad_sequences(tokenizer.texts_to_sequences([preprocessed_text]), maxlen=SEQUENCE_LENGTH)

    predictions = model.predict(x)
    sentiment = decode_sentiment(predictions[0])
    print("Text:", text)
    print("Sentiment:", sentiment)
    return sentiment

# Print the sentiment prediction

