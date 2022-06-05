FROM python:3.9
# 環境変数の定義
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# 作業ディレクトリの設定
WORKDIR /code
# インストール
ADD requirements.txt /code/
RUN pip install -r requirements.txt 
# プロジェクトフォルダのコピー
COPY . /code/