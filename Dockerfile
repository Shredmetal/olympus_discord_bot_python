# Use an official Python runtime as a parent image
FROM python:3.11-buster

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Run bot.py when the container launches
CMD ["python", "-m", "src.bot.bot"]