FROM python:3-alpine3.10

COPY requirements.txt .

RUN apk add --no-cache bind-tools bash curl ca-certificates iproute2 make gcc g++ libc-dev libxml2-dev                 \
    libxslt-dev libffi libffi-dev postgresql-dev

ENV CRYPTOGRAPHY_DONT_BUILD_RUST=1
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN mkdir app
COPY . app

WORKDIR app

CMD python manage.py runserver