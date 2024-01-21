import pickle
import pandas as pd
from flask import Flask, request, jsonify

with open('/Users/aasth/Desktop/Data analytics/MLOps/youtube-likes-prediction/tests/deployment/lightgbm_reg.bin', 'rb') as f_in:
    model = pickle.load(f_in)

def prepare_data(video):

    df = pd.DataFrame([video])

    df = df[(df['videoViewCount']>=0) & 
        (df['videoDislikeCount']>=0) & 
        (df['VideoCommentCount']>=0)
        ]    
    
    for cat_cols in df.select_dtypes(include='object').columns:
        df[cat_cols] = df[cat_cols].astype('category') 

    return df 


def predict(data):
    preds = model.predict(data)
    return int(preds[0])


app = Flask("yt-likes-prediction")

@app.route('/predict',methods=['POST'])
def predict_endpoint():
    video = request.get_json()

    data = prepare_data(video)
    pred = predict(data)    

    result = {
        'videoLikeCount':pred
    }

    return jsonify(result)

if __name__=="__main__":
    app.run(debug=True,host='0.0.0.0',port=9696)