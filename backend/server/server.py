from flask import Flask, request, jsonify
from flask_cors import CORS
from sentimentModel.predictSentiment import predictSentimentFunc
from emotionModel.predictEmotion import predict_emotion
from bertModel.bertModel import get_sentiment_output
app = Flask(__name__)
CORS(app)



@app.route('/api', methods=['POST'])
def process_post_request():
    data = request.get_json()  
    print(data,data['text'],predict_emotion(data['text']))
    #modelOutput=predictSentimentFunc(data['text'])
    no_output='Invalid query !. I can only recommend medicines to relevant queries. Apologies I can\'t find any medicines.'
    output=''

    
    emotion = predict_emotion(data['text'])
    sentimentModelOutput=get_sentiment_output(data['text'])
    # if(sentimentModelOutput=='POSITIVE'):
    #     response = {
    #     'message': 'Success',
    #     'data': no_output,
    #     'modelOutput':emotion,
    #     }
    #     return jsonify(response), 200

    if emotion == "sadness":
        output+="For sadness, Ayurvedic medicine recommendations include: Ashwagandha, Brahmi, Jatamansi,Aconitum nap., Butyricum acidum (tds), Ignatia amara, Kalium phos and Saffron ."
    elif emotion == "fear":
        output+="If you're experiencing fear, you may find Ayurvedic remedies such as Aconitum nap., Anacardium ori., Argentum nit., Arsenicum alb., Kalium carb helpful."
    elif emotion == "anger":
        output+="To address anger, consider Ayurvedic medicines like Calcarea ars., Colocynthis, Conium mac., Lycopodium, Nux vomica."
    elif emotion == "disgust":
        output+="For feelings of disgust, Ayurveda suggests trying remedies such as Ashwagandha, Brahmi, Shankhpushpi, and Tulsi (Holy Basil)."
    elif emotion == "shame":
        output+="If you're struggling with shame, Ayurvedic medicines like Ashwagandha, Brahmi, Shankhpushpi, and Jatamansi may be beneficial."
    # else:
    #     out=check_emotion(data['text'])
    #     if out is not None:
    #         output+=out
    if len(output)>0:
        output+="\n Please note that these recommendations are provided for informational purposes only. It's important to consult with a healthcare professional or Ayurvedic practitioner for personalized advice and appropriate dosage based on your specific needs and constitution."
    else:
        output+=no_output
    response = {
        'message': 'Success',
        'data': output,
        'modelOutput':emotion,
    }

    return jsonify(response), 200


@app.route('/api/sentiment', methods=['POST'])
def check_sentiment():
    
    data = request.get_json() 
  
    
    modelOutput=get_sentiment_output(data['text'])

    
   
    print("Text:", data['text'])
    print("Sentiment:", modelOutput)
    response = {
        'message': 'Success',
        'sentiment':modelOutput
    }
  
    return jsonify(response), 200



@app.route('/api', methods=['GET'])
def process_get_request():
    # Process the GET request as needed
    # ...

    # Create a response
    response = {
        'message': 'Success',
        'data': 'This is a GET request'
    }

    return jsonify(response), 200


if __name__ == '__main__':
    app.run()
