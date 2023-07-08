import joblib
import neattext.functions as nfx
#from sentimentModel.predictSentiment import predictSentimentFunc
pipeline_file = open("backend\server\emotionModel\emotion_classifier.pkl", "rb")
pipe_lr = joblib.load(pipeline_file)
pipeline_file.close()





def preprocess_text(text):
    # Remove user handles
    clean_text = nfx.remove_userhandles(text)
    # Remove stopwords
    clean_text = nfx.remove_stopwords(clean_text)
    return clean_text

def predict_emotion(text):
    #print("Sentiment",predictSentimentFunc(text),predictSentimentFunc(text)=='NEGATIVE')
    clean_text = preprocess_text(text)
    prediction = pipe_lr.predict([clean_text])
    probability = pipe_lr.predict_proba([clean_text])
    #print(prediction)
    return prediction[0]

# ex1 = "Covid rise people dying"
# emotion, probability = predict_emotion(ex1)
# print("Emotion:", emotion)
# print("Probability:", probability)
