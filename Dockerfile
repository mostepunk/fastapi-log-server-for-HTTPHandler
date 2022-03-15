FROM nexus.utkonos.dev:5000/python:3.8-slim-buster

ENV PYTHONUNBUFFERED 1

EXPOSE 5000
WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip       && \
    pip install -r requirements.txt && \
    find / -name __pycache__ -type d | xargs rm -rf

COPY app .
