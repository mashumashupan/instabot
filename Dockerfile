FROM python:3

WORKDIR /app

RUN apt -y update && apt -y upgrade
RUN apt install -y libglib2.0-dev libnss3-dev libcups2-dev libxss-dev libasound2-dev libpangocairo-1.0-0 libatk1.0-dev libatk-bridge2.0-dev libgtk-3-dev
ARG CHROME_VERSION="98.0.4758.9-1"
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add && \
    wget http://dl.google.com/linux/deb/pool/main/g/google-chrome-unstable/google-chrome-unstable_${CHROME_VERSION}_amd64.deb && \
    apt-get install -y -f ./google-chrome-unstable_${CHROME_VERSION}_amd64.deb

ARG CHROME_DRIVER_VERSION="98.0.4758.102"
ADD https://chromedriver.storage.googleapis.com/${CHROME_DRIVER_VERSION}/chromedriver_linux64.zip /opt/chrome/
RUN unzip /opt/chrome/chromedriver_linux64.zip -d /opt/chrome/

# ユーザー追加
RUN adduser -u 1000 --disabled-password --gecos "" appuser
USER appuser

# Poetryインストール
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -

CMD [ "/bin/bash" ]