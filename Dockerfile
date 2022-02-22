FROM python:3

WORKDIR /app

RUN apt -y update && apt -y upgrade
ARG CHROME_VERSION="98.0.4758.9-1"
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add && \
wget http://dl.google.com/linux/deb/pool/main/g/google-chrome-unstable/google-chrome-unstable_${CHROME_VERSION}_amd64.deb && \
apt-get install -y -f ./google-chrome-unstable_${CHROME_VERSION}_amd64.deb

ARG CHROME_
ADD https://chromedriver.storage.googleapis.com/${CHROME_VERSION}/chromedriver_linux64.zip /opt/chrome/

# ユーザー追加
RUN adduser -u 1000 --disabled-password --gecos "" appuser
USER appuser

# Poetryインストール
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -

CMD [ "/bin/bash" ]