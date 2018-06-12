# Use an official Python runtime as a parent image
FROM python:3.5

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Run run.py when the container launches
CMD ["python", "start_baidu_qianxi_baike.py"]