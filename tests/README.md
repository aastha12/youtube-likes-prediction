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
pipenv install --dev black isort
```

To see what changes Black would have made to a file:
```bash
black ../model/likes-prediction.py --diff
```

To apply those changes run:
```bash
black ../model/likes-prediction.py
black ../prefect-workflow/likes-prediction.py
black ../deployment/predict.py
black ../monitoring/evidently_metrics_calculation.py
```

To see what changes isort would have made to a file:
```bash
isort ../model/likes-prediction.py --diff
```

To apply those changes run:
```bash
isort ../model/likes-prediction.py
isort ../prefect-workflow/likes-prediction.py
isort ../deployment/predict.py
isort ../monitoring/evidently_metrics_calculation.py
```

Then to run the linter on a file:
```bash
cd prefect-workflow
. /Users/aasth/.local/share/virtualenvs/prefect-workflow-q6xtxK7U/bin/activate
pylint likes-prediction.py
```

## Pre-commit hooks:

We can configure to run pytests,pylint,black and isort automatically before committing.

In the `test` venv and in the `youtube-likes-prediction` folder, run:
```bash
pipenv install --dev pre-commit
```
Do `git init` to initialize an empty git repository in the code folder. You'll see a `.git` folder being created after you execute the `git init` command. Type `ls -a` in the command line to verify that the .git folder was created.

Then we need to create a `.pre-commit-config.yaml` file before running the `pre-commit` command. Type `pre-commit sample-config` (in the `youtube-likes-prediction` directory with the `test` environment activated) to see see a sample content for the `.pre-commit-config.yaml` file. You can copy this content and then create a `.pre-commit-config.yaml` file and paste the contents in this file.

Run `pre-commit install` in the command line. This creates a pre-commit folder in the `.git` folder. The`.git` folder isn't committed to git. The `.git` folder is a local folder that is created which means whenever you clone a repo, you need to run `pre-commit install` first to create the pre-commit folder.

Now, proceed to do `git add .` and `git commit -m "some message"` and you will see that some hooks may say "Failed" but it will have a "files were modified by this hook" message which means the hook modified the file to make it pass. So the next time you do `git add .` and `git commit`, you'll notice that same hook will now Pass.

<img src="/images/pre-commit-hooks.png" width=700>
