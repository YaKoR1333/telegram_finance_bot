FROM python:3.10

WORKDIR /home

ENV TELEGRAM_API_TOKEN="5303421950:AAEu_Zc1JrrrTY1XSzqHOhwDIFbomv-myx8"
ENV TELEGRAM_ACCES_ID="588626327"

ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN pip install -U pip aiogram pytz && apt-get update && apt-get install sqlite3
COPY *.py ./
COPY createdb.sql ./

ENTRYPOINT ["python", "server.py"]