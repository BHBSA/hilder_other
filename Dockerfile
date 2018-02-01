# Use an official Python runtime as a parent image
FROM python:3.5

# Set the working directory to /app
WORKDIR /other

# Copy the current directory contents into the container at /app
ADD . /other

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Define environment variable
ENV NAME hilder_other

# Run run.py when the container launches
CMD ["python", "run.py"]