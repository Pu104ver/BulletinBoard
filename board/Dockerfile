FROM python:3.12

ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code

RUN python -m pip install --upgrade pip
COPY requirements.txt /code/
RUN python -m pip install -r requirements.txt

COPY . /code/

EXPOSE 8000