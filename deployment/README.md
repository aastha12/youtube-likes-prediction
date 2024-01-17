 
 ## Virtual environment:

 1. We need to get the scikit-learn & lightgbm version used to train and test the model:
 ```bash 
 cd model
 . /Users/aasth/.local/share/virtualenvs/model-RCtldyqy/bin/activate
 pip list | grep scikit-learn 
  pip list | grep lightgbm
 ```

 2. In my case `scikit-learn==1.3.2` and `lightgbm==4.2.0` version was used, so we will create a venv using this:
 ```bash
 cd deployment
 . /opt/homebrew/anaconda3/bin/activate #activate conda
pipenv install scikit-learn==1.3.2 flask
pipenv shell
pipenv install lightgbm==4.2.0
 ```

 3. If you have already created this environment and want to activate it later on, use the following:
 ```bash
 . /Users/aasth/.local/share/virtualenvs/deployment-g9Ff-FmE/bin/activate
 ```

## Flask:

 4. I will put the lightgbm model in a Flask application so that we can interact with it and get a prediction:
 
    - Check out the `predict.py` file to see how I added Flask to the prediction script. (Make sure you are in the `deployment` virtual environment and `deployment` folder and run `python predict.py` to run the prediction script.)

    - To request a prediction from the server, I created another file `test.py`. This file will post the video information to the server and print out the response (i.e: The predicted likes). While the prediction script is running on the terminal, open up another terminal and make sure you are in the `deployment` virtual environment and run `python test.py` to run the get a prediction. 

## WGSI server:

Now that I can see that my app is running fine with Flask, I will switch the servers. Flask is mostly used when you want to develop things locally. We need to use a production server like gunicorn instead of using a development server like Flask. 

```bash
pipenv install gunicorn
gunicorn --bind=0.0.0.0:9696 predict:app
```
and then in another terminal in the `deployment` venv and folder, run `python test.py` and you should get a prediction.

## Docker:

I am going to package the app to Docker for reproducibility, scalability, security.

Check out the version of python by typing `python -V` in the command line. I will create a DockerFile using this information.

Open the Docker app and while it is open in the background, we then build the Docker Image with:
(in the `deployment` venv and folder)
```bash
docker build -t youtube-likes-prediction-service:v1 .
```
In the above, youtube-likes-prediction-service is the image name and v1 is the tag.

And run the container that was built with:
```bash
docker run -it --rm -p 9696:9696 youtube-likes-prediction-service:v1
```

Now when we request predictions like earlier, we're instead calling the WGSI within the Docker Container. While the container is running in the terminal , open another terminal and make sure you are in the `deployment` venv and run `python test.py` to run the get a prediction.