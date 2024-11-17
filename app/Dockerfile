FROM python:3.12-slim AS builder
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    gcc \
    binutils \
    postgresql-client-common \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

EXPOSE 8000

COPY requirement.txt /
RUN pip3 install -r requirement.txt 

COPY docker-entrypoint.sh /
RUN chmod +x /docker-entrypoint.sh
ENTRYPOINT ["/docker-entrypoint.sh"]