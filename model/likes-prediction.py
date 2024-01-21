#!/usr/bin/env python
# coding: utf-8

# In[28]:


from datetime import datetime

import category_encoders as ce
import lightgbm as lgb
import mlflow
import pandas as pd
from catboost import CatBoostRegressor
from mlflow.tracking import MlflowClient
from sklearn.linear_model import ElasticNet
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import QuantileTransformer, RobustScaler

# In[2]:


mlflow.set_tracking_uri("http://127.0.0.1:5000")
mlflow.set_experiment("my-experiment-1")


# In[3]:


data = pd.read_csv("../data/YouTubeDataset_withChannelElapsed.csv")


# In[4]:


data.head()


# In[5]:


# data.columns


# I will select only the required columns for the prediction

# In[6]:


selected_columns = [
    "index",
    "channelId",
    "videoCategoryId",
    "channelViewCount",
    "videoCount",
    "subscriberCount",
    "videoId",
    "channelelapsedtime",
    "channelCommentCount",
    "videoViewCount",
    "elapsedtime",
    "videoLikeCount",
    "videoDislikeCount",
    "videoPublished",
    "VideoCommentCount",
]

data = data[selected_columns]

data.head()


# In[7]:


data.describe()


# There are some negative values in the dataset which doesn't make
# sense logically so I will remove those values

# In[8]:


data = data[
    (data["videoViewCount"] >= 0)
    & (data["videoLikeCount"] >= 0)
    & (data["videoDislikeCount"] >= 0)
    & (data["VideoCommentCount"] >= 0)
]

data.head(2)


# In[9]:


data.describe()


# In[10]:


data.isnull().sum()


# In[11]:


data.skew(numeric_only=True)


# In[12]:


# data.dtypes


# In[13]:


# data.corr(numeric_only=True)["videoLikeCount"]


# In[14]:


data_copy = data.copy()
y = data["videoLikeCount"]
X = data.drop(["videoLikeCount"], axis=1)


# ElasticNet as baseline model

# In[15]:


with mlflow.start_run():
    mlflow.set_tag("model", "Elastic Net Pipeline")

    mlflow.log_param("train-data-path", "data/YouTubeDataset_withChannelElapsed.csv")

    cat_encoder = ce.CatBoostEncoder(
        cols=list(X.select_dtypes(include="object").columns)
    )
    qt = QuantileTransformer(output_distribution="normal")
    rs = RobustScaler()
    en = ElasticNet(random_state=123)
    en_pipeline = Pipeline(
        [
            ("Cat_Encoder", cat_encoder),
            ("Quantile transformer", qt),
            ("Scaling", rs),
            ("Elastic Net", en),
        ]
    )
    en_scores = cross_val_score(
        en_pipeline, X, y, cv=3, scoring="neg_root_mean_squared_error"
    )

    mlflow.log_metric("rmse", -en_scores.mean())
    mlflow.sklearn.log_model(en_pipeline, artifact_path="models")
    print(f"default artifacts URI: '{mlflow.get_artifact_uri()}'")


# I will use lightgbm as it can handle categorical features and it works fast too.
#
# LGBM can handle categorical features by changing the data types pf these features to "category".
# However it is mentioned in the http://lightgbm.readthedocs.io/en/latest/Advanced-Topics.html
# that for high cardinality datasets it is better to convert the categorical data as numeric

# In[15]:


# lightgbm needs categorical features to be of type 'category'

X_lightgbm = X.copy()
for cat_cols in X_lightgbm.select_dtypes(include="object").columns:
    X_lightgbm[cat_cols] = X_lightgbm[cat_cols].astype("category")

# X_lightgbm.dtypes


# In[50]:


