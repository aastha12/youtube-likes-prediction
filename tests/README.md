## Virtual enviroment

1. Go to the correct directory by:,
```bash
cd tests
```
2. Activate any existing conda virtual evironment:,
```bash,
    . /opt/homebrew/anaconda3/bin/activate
```
3. Create a new virtual environment: `pipenv install`
4. Activate it by `pipenv shell`
5. Install pytest with `pipenv install --dev pytest`. We use the dev argument cause we want pytest only in the dev environment and not in the production environment.
6. Find the location of your virtual environment by typing `pipenv --venv`. You'll get the path `/Users/aasth/.local/share/virtualenvs/tests-XANs4QQD` to the venv. Copy the path.
7. We need to set up our python envionment in VSCode. Hit `Cmd+Shift+P` -> `Select Python Interpreter` and paste the path of the venv that you copied in step 6.
8. We will configure the python tests. Click on the `Testing` tab which is lcoated on the left panel of VSCode. Click om the `Configure Python Tests` button. Select `pytest` and the `test` directory.

If you are already in the right directory and have created the venv earlier then you can activate it by:
```bash
. /Users/aasth/.local/share/virtualenvs/tests-XANs4QQD/bin/activate
```

## Running the pytest:

Note: Check out [this](https://madewithml.com/courses/mlops/testing/#fixtures) page for testing ML systems

Once you are in the `tests` venv and folder, run

```bash
pytest deployment/test_predict.py
```
<img src="/images/pytest.png" width=700>

## Linters, Formatting & Imports:

In the `test` venv and folder,, run
```bash
pipenv install --dev pylint

```

Then to run the linter on a file: 
```bash
pylint ../model/likes-prediction.py
```