FROM python:3

WORKDIR /app

# ユーザー追加
RUN adduser -u 1000 --disabled-password --gecos "" appuser
USER appuser

# PDMインストール
RUN curl -sSL https://raw.githubusercontent.com/pdm-project/pdm/main/install-pdm.py | python3 -

CMD [ "/bin/bash" ]