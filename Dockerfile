# Take python as base image
FROM python:3.9

# Create a directory to work in
WORKDIR /code

# Copy the requirements file to the working directory
COPY ./requirements.txt /code/requirements.txt

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

# Install requirements
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy all code to the working directory
COPY . /code/app

# Run the application on port 80
CMD ["python", "main.py"]