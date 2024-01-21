This is a local MLOps system that predicts the popularity of a Youtube video by predicting the number of likes a video will get.

Data for this project is taken from [this Kaggle dataset](https://www.kaggle.com/datasets/thedevastator/youtube-video-and-channel-analysis).

Steps:
1. Train a model on the above dataset tracking the experiments using MLFlow ✅

<img src="/images/mlflow runs compare.png" width=400>

2. Create a workflow orchestration using prefect ✅

<img src="/images/prefect workflow.png" width=400>

3. Deploy the model as web service using flask and docker ✅

<img src="/images/deployment.png" width=400>

4. Monitor the performance of the model using Evidently and build grafana dashboard based on Evidently metrics ✅

<img src="/images/grafana.png" width=400>

I will try to follow the best coding practices by
- implementing pytests ✅
- using linters and code formatters ✅
- using makefile and pre-commit hooks ✅


Potential Improvements:

 - For (3): You can also try to load the model from mlflow cloud or some other cloud service (instead of local path)
