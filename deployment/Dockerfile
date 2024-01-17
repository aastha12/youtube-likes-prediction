FROM python:3.11-slim

RUN pip install -U pip
RUN pip install pipenv

#to avoid "libgomp.so.1: cannot open shared object file" error
RUN apt-get update && apt-get install -y --no-install-recommends apt-utils
RUN apt-get -y install curl
RUN apt-get install libgomp1

#go to the app directory
WORKDIR /app 

#copy the pipfile and pip lock file into the current directory
COPY ["Pipfile","Pipfile.lock","./"]

#install all the depedencies
RUN pipenv install --system --deploy

#copy predict file and model into current directory
COPY [ "predict.py","lightgbm_reg.bin","./"]

EXPOSE 9696

#we want to run gunicorn
ENTRYPOINT [ "gunicorn", "--bind=0.0.0.0:9696","predict:app" ]