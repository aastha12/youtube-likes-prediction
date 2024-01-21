# pylint: disable-all

import pickle

import pandas as pd
from flask import Flask, jsonify, request

with open(
    (
        "/Users/aasth/Desktop/Data analytics/MLOps/"
        "youtube-likes-prediction/tests/deployment/lightgbm_reg.bin"
    ),
    "rb",
) as f_in:
    model = pickle.load(f_in)


def prepare_data(video):
    """
    Preprocesses the input video data for prediction.

    Parameters:
    - video (dict): Dictionary containing video data.

    Returns:
    - pd.DataFrame: Preprocessed DataFrame for prediction.
    """

    df = pd.DataFrame([video])

    df = df[
        (df["videoViewCount"] >= 0)
        & (df["videoDislikeCount"] >= 0)
        & (df["VideoCommentCount"] >= 0)
    ]

    for cat_cols in df.select_dtypes(include="object").columns:
        df[cat_cols] = df[cat_cols].astype("category")

    return df


def predict(data):
    """
    Makes predictions on the given data using a pre-trained model.

    Parameters:
    - data (pd.DataFrame): Preprocessed data for prediction.

    Returns:
    - int: Predicted value for 'videoLikeCount'.
    """

    preds = model.predict(data)
    return int(preds[0])


app = Flask("yt-likes-prediction")


@app.route("/predict", methods=["POST"])
def predict_endpoint():
    """
    Endpoint for making predictions based on incoming JSON data.

    Returns:
    - Flask response: JSON response containing the predicted 'videoLikeCount'.
    """

    video = request.get_json()

    data = prepare_data(video)
    pred = predict(data)

    result = {"videoLikeCount": pred}

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=9696)
