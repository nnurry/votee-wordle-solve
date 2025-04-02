# Use the official Python 3.12 Alpine image as the base image
FROM python:3.12-alpine

# Set the working directory inside the container
WORKDIR /app

# Copy only the requirements file to leverage Docker's caching mechanism
COPY requirements.txt ./

# Install Python dependencies specified in requirements.txt
# --no-cache-dir: Avoid caching to reduce image size
RUN pip install --no-cache-dir --requirement requirements.txt

# Copy Python source files and the words.txt file into the container
COPY *.py words.txt ./
