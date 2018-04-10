FROM python:3

COPY . /var/apps/blockchain/

WORKDIR /var/apps/blockchain/

RUN pip install -r requirements.txt
