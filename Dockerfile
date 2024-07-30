FROM python:3.11.4-alpine

ARG ENVIRONMENT=prod

RUN apk add --no-cache curl wget bash

WORKDIR /code

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

COPY .env.a .env

CMD ["python", "main.py"]