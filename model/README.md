
## Virtual Envrionment:

1. Activate conda by 
```bash 
cd model
. /opt/homebrew/anaconda3/bin/activate
```

2. Create and install libraries:
```bash 
pipenv install -r requirements.txt
```

3. If you are opening a new terminal, you can activate it by doing:
```bash
cd model
. /Users/aasth/.local/share/virtualenvs/model-RCtldyqy/bin/activate
```

4. While in the `model` folder and in the `model` venv, run the below command to open the mlflow ui:
```bash
mlflow ui --backend-store-uri sqlite:///mlflow.db
```

5. While in the `model-RCtldyqy` venv, I will convert the [likes-prediction.ipynb](./likes-prediction.ipynb) to a script using:
```bash 
jupyter nbconvert --to python likes-prediction.ipynb
```