
## Virtual Envrionment:

1. Activate conda by 
```bash 
cd prefect-workflow
. /opt/homebrew/anaconda3/bin/activate
```

2. Create and install libraries:
```bash 
pipenv install -r requirements.txt
```

3. If you are opening a new terminal, you can activate it by doing:
```bash
cd prefect-workflow
. /Users/aasth/.local/share/virtualenvs/prefect-workflow-q6xtxK7U/bin/activate
```

4. I have copied the [likes-prediction.py](/model/likes-prediction.py) file from the `model` folder into the `prefect-workflow` folder. I will clean up the script, add prefect flows and use it to deploy my model.

5. Open 3 terminals and make sure you are in the `prefect-workflow` folder with the `prefect-workflow` venv activated. 

a. In the first terminal, type:
```bash
prefect project init
prefect server start
```

b. In the second terminal, type:
```bash
prefect config set PREFECT_API_URL=http://127.0.0.1:4200/api
prefect worker start -p workerpool -t process
```

c. In the third terminal, type:
```bash
prefect deploy "/Users/aasth/Desktop/Data analytics/MLOps/youtube-likes-prediction/prefect-workflow"/likes-prediction.py:main_flow -n likes-predictor -p workerpool

prefect deployment run 'main-flow/likes-predictor'
```