with mlflow.start_run():
    mlflow.set_tag("model", "LightGBM Regressor")
    mlflow.log_param("train-data-path", "data/YouTubeDataset_withChannelElapsed.csv")

    lightgbm_reg = lgb.LGBMRegressor(random_state=123, verbose=-1)
    lightgbm_reg.fit(X_lightgbm, y)
    scores = cross_val_score(
        lightgbm_reg, X_lightgbm, y, scoring="neg_root_mean_squared_error", cv=3
    )

    mlflow.log_metric("rmse", -scores.mean())
    mlflow.sklearn.log_model(lightgbm_reg, artifact_path="models")
    print(f"default artifacts URI: '{mlflow.get_artifact_uri()}'")


# In[52]:


with mlflow.start_run():
    mlflow.set_tag("model", "LightGBM Regressor Pipeline")
    mlflow.log_param("train-data-path", "data/YouTubeDataset_withChannelElapsed.csv")

    lightgbm_reg = lgb.LGBMRegressor(random_state=123, verbose=-1)
    light_pipeline = Pipeline(
        [("Cat_Encoder", cat_encoder), ("LightGBM", lightgbm_reg)]
    )
    light_pipeline.fit(X_lightgbm, y)
    scores = cross_val_score(
        light_pipeline, X_lightgbm, y, scoring="neg_root_mean_squared_error", cv=3
    )

    mlflow.log_metric("rmse", -scores.mean())
    mlflow.sklearn.log_model(light_pipeline, artifact_path="models")
    print(f"default artifacts URI: '{mlflow.get_artifact_uri()}'")


# In[20]:


with mlflow.start_run():
    mlflow.set_tag("model", "CatBoost Regressor")
    mlflow.log_param("train-data-path", "data/YouTubeDataset_withChannelElapsed.csv")

    cat = CatBoostRegressor(
        random_state=123,
        cat_features=list(X.select_dtypes(include="object").columns),
        verbose=False,
    )
    cat.fit(X, y)
    scores = cross_val_score(cat, X, y, scoring="neg_root_mean_squared_error", cv=3)

    mlflow.log_metric("rmse", -scores.mean())
    mlflow.sklearn.log_model(cat, artifact_path="models")
    print(f"default artifacts URI: '{mlflow.get_artifact_uri()}'")


# Let's see which model performed the best

# In[15]:


client = MlflowClient("http://127.0.0.1:5000")
runs = client.search_runs(experiment_ids="1", order_by=["metrics.rmse ASC"])


# In[16]:


for run in runs:
    duration = (run.info.end_time - run.info.start_time) / 1000
    print(
        f"run id: {run.info.run_id}, model name: {run.data.tags['model']},"
        + f"rmse: {run.data.metrics['rmse']:.4f}, duration(s): {duration:.2f}"
    )


# We can see that the LightGBM Regressor Pipeline performed the best but it took more
# than double the time of a simple LightGBM Regressor. The simple LGBM Regressor is able to
# give a similar mse at a much faster time so let's use that.
#
# Note for Hyperparameter Tuning: I will convert my dataset into lightgbm.DataSet() type
# as it will make the computation more efficient.
# More info can be found here -
# https://stackoverflow.com/questions/65924856/lightgbm-intent-of-lightgbm-dataset
# The hyperparameter tuning process was taking too long so I didn't continue with it.

# In[23]:


run_id = "bbdfddcf7a3f460bba46b24978de3707"
mlflow.register_model(model_uri=f"runs:/{run_id}/models", name="yt-likes-regressor")


# In[24]:


# check if model was registered

client.search_registered_models()


# In[25]:


model_name = "yt-likes-regressor"
latest_versions = client.get_latest_versions(name=model_name)

for version in latest_versions:
    print(f"version: {version.version}, stage: {version.current_stage}")


# In[26]:


# moving model to staging
model_version = 1
new_stage = "Staging"
client.transition_model_version_stage(
    name=model_name,
    version=model_version,
    stage=new_stage,
    archive_existing_versions=False,
)


# In[27]:


client.transition_model_version_stage(
    name=model_name, version=1, stage="Production", archive_existing_versions=True
)


# In[29]:


date = datetime.today().date()

client.update_model_version(
    name=model_name,
    version=1,
    description=f"The model version 1 was transitioned to Production on {date}",
)


# In[ ]:
