FROM python:3.12

WORKDIR /app

COPY . /app

RUN apt-get update && \
    apt-get install -y libgl1-mesa-glx && \
    apt-get install libzbar0 -y && \
    apt-get install -y poppler-utils && \
    pip install -r requirements.txt
    