FROM python:3.12-slim AS builder

WORKDIR /app
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    gcc \
    binutils \
    postgresql-client-common \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

EXPOSE 8000

COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip3 install -r requirements.txt 

COPY docker-entrypoint.sh /
RUN chmod +x /docker-entrypoint.sh
COPY . /app

ENTRYPOINT ["/bin/sh","/docker-entrypoint.sh"]