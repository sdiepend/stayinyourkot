FROM python:3.7

ENV INSTALL_PATH=/app/corona

RUN apt-get -qq update && \
    apt-get upgrade -y && \
    apt-get install -y gcc libpq-dev apt-utils

RUN mkdir -p $INSTALL_PATH
WORKDIR $INSTALL_PATH

COPY viz viz/
COPY requirements.txt requirements.txt

#COPY requirements.txt requirements.txt

RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    rm -f requirements.txt

EXPOSE 8000

CMD gunicorn -b :8080 viz.app:app.server