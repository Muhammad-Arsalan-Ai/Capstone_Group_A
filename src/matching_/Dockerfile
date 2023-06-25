# Base Image
FROM python:latest

# Working Dir
WORKDIR /home/matching_service/

# Copy files
COPY . /home/matching_service/

# Update package lists
RUN apt-get update

# RUN apt-get install -y redis-server
RUN apt install -y redis-server

# RUN requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run the fast_api script when the container starts
CMD ["python", "fast_api.py"]