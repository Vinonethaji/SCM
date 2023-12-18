# Use the official Python runtime as a parent image
FROM python:3.12.0

# Set the working directory to /app
WORKDIR /SCMEXPERT/kafka/consumer

# Install any needed packages specified in requirements.txt
RUN pip install confluent-kafka pymongo python-dotenv


# Copy the rest of the application code into the container at /app
COPY . /SCMEXPERT/kafka/consumer

# Copy the codec.py file into the container

# Define the command to run your FastAPI application when the container starts
CMD ["python", "consumer.py"]