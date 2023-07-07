# Base Image
FROM python:latest

# Working dir
RUN mkdir /src
RUN mkdir /src/matching_service
RUN touch /src/__init__.py
COPY . /src/matching_service

# Copy requirements.txt
COPY ./requirements.txt ./

# Install requirements
RUN pip install --no-cache-dir -r requirements.txt

# Copy files
COPY . /home/matching_service/
