FROM python:3.12-slim AS builder
EXPOSE 8000

WORKDIR /app 

COPY requirement.txt /app
RUN pip3 install -r requirement.txt 

COPY . /app 

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
