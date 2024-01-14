Will build MLOps system that predicts the popularity of a Youtube video by predicting the number of likes a video will get.

Data for the video is taken from [this Kaggle dataset](https://www.kaggle.com/datasets/thedevastator/youtube-video-and-channel-analysis).

Steps:
1. Train a model on the above dataset tracking the experiments using MLFlow

2. Create a model training pipeline

3. Deploy the model in batch, web service or streaming

4. Monitor the performance of the model


I will try to follow the best coding practices by 
- implementing pytests
- using linters and code formatters
- using makefile and pre-commit hooks