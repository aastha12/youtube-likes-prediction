import pandas as pd
from sklearn.model_selection import cross_val_score
import lightgbm as lgb
import mlflow
from prefect import flow, task

@task(name="read_data")
def read_data(filename: str) -> pd.DataFrame:
    data = pd.read_csv(filename)

    # I will select only the required columns for the prediction
    selected_columns =['index','channelId','videoCategoryId', 'channelViewCount',
                        'videoCount', 'subscriberCount', 'videoId','channelelapsedtime',
                        'channelCommentCount', 'videoViewCount','elapsedtime', 'videoLikeCount', 
                        'videoDislikeCount','videoPublished', 'VideoCommentCount']

    data = data[selected_columns]

    return data

@task(name="prepare_data")
def prepare_data(data: pd.DataFrame) -> pd.DataFrame:
    # There are some negative values in the dataset which doesn't make sense logically so I will remove those values
    data = data[(data['videoViewCount']>=0) & 
        (data['videoLikeCount']>=0) & 
        (data['videoDislikeCount']>=0) & 
        (data['VideoCommentCount']>=0)
        ]

    data_copy = data.copy()
    y=data['videoLikeCount']
    X=data.drop(['videoLikeCount'],axis=1)

    # lightgbm needs categorical features to be of type 'category'
    X_train = X.copy()
    y_train=y.copy()
    for cat_cols in X_train.select_dtypes(include='object').columns:
        X_train[cat_cols] = X_train[cat_cols].astype('category')
    
    return X_train,y_train
    
@task(name="train_best_model",log_prints=True)
def train_best_model(
    X_train: pd.DataFrame,
    y_train: pd.DataFrame
) -> None:
    with mlflow.start_run():

        mlflow.set_tag("model", "LightGBM Regressor")
        mlflow.log_param("train-data-path", "data/YouTubeDataset_withChannelElapsed.csv")

        lightgbm_reg=lgb.LGBMRegressor(random_state=123,verbose=-1)
        lightgbm_reg.fit(X_train,y_train)
        scores = cross_val_score(lightgbm_reg, X_train, y_train, scoring='neg_root_mean_squared_error', cv=3)

        mlflow.log_metric("rmse", -scores.mean())
        mlflow.sklearn.log_model(lightgbm_reg, artifact_path="models")


@flow
def main_flow(
    train_path: str = '/Users/aasth/Desktop/Data analytics/MLOps/youtube-likes-prediction/data/YouTubeDataset_withChannelElapsed.csv'
) -> None:
    """The main training pipeline"""

    # MLflow settings
    mlflow.set_tracking_uri("sqlite:///mlflow.db")
    mlflow.set_experiment("my-experiment-1")    

    # Load
    df_train = read_data(train_path)

    # Transform
    X_train, y_train= prepare_data(df_train)

    # Train
    train_best_model(X_train, y_train)


if __name__ == "__main__":
    main_flow()


