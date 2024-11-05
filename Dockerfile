# Use an official Python runtime as a parent image
FROM python:3.12-slim-bullseye AS builder
EXPOSE 8000

# Set up the working directory
WORKDIR /app 

# Copy the requirements file and install dependencies
COPY requirement.txt /app
RUN pip3 install -r requirement.txt --no-cache-dir

# Copy the current directory contents into the container
COPY . /app 
# Entry command
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
