FROM python:3


ENV PYTHONUNBUFFER 1
RUN mkdir /referral_api
WORKDIR /referral_api
COPY . /referral_api/
RUN pip install -r requirements.txt
