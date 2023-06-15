# Use the official Python image as the base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the code files to the container
COPY . /app

# Install the required dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set the command to run the script
CMD ["python", "extract.py"]
