# Use a base CUDA image with OpenGL support
FROM python:3.8

# Set the working directory inside the container
WORKDIR /app

# Copy the code and requirements.txt file
COPY . /app//

# Install the dependencies
RUN apt-get update && apt-get install -y python3-opencv
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port on which the Flask application runs (default is 5000)
EXPOSE 5000

# Start the application
CMD ["python", "app.py"]
