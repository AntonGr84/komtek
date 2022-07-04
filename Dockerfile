FROM python:3.8-alpine3.15

EXPOSE 8000

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# RUN apk update && apk add gcc musl-dev
RUN pip install --upgrade pip
WORKDIR /usr/src/app
COPY requirements.txt .
RUN python -m pip install -r requirements.txt
COPY ./wait-db.sh /tmp
COPY . /usr/src/app

# RUN mkdir /usr/media
RUN adduser -u 5678 --disabled-password --gecos "" django
RUN chown -R django /usr/src/app
USER django