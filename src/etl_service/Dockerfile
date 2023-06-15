# Use the official Python image as the base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /home/app/

# Copy the code files to the container
COPY ./ /home/app/

# update the apt & Install the required dependencies openjdk-11-jdk
RUN  apt-get update && apt-get install -y --no-install-recommends openjdk-11-jdk 

# Install the required dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set the command to run the script
CMD ["python", "extract.py"]
