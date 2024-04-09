FROM python:3.11.1-slim-buster

WORKDIR /app

RUN apt-get update && apt-get install -y netcat

COPY entrypoint.sh docker-entrypoint.sh
RUN chmod +x docker-entrypoint.sh

COPY requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./app /app
RUN pybabel compile -d locales -D messages;

ENTRYPOINT ["sh", "/app/docker-entrypoint.sh"]
