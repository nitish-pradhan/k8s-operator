FROM python:3.9-alpine
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cahce-dir --upgrade -r requirements.txt
COPY ./app /code/app
RUN ["uvicorn", "app.index:app", "--host", "0.0.0.0", "--port", "80"]