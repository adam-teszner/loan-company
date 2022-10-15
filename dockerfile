FROM python:3.10.8-slim-bullsye
WORKDIR /loan_site
COPY requirements.txt /loan_site/
RUN pip install -r requirements.txt
COPY . /loan_site/